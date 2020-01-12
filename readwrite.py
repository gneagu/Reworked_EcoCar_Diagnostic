import serial
import time
import ast
import cProfile
import sys
from PyQt4 import QtGui, QtCore
import mainUI

debug = 0

def determinePorts():
    #List of possible ports.
    ports = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3']

    #See if possible to open connection on port (should mean that's the comms hub)
    for port in ports:
        try:
            portConnection = serial.Serial(port, 9600, timeout=1)
            print("Connect to port: {}".format(port))
            return(portConnection)
        except:
            pass

    print("No ports available. Ending program.\n")
    sys.exit()

class mythread(QtCore.QThread):
    total = QtCore.pyqtSignal(object)
    update = QtCore.pyqtSignal()

    def __init__(self, parent, n):
        super(mythread, self).__init__(parent)
        self.n = n

    def run(self):
        self.total.emit(self.n)
        i = 0

        while(i<self.n):
            if (time.time() % 1 == 0):
                i += 1
                print(str(i))
                self.update.emit()


def main():
    ard = determinePorts()
    ard.flush()

    print("Sending value: T")
    ard.write(b"T")

    time.sleep(1)

    msg = ard.readline();

    if (debug == 1) :
        print("Message reeceived: ")
        print(msg)


    ard.close()

    print(ast.literal_eval(msg.decode()))


class TestWindow(QtGui.QMainWindow):


    def __init__(self):
        super(TestWindow, self).__init__()
        self.ui = mainUI.Ui_Dialog()
        self.ui.setupUi(self)
        QtCore.QTimer.singleShot(0, self.appinit)

        # self.mythread.total.connect(self.setMaximum)
        # self.mythread.update.connect(self.update)
        # self.mythread.finished.connect(self.close)
        #
        # self.n = 0
        # self.thread.start()
    def appinit(self):
        thread = worker()
        self.connect(thread, thread.signal, self.testfunc)
        thread.start()

    def testfunc(self, sigstr):
        print(sigstr)

    # def update(self):
    #     self.n += 1
    #     print(self.n)
    #     self.setValue(self.n)

class worker(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self, parent = app)
        self.signal = QtCore.SIGNAL("signal")

    def run(self):
        time.sleep(5)
        print("IN THREAD")
        self.emit(self.signal, "i from thread")



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # thread = AThread()
    # thread.finished.connect(app.exit)
    window = TestWindow()
    window.show()
    # QtCore.QTimer.singleShot(0, window.appinit)
    # thread.start()
    sys.exit(app.exec_())

# import serial
# import time
# import ast
# import cProfile
# import sys
# from PyQt4 import QtGui, QtCore
# import mainUI
#
# debug = 0
#
# def determinePorts():
#     #List of possible ports.
#     ports = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3']
#
#     #See if possible to open connection on port (should mean that's the comms hub)
#     for port in ports:
#         try:
#             portConnection = serial.Serial(port, 9600, timeout=1)
#             print("Connect to port: {}".format(port))
#             return(portConnection)
#         except:
#             pass
#
#     print("No ports available. Ending program.\n")
#     sys.exit()
#
#
#
# def main():
#     ard = determinePorts()
#     ard.flush()
#
#     print("Sending value: T")
#     ard.write(b"T")
#
#     time.sleep(1)
#
#     msg = ard.readline();
#
#     if (debug == 1) :
#         print("Message reeceived: ")
#         print(msg)
#
#
#     ard.close()
#
#     print(ast.literal_eval(msg.decode()))
#
#
# class TestWindow(QtGui.QMainWindow):
#
#     signalStatus = QtCore.pyqtSignal(str)
#
#     def __init__(self):
#         super(TestWindow, self).__init__()
#         self.ui = mainUI.Ui_Dialog()
#         self.ui.setupUi(self)
#         self.createWorkerThread()
#         self._connectSignals()
#
#     def _connectSignals(self):
#         self.ui.set_pushButton_2.clicked.connect(self.gui.updateStatus)
#
#     def createWorkerThread(self):
#         self.worker = WorkerObject()
#         self.worker_thread = QtCore.QThread()
#         self.worker.moveToThread(self.worker_thread)
#         self.worker_thread.start()
#
#         self.worker.signalStatus.connect(self.gui.updateStatus)
#         self.ui.debug_pushButton_5.connect(self.worker.startWork)
#
#     @QtCore.pyqtSlot(str)
#     def updateStatus(self, status):
#         self.label_2.setText(status)
#
# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     # thread = AThread()
#     # thread.finished.connect(app.exit)
#     window = TestWindow()
#     window.show()
#     # thread.start()
#     sys.exit(app.exec_())
#

# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     Dialog = QtGui.QDialog()
#     ui = Ui_Dialog()
#     ui.setupUi(Dialog)
#     Dialog.show()
#
# if __name__ == "__main__":
#     print("HERe")
#     if debug == 0:
#         print("HER")
#         main()
#     elif debug == 1:
#         cProfile.run('main()')

# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     Dialog = QtGui.QDialog()
#     ui = Ui_Dialog()
#     ui.setupUi(Dialog)
#     Dialog.show()
#
# if __name__ == "__main__":
#     print("HERe")
#     if debug == 0:
#         print("HER")
#         main()
#     elif debug == 1:
#         cProfile.run('main()')
