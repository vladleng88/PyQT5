from PyQt5 import QtCore, QtWidgets
import sys
class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(MyThread, self).__init__()
        self.closeKey = False
        self.count = 1
    def run(self):
        n=10
        for i in range(n):
            self.sleep(1)
            print(self.closeKey)
            if not self.closeKey:
                self.mysignal.emit(f'iteration №{i+1} from {n}')
                self.count+=1
            else:
                break
class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        vbox = QtWidgets.QVBoxLayout()
        self.title = self.setWindowTitle('Thread window')
        self.label = QtWidgets.QLabel('Default label')
        self.btn = QtWidgets.QPushButton('Start calc')
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn)
        self.setLayout(vbox)
        self.mythread = MyThread()
        self.btn.clicked.connect(self.on_clicked_btn)
        self.mythread.started.connect(self.start_thread_dispatcher)
        self.mythread.finished.connect(self.finish_thread_dispatcher)
        self.mythread.mysignal.connect(self.mysignal_dispatcher)

    def on_clicked_btn(self):
        if not self.mythread.isRunning():
            self.mythread.start()
            self.btn.setDisabled(True)

    def start_thread_dispatcher(self):
        self.label.setText('thread is started succesfully!')

    def finish_thread_dispatcher(self):
        self.label.setText('thread finished task')
        self.btn.setDisabled(False)
        self.mythread.count = 0


    def mysignal_dispatcher(self, str):
        self.label.setText(str)
        if self.mythread.isRunning():
            print('thread is working...', str)
            print('count',self.mythread.count)
            if self.mythread.count == 3:
                self.setWindowTitle('New title')
            elif self.mythread.count == 5:
                #self.mythread.terminate()
                #self.mythread.wait(5000)
                """Закончить процесс можно и путем прерывания цикла в MyThread"""
                self.mythread.closeKey = True
        else:
            print('thread does not work', str)
if __name__ == '__main__':
    print('start QThread lesson')
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.resize(500,70)
    window.show()
    sys.exit(app.exec_())