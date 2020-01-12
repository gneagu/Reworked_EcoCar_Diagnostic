import serial
import time
import ast
import cProfile
import sys
from PyQt4 import QtGui, QtCore
import mainUI

debug = 0

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

# class mythread(QtCore.QThread):
#     total = QtCore.pyqtSignal(object)
#     update = QtCore.pyqtSignal()
#
#     def __init__(self, parent, n):
#         super(mythread, self).__init__(parent)
#         self.n = n
#
#     #Put code in here
#     def run(self):
#         self.total.emit(self.n)
#         i = 0
#
#         while(i<self.n):
#             if (time.time() % 1 == 0):
#                 i += 1
#                 print(str(i))
#                 self.update.emit()


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

        self.ui.set_pushButton_2.clicked.connect(self.appinit)
        self.ui.refresh_pushButton.clicked.connect(self.appinit2)

        self.set_port_comboBox_selections()


    #Initializes seperate thread.
    def appinit(self):
        thread = worker()
        self.connect(thread, thread.signal, self.testfunc)
        thread.start()

    def port_connect(self):
        #Get data from
        COM_port = self.ui.com_port_comboBox.currentText()
        baud_rate = self.ui.baud_rate_lineEdit.text()
        portConnection = serial.Serial(COM_port, baud_rate, timeout=1)
        return(portConnection)

    #Initializes seperate thread.
    def appinit2(self):
        port = self.port_connect()
        thread = arduino_worker(port)
        self.connect(thread, thread.signal, self.testfunc)
        thread.start()

    # Find active COM ports.
    def set_port_comboBox_selections(self):
        list_of_ports = []

        ports = ["/dev/ttyACM{}".format(i) for i in range(20)]

        # print(ports)

        #See if possible to open connection on port (should mean that's the comms hub)
        for port in ports:
            try:
                portConnection = serial.Serial(port)
                print("Connect to port: {}".format(port))
                list_of_ports.append(port)
            except:
                pass
        if len(list_of_ports) == 0:
            self.ui.com_port_comboBox.addItem("No Ports Found")
        else:
            for port in list_of_ports:
                self.ui.com_port_comboBox.addItem(port)

    def testfunc(self, sigstr):
        return(sigstr)

#This is the thread that works independently on the main.
class worker(QtCore.QThread):
    def __init__(self, list_of_variables):
        QtCore.QThread.__init__(self, parent = app)
        self.signal = QtCore.SIGNAL("signal")

    def run(self):
        time.sleep(5)
        for i in range(5):
            time.sleep(3)
            # self.ui.com_port_comboBox.addItme(i)
            print("Loop 1")
        print("IN THREAD")
        self.emit(self.signal, "i from thread")

    def _get_data_from_arduino(self, list_of_variables):
        pass

class arduino_worker(QtCore.QThread):
    def __init__(self, connection):
        QtCore.QThread.__init__(self, parent = app)
        self.signal = QtCore.SIGNAL("signal")
        self.connection = connection
        # self.list_of_variables = list_of_variables
        self.connection = connection


    def run(self):
        self._get_data_from_arduino(self.connection)
        self.emit(self.signal, "i from thread")

    def _get_data_from_arduino(self, connection):
        self.connection.flush()

        print("Sending value: T")
        self.connection.write(b"T")

        # time.sleep(1)
        self.sleep(1)

        msg = self.connection.readline();
        print(msg)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    # QtCore.QTimer.singleShot(0, window.appinit)
    sys.exit(app.exec_())

# import glob
#
# # ports = ['COM%s' % (i + 1) for i in range(256)]
# ports = glob.glob('/dev/tty[A-Za-z]*')
#
# for i in ports:
#     print(i)

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
