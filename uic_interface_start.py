from PyQt5 import QtWidgets, uic
import sys
uiPath = r'Ui/testinterface.ui'
#app = QtWidgets.QApplication(sys.argv)
#window = uic.loadUi(uiPath)
#window.btnQuit.clicked.connect(app.quit)
#window.show()
#sys.exit(app.exec_())
class MyUiWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyUiWindow, self).__init__()
        #self.__pathUi = pathUi
        uic.loadUi('Ui/testinterface.ui', self)
        self.btnQuit.clicked.connect(QtWidgets.qApp.quit)
if __name__ == '__main__':
    print('start')
    app = QtWidgets.QApplication(sys.argv)
    window = MyUiWindow()
    window.show()
    sys.exit(app.exec_())
