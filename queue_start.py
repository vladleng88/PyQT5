from PyQt5 import QtWidgets, QtCore
import queue
import sys
class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(int, int)
    def __init__(self, id, queue):
        super(MyThread, self).__init__()
        self.__id = id
        self.__queue = queue
    def run(self):
        while True:
            task = self.__queue.get(block = True)
            self.mysignal.emit(self.__id, task)
            self.sleep(task+1)
            self.__queue.task_done()
import time
class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.queue = queue.Queue()
        vbox = QtWidgets.QVBoxLayout()
        self.btn = QtWidgets.QPushButton('Раздать задание')
        self.btnStop = QtWidgets.QPushButton('Прервать расчет')
        self.label = QtWidgets.QLabel('Length of queue is {}'.format(self.queue.qsize()))
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.btnStop)
        self.setLayout(vbox)
        self.threads = []
        for i in range(3):
            thread = MyThread(i, self.queue)
            self.threads.append(thread)
            thread.mysignal.connect(self.printResults, QtCore.Qt.QueuedConnection)
        self.btn.clicked.connect(self.add_queue)
        self.btnStop.clicked.connect(self.stop_queue)

    def stop_queue(self):
        for thread in self.threads:
            if thread.isRunning():
                thread.terminate()
                thread.wait(500)
        try:
            #for elem in range(self.queue.qsize()):
            while True:
                self.queue.get(False)
        except queue.Empty:
            print('Empty queue')
        self.label.setText('The length of queue is ' + str(self.queue.qsize()))
        self.btn.setDisabled(False)
    def add_queue(self):
        for i in range(10):
            self.queue.put(i)
        self.label.setText('The length of queue is ' + str(self.queue.qsize()))
        QtWidgets.qApp.processEvents()
        #time.sleep(1)
        self.btn.setDisabled(True)
        for i in range(len(self.threads)):
            self.threads[i].start()

    def printResults(self, id, task):
        self.label.setText('The length of queue is ' + str(self.queue.qsize()))
        QtWidgets.qApp.processEvents()
        print('thread id = {} finished work. res = {}'.format(id, task))
        quitKey = True
        for thread in self.threads:
            if thread.isRunning():
                quitKey=False
        if self.queue.qsize()==0:
            self.btn.setDisabled(False)
if __name__=='__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MyWindow()
        window.setWindowTitle('Using queue module')
        window.resize(500, 50)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
