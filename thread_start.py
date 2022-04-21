from PyQt5 import QtCore, QtWidgets
import sys
class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(MyThread, self).__init__()
    def run(self):
        for i in range(10):
            self.sleep(1)
            self.mysignal.emit(f'i = {i}')
class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        vbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Default label')
        btn = QtWidgets.QPushButton('Start calc')
        vbox.addLayout(label)
        vbox.addLayout(btn)
        self.setLayout(vbox)
        btn.clicked.connect(self.on_clicked_btn)

    def on_clicked_btn(self):
        self.

if __name__ == '__main__':
    print('start')
    app = QtWidgets.QApplication(sys.argv)