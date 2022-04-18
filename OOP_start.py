import sys
from PyQt5 import QtWidgets, QtCore

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        vBox = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel('label')
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.btnQuit = QtWidgets.QPushButton('Close btn')
        vBox.addWidget(self.label)
        vBox.addWidget(self.btnQuit)
        self.setLayout(vBox)
        self.btnQuit.clicked.connect(QtWidgets.qApp.quit)
        self.title = self.setWindowTitle('OOP_start')
class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        vBox = QtWidgets.QVBoxLayout()
        self.win = MyWindow()
        #self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.btnQuit = QtWidgets.QPushButton('Change label')
        vBox.addWidget(self.win)
        vBox.addWidget(self.btnQuit)
        self.setLayout(vBox)
        self.btnQuit.clicked.connect(self.onButtonChange)
        self.title = self.setWindowTitle('OOP_start')
    def onButtonChange(self):
        self.win.label.setText('New Label')
        self.btnQuit.setDisabled(True)



if __name__ == '__main__':
    print('Start OOP_start.py...')
    app = QtWidgets.QApplication(sys.argv)
    window = MyDialog()
    window.resize(500, 70)
    window.show()
    sys.exit(app.exec_())
