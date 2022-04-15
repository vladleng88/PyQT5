from PyQt5 import QtCore
from PyQt5 import QtWidgets
import sys
print(QtCore.PYQT_VERSION_STR)
print(QtCore.QT_VERSION_STR)
app = QtWidgets.QApplication(sys.argv)
print(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle('First QT programm')
btnQuit = QtWidgets.QPushButton("Close window")
window.resize(300,70)
label = QtWidgets.QLabel('<center>Hello, world</center>')
vBox = QtWidgets.QVBoxLayout()
vBox.addWidget(label)
vBox.addWidget(btnQuit)
window.setLayout(vBox)

btnQuit.clicked.connect(app.quit)
window.show()
sys.exit(app.exec_())