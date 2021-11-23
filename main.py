import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow, QHBoxLayout, QPushButton, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal
import sounddevice as sd
import numpy as np
from note_analyzer import probability_of_notes, most_likely_notes, note_dict

class UI(QMainWindow):

    record_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.button = QPushButton('Start')
        self.button.clicked.connect(lambda checked : self.record_signal.emit())
        self.setCentralWidget(self.button)
        self.show()

    def set_label(self, text):
        print('Set')
        self.button.setText(text)
        self.record_signal.emit()

class ProgramBackend(QObject):

    label_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def record_and_analyze(self):
        print('Analyze')
        fs = 44100  # Sample rate
        seconds = 0.2  # Duration of recording

        recording_data = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        recording_data = np.average(recording_data, axis=1)
        recording_data = recording_data/np.max(recording_data)
        keys, probability = probability_of_notes(fs, recording_data)
        triad = most_likely_notes(keys, probability, n=3)
        self.label_signal.emit(str([note_dict[x] for x in triad]))


def main():
    app = QtWidgets.QApplication(sys.argv)
        
    ui = UI()
    program_backend = ProgramBackend()

    ui.record_signal.connect(program_backend.record_and_analyze)
    program_backend.label_signal.connect(ui.set_label)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()