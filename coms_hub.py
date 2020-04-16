import serial
import time
import ast
import cProfile
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from gui import mainUI2
import sys

debug = 0

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.numOfVars = 0
        self.buttons = []
        self.ui = mainUI2.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.set_pushButton_2.clicked.connect(self.set_data_view_variables)
        self.ui.refresh_pushButton.clicked.connect(self.appinit)

        # This searches active com ports, and adds them to the comboBox
        self.set_port_comboBox_selections()

    # Initializes seperate thread.
    def appinit(self):
        thread = Worker(connection)
        self.connect(thread, thread.signal, self.testfunc)

        # Get dict of values and data types from coms board
        thread.start()

    # Taking user selection, opens a conenction on specified port.
    def port_connect(self):
        COM_port = self.ui.com_port_comboBox.currentText()
        baud_rate = self.ui.baud_rate_lineEdit.text()
        portConnection = serial.Serial(COM_port, baud_rate, bytesize=8, parity='N', stopbits=1)
        return(portConnection)


    def get_value_name_dict(self, serial):
        ser = serial
        dict_value_type = {}

        # Send command to get number of variables from the board.
        ser.write(b'GET *VCOUNT\n')

        # Number of variables is returned as a bit array. Ex// b'VAL *VCOUNT 11\n'
        numOfVars = ser.readline().decode(encoding='ascii').split(" ")[-1]

        # Sending "GET *VN#x" where x is number of variable returns variable name and var type.
        for i in range(int(numOfVars)):
            #Create string and convert to bit array.
            bitString = "GET *VN#{}\n".format(i)
            ser.write(bitString.encode(encoding='ascii'))
            time.sleep(0.1)

            # Value list returns as ["command sent", "variable type", "variable name"]
            # Variable name and type returned Ex//
            valueList = ser.readline().decode(encoding='ascii').split(" ")

            # Ex// ["VAL", "*VN#1:F", "MOT_I"]
            valueName = valueList[-1]
            valueType = valueList[1].split(":")[-1]

            # As of Python 3.7, dicts are ordered.
            dict_value_type[valueName] = valueType

        return dict_value_type

    # Recieves a dict with new data from coms board, and sets appropriate columns in gui.
    def set_data_view_variables(self):
        self.connection = self.port_connect()
        self.dict_value_type = self.get_value_name_dict(self.connection)

        self.thread = DataCollectionThread(self.connection, self.dict_value_type)
        self.thread.new_data_dict.connect(self.update_data_view)
        self.thread.start()





    # Initializes seperate thread.
    # def appinit2(self):
    #     self.ui.tableWidget.insertColumn(0)
    #     self.ui.tableWidget.insertColumn(1)
    #     self.ui.tableWidget.insertColumn(2)
    #
        # Given dict with variables, query board for value and upgate gui
        #
        # for i in range(self.numOfVars):
        #     #Get value of variable
        #     name = "X"
        #
        #     self.ui.tableWidget.insertRow(i)
        #
        #     #Create text name
        #     self.ui.tableWidget.setItem(i, 0,QtGui.QTableWidgetItem(name))
        #
        #     #Create Button to push to tableWidget
        #     self.buttons.append(QtGui.QPushButton(self.ui.tableWidget))
        #     self.buttons[i].setText("Graph".format(i))
        #
        #     #Set cell as text, and button
        #     self.ui.tableWidget.setCellWidget(i, 2, self.buttons[i])


    # Find and add active COM ports to the gui combobox.
    def set_port_comboBox_selections(self):
        list_of_ports = []

        if sys.platform.startswith('linux'):
            ports = ["/dev/ttyACM{}".format(i) for i in range(20)]
        elif sys.platform.startswith('win'):
            ports = ['COM{}'.format(i + 1) for i in range(256)]

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
        print("FInally here")
        print(data)
        pass

# This thread works independently on the main.
# This one gets each value from the
# https://www.youtube.com/watch?v=eYJTcLBQKug
# https://wiki.python.org/moin/PyQt5/Threading%2C_Signals_and_Slots
class DataCollectionThread(QThread):

    new_data_dict = pyqtSignal(dict)

    def __init__(self, connection, value_dict):
        QThread.__init__(self, parent = app)
        # print(connection)
        self.threadactive = True
        self.connection = connection
        self.value_dict = value_dict

    #Self.emit will emit data back to main thread.
    def run(self):
        print("Her")
        print(self.connection)

        self.new_data_dict.emit({})

    def __del__(self):
        self.wait()

    # Function to kill a thread
    # https://stackoverflow.com/questions/51135444/how-to-kill-a-running-thread
    def stop(self):
        self.threadactive = False
        self.wait()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
