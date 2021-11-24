from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout

class FadingListWidget(QWidget):

    def __init__(self, len=4):
        super().__init__()
        self.len = len
        self.layout = QVBoxLayout(self)
        self.labels = [QLabel('') for i in range(len)]
        for i, label in enumerate(self.labels):
            label.setStyleSheet(f'color: rgba(0,0,0,{(len-i)/(len+1)}); font-size: 36pt')
            label.setAlignment(QtCore.Qt.AlignLeft)
            self.layout.addWidget(label)
        self.contents = []

    def set_list(self, strings: list):
        self.contents = strings
        self._refresh_labels()

    def _refresh_labels(self):
        for i, label in enumerate(self.labels):
            x = self.contents[i] if i < len(self.contents) else ''
            label.setText(x)
