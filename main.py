import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QGridLayout, QLabel, QMainWindow, QHBoxLayout, QPushButton, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
import sounddevice as sd
import numpy as np
import utility_functions
from datetime import datetime

from fading_list_widget import FadingListWidget
from midi_reader import MidiReader
from notes_scales_and_chords import Chord, generate_random_chord

class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.fading_list = FadingListWidget(4)
        self.play_label = QLabel('Play -> ')
        self.playing_label = QLabel('Playing: ')
        self.score_label = QLabel('Score: ')
        self.score = QLabel('0')
        self.chord_label = QLabel('')
        self.start_button = QPushButton('Start')
        self.start_button.setStyleSheet('font-size: 36pt')
        self.score.setStyleSheet('font-size: 36pt')
        self.score_label.setStyleSheet('font-size: 36pt')
        self.play_label.setStyleSheet('font-size: 36pt')
        self.playing_label.setStyleSheet('font-size: 36pt')
        self.chord_label.setStyleSheet('font-size: 36pt')
        self.play_label.setAlignment(QtCore.Qt.AlignTop)
        self.align_fix_widget = QWidget()
        self.align_fix_layout = QGridLayout(self.align_fix_widget)
        self.root_widget = QWidget()
        self.root_layout = QGridLayout(self.root_widget)
        self.root_layout.addWidget(self.start_button, 0, 0)
        self.root_layout.addWidget(self.score_label, 1, 0, alignment=QtCore.Qt.AlignRight)
        self.root_layout.addWidget(self.score, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.root_layout.addWidget(self.playing_label, 2, 0, alignment=QtCore.Qt.AlignRight)
        self.root_layout.addWidget(self.chord_label, 2, 1, alignment=QtCore.Qt.AlignLeft)
        self.root_layout.addWidget(self.play_label, 3, 0, alignment=QtCore.Qt.AlignRight)
        self.root_layout.addWidget(self.fading_list, 3, 1, alignment=QtCore.Qt.AlignLeft)
        self.align_fix_layout.addWidget(self.root_widget, 0, 0, alignment=QtCore.Qt.AlignLeft)
        self.setCentralWidget(self.align_fix_widget)
        self.show()
        

    def set_target_list(self, strings: list):
        self.fading_list.set_list(strings)

    def set_chord_label(self, string):
        self.chord_label.setText(string)

    def set_score(self, string):
        self.score.setText(string)

    def set_window_title(self, string):
        self.setWindowTitle(string)

class ProgramBackend(QObject):

    playing_signal = pyqtSignal(str)
    target_signal = pyqtSignal(list)
    score_signal = pyqtSignal(str)
    time_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update)
        self.update_timer.start(50)  #ms

        self.target_chords = []
        self.score = 0
        self.start_time = None

        self.midi_reader = MidiReader(1)
    
    def start(self):
        self.start_time = datetime.now()
        self.score = 0

    def _update(self):
        sequence = self.midi_reader.get_pressed_keys()
        if sequence:
            self.playing_signal.emit(Chord(0, sequence[-1]).find_name())
        if self.start_time:
            seconds = 60 - (datetime.now()-self.start_time).seconds
            self.time_signal.emit(str(seconds))
            if seconds == 0:
                self.start_time=None
            if len(self.target_chords) < 4:
                self.target_chords.extend([generate_random_chord() for i in range(4-len(self.target_chords))])
                self._send_targets()
            for chord in sequence:
                if Chord(0, chord) == self.target_chords[0]:
                    self.score+=1
                    self.score_signal.emit(str(self.score))
                    self.target_chords.pop(0)
                    self._send_targets()
        else:
            self.target_chords = []
            self._send_targets()

    def _send_targets(self):
        self.target_signal.emit([utility_functions.remove_numerics(chord.name) for chord in self.target_chords])



def main():
    app = QtWidgets.QApplication(sys.argv)
        
    ui = UI()
    program_backend = ProgramBackend()

    program_backend.target_signal.connect(ui.set_target_list)
    program_backend.playing_signal.connect(ui.set_chord_label)
    program_backend.score_signal.connect(ui.set_score)
    ui.start_button.pressed.connect(program_backend.start)
    program_backend.time_signal.connect(ui.set_window_title)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()