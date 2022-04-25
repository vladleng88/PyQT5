from PyQt5 import QtCore, QtWidgets
import sys
class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(object)
    quitsignal = QtCore.pyqtSignal(bool)
    def __init__(self, id):
        super(MyThread, self).__init__()
        self.closeKey = False
        self.__id = id
    def run(self):
        n=10
        for i in range(1, 6000000):
            pass
        for i in range(n):
            self.sleep(int(3*self.__id/5))
            if not self.closeKey:
                self.mysignal.emit({'id': self.__id, 'value':i})
                #QtWidgets.qApp.processEvents()
            else:
                break
        self.quitsignal.emit(True)
    def getId(self):
        return self.__id

class MyThread1(QtCore.QThread):
    s1 = QtCore.pyqtSignal(str)
    def __init__(self):
        super(MyThread1, self).__init__()
        self.code = 'secretCode'
    def run(self):
        """ Каждый поток может иметь свой собственный цикл обработки сигналов,
            который запускается с помощью метода exec_()"""
        self.exec_()
    def generateSignal(self):
        i = 0
        for i in range(1, 600000):
            pass
        self.s1.emit(self.code+'i={}'.format(i))

class MyThread2(QtCore.QThread):
    s2 = QtCore.pyqtSignal(str)
    def __init__(self):
        super(MyThread2, self).__init__()
    def run(self):
        """ Каждый поток может иметь свой собственный цикл обработки сигналов,
            который запускается с помощью метода exec_()"""
        self.exec_()
    def changeStr(self, str):
        self.s2.emit('str changed. '+str)

from functools import partial

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        vbox = QtWidgets.QVBoxLayout()
        self.title = self.setWindowTitle('Thread window')
        self.__N = 20
        self.myLabelList = [QtWidgets.QLabel(f'Process № {i}:') for i in range(self.__N)]

        self.btn = QtWidgets.QPushButton('Start calc')
        self.btnStop = QtWidgets.QPushButton('Stop calc')
        self.btnQuit = QtWidgets.QPushButton('Quit app')
        self.btnClear = QtWidgets.QPushButton('Clear view')
        self.btn1 = QtWidgets.QPushButton('Сгенерировать сигнал')
        for label in self.myLabelList:
            vbox.addWidget(label)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.btnStop)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btnQuit)
        vbox.addWidget(self.btnClear)
        self.setLayout(vbox)

        self.myThreadList = [MyThread(i) for i in range(self.__N)]
        self.btn.clicked.connect(self.on_clicked_btn)
        self.btnStop.clicked.connect(self.on_clicked_btnStop)
        self.btnClear.clicked.connect(self.on_clicked_btnClear)
        self.btnQuit.clicked.connect(self.closeEvent)

        for thread in self.myThreadList:
            thread.started.connect(partial(self.start_thread_dispatcher, thread.getId()))
            thread.mysignal.connect(self.mysignal_dispatcher)
            thread.quitsignal.connect(partial(self.quit_thread_dispatcher, thread.getId()))
            thread.finished.connect(self.finished_thread_dispatcher)
    """
        self.process1 = MyThread1()
        self.process2 = MyThread2()
        self.process1.start()
        self.process2.start()

        self.btn1.clicked.connect(self.process1.generateSignal)
        self.process1.s1.connect(self.process2.changeStr)
        self.process2.s2.connect(self.exchange_between_processes)
    """
    def finished_thread_dispatcher(self):
        quitKey = True
        for thread in self.myThreadList:
           if thread.isRunning():
               quitKey = False
        if quitKey:
           self.btn.setDisabled(False)
    def exchange_between_processes(self, str):
        print('exchange_between_processes is done')
        print('str received:', str)

    def on_clicked_btn(self):
        self.on_clicked_btnClear()
        for thread in self.myThreadList:
            thread.start()
            QtWidgets.qApp.processEvents()
        self.btn.setDisabled(True)

    def on_clicked_btnStop(self):
        for thread in self.myThreadList:
            if thread.isRunning():
                thread.terminate()
                thread.wait(5000)
        self.btn.setDisabled(False)


    def on_clicked_btnClear(self):
        for i,label in enumerate(self.myLabelList):
            label.setText(f'Process № {i}:')

    def start_thread_dispatcher(self, id):
        text = self.myLabelList[id].text()
        self.myLabelList[id].setText(text+f'thread {id} is started succesfully!')

        #self.mythread.closeKey = False
        #self.label.setText('thread is started succesfully!')

    def quit_thread_dispatcher(self, id):
        self.myLabelList[id].setText('Process № {}: The work is done!'.format(id))

    def mysignal_dispatcher(self, dictRes):
        id = dictRes['id']
        self.myLabelList[id].setText('Process № {}: iter= {}'.format(dictRes['id'], dictRes['value']))
        QtWidgets.qApp.processEvents()

        """
        if self.mythread.isRunning():
            print('thread is working...', str)
            print('count',self.mythread.count)
            if self.mythread.count == 3:
                self.setWindowTitle('New title')
            elif self.mythread.count == 5:
                #self.mythread.terminate()
                #self.mythread.wait(5000)
                #Закончить процесс можно и путем прерывания цикла в MyThread
                self.mythread.closeKey = True
        else:
            print('thread does not work', str)"""

    def eventSignalDispatcher(self, eventStr):
        print('log:', eventStr)

    def closeEvent(self, event):
        for thread in self.myThreadList:
            if thread.isRunning():
                print('thread', thread, 'is terminating...')
                thread.terminate()
                thread.wait(5000)
                if thread.isRunning():
                    print('thread'+str(thread)+' still work...')
                else:
                    print('thread'+str(thread)+' is stopped')
        event.accept()
        #if not self.
if __name__ == '__main__':
    print('start QThread lesson')
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MyWindow()
        window.resize(500,70)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)