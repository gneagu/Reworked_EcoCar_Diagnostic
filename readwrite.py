import serial
import time
import ast
import cProfile
import sys
from PyQt4 import QtGui, QtCore
import mainUI2

debug = 0

def main():
    ard = determinePorts()
    ard.flush()

    # print("Sending value: T")
    # ard.write(b"T")
    #
    # time.sleep(1)
    #
    # msg = ard.readline();
    #
    # if (debug == 1) :
    #     print("Message reeceived: ")
    #     print(msg)
    #
    #
    # ard.close()
    #
    # print(ast.literal_eval(msg.decode()))


class TestWindow(QtGui.QMainWindow):


    def __init__(self):
        super(TestWindow, self).__init__()
        self.numOfVars = 7
        self.buttons = []
        self.ui = mainUI2.Ui_Dialog()
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

    def get_all_variables(self, connection):
        #get number of variables from comms hub
        pass

    #Initializes seperate thread.
    def appinit2(self):
        self.ui.tableWidget.insertColumn(0)
        self.ui.tableWidget.insertColumn(1)
        self.ui.tableWidget.insertColumn(2)

        #Get number of variables

        for i in range(self.numOfVars):
            #Get value of variable
            name = "X"

            self.ui.tableWidget.insertRow(i)

            #Create text name
            self.ui.tableWidget.setItem(i, 0,QtGui.QTableWidgetItem(name))

            #Create Button to push to tableWidget
            self.buttons.append(QtGui.QPushButton(self.ui.tableWidget))
            self.buttons[i].setText("Graph".format(i))

            #Set cell as text, and button
            self.ui.tableWidget.setCellWidget(i, 2, self.buttons[i])



        # for i in range(self.numOfVars):
        #     self.ui.tableWidget.insertColumn(i)
        #     self.ui.tableWidget.setItem(0, i,QtGui.QTableWidgetItem("hello"))
        #     # self.ui.tableWidget.setCellWidget(0,i, btn)
        #
        #w
        #     #Create Button to push to tableWidget
        #     self.buttons.append(QtGui.QPushButton(self.ui.tableWidget))
        #     # "btn{}".append(i) = QtGui.QPushButton(self.ui.tableWidget)
        #     self.buttons[i].setText("PUSH")
        #
        #     #Set cell as text, and button
        #     self.ui.tableWidget.setItem(2, i,QtGui.QTableWidgetItem("hello"))
        #     self.ui.tableWidget.setCellWidget(2, i, self.buttons[i])

        # pass

        # self.ui.tableView.append([1,1,1,1,1])
        # sele.tableView.model().laoyoutChanged.emit()
        # print("Success")
        # rowPosition = self.ui.tableView.rowCount()
        # table.insertRow(rowPosition)
        #
        # self.ui.tableView.setItem(rowPorition, 0, QtGui.QTableWidgetItem("text1"))
        # port = self.port_connect()
        # thread = arduino_worker(port)
        # self.connect(thread, thread.signal, self.testfunc)
        # thread.start()

    # Find and add active COM ports to the gui combobox.
    def set_port_comboBox_selections(self):
        list_of_ports = []
        ports = ["/dev/ttyACM{}".format(i) for i in range(20)]

        #See if possible to open connection on port (should only open if theres an active device)
        for port in ports:
            try:
                portConnection = serial.Serial(port)
                print("Connect to port: {}".format(port))
                list_of_ports.append(port)
            except:
                pass

        #Check if any ports are available.
        if len(list_of_ports) == 0:
            self.ui.com_port_comboBox.addItem("No Ports Found")
            self.ui.set_pushButton_2.setEnabled(False);
        else:
            for port in list_of_ports:
                self.ui.com_port_comboBox.addItem(port)

    def testfunc(self, sigstr):
        return(sigstr)

    def update_data_view(self, data):
        pass

#This is the thread that works independently on the main.
class worker(QtCore.QThread):
    def __init__(self, list_of_variables):
        QtCore.QThread.__init__(self, parent = app)
        self.signal = QtCore.SIGNAL("signal")

    #Self.emit will emit data back to main thread.
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

    def run(self):
        self._get_data_from_arduino(self.connection)
        self.emit(self.signal, "i from thread")

    def __del__(self):
        self.wait()

    def _get_data_from_arduino(self, connection):
        self.connection.flush()

        while (1 == 1):

            print("Sending value: T")
            self.connection.write(b'T')

            # self.usleep(2000)

            msg = self.connection.readline();

            print(msg)
            print("Finish")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    # QtCore.QTimer.singleShot(0, window.appinit)
    sys.exit(app.exec_())


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
#s
