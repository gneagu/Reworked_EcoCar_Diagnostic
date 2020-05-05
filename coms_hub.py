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
        self.time_delay = 0.2
        self.ui = mainUI2.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.set_pushButton_2.clicked.connect(self.set_data_view_variables)
        self.ui.refresh_pushButton.clicked.connect(self.kill_tread)

        # This searches active com ports, and adds them to the comboBox
        self.set_port_comboBox_selections()

    # # Initializes seperate thread.
    # def appinit(self):
    #     thread = Worker(connection)
    #     self.connect(thread, thread.signal, self.testfunc)
    #
    #     # Get dict of values and data types from coms board
    #     thread.start()
    def kill_tread(self):
        self.thread.stop()

    # Taking user selection, opens a conenction on specified port.
    def port_connect(self):
        self.time_delay = self.ui.time_spinBox.value() / 1000
        COM_port = self.ui.com_port_comboBox.currentText()
        baud_rate = self.ui.baud_rate_lineEdit.text()
        portConnection = serial.Serial(COM_port, baud_rate, bytesize=8, parity='N', stopbits=1)
        return(portConnection)

    def add_columns(self, numOfVars):
        #Add columns here to table.
        self.ui.tableWidget.insertColumn(0)
        self.ui.tableWidget.insertColumn(1)
        self.ui.tableWidget.insertColumn(2)

        Given dict with variables, query board for value and upgate gui

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

    def get_value_name_dict(self, serial):
        ser = serial
        dict_value_type = {}

        # Send command to get number of variables from the board.
        ser.write(b'GET *VCOUNT\n')

        # Number of variables is returned as a bit array. Ex// b'VAL *VCOUNT 11\n'
        numOfVars = ser.readline().decode(encoding='ascii').split(" ")[-1]
        self.numOfVars = numOfVars

        #Set the columns here.
        self.add_columns(numOfVars)

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

    # Recieves a dict with new data from coms board, and sends to worker thread.
    # Then starts worker thread.
    def set_data_view_variables(self):
        self.connection = self.port_connect()
        self.dict_value_type = self.get_value_name_dict(self.connection)
        print(self.dict_value_type)

        #Should call function here to populate the rows and columns.

        #Launch seperate thread to get variable from coms hub.
        self.thread = DataCollectionThread()
        self.thread.new_data_dict.connect(self.update_data_view)
        # https://stackoverflow.com/questions/45668961/send-data-to-qthread-when-in-have-changes-in-gui-windows-pyqt5
        self.thread.setup(self.dict_value_type, self.connection, self.time_delay)
        self.thread.start()




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

    # Emmited data from DataCollectionThread come here.
    # This function updates the values in the main window.
    def update_data_view(self, data):
        print("FInally here")
        print(data)
        pass

# This thread works independently on the main.
# This one gets each value from the
# https://www.youtube.com/watch?v=eYJTcLBQKug
# https://wiki.python.org/moin/PyQt5/Threading%2C_Signals_and_Slots
class DataCollectionThread(QThread):

    #This dict is sent as a signal from the thread that started it.
    new_data_dict = pyqtSignal(dict)
    # print(variable_dict)

    def __init__(self):
        QThread.__init__(self, parent = app)
    #     # print(connection)
        self.threadactive = False
        self.connection = 0
        self.value_dict = {}

    def setup(self, dict_value_names, serial_con, time_delay):
        self.connection = serial_con
        self.value_dict = dict_value_names
        self.time_delay = time_delay

    # This is the main function of the thread. Purpose is to query coms hub
    # for variable from dictionary of value names and types.
    def run(self):

        print(self.value_dict)
        values_read = {}

        #From the dictionary, get value name, and expected value type.
        while True:
            for name, type in self.value_dict.items():

                #Command to get variable
                bitString = "GET {}".format(name)
                self.connection.write(bitString.encode(encoding='ascii'))

                # Read value from Coms hub
                value = self.connection.readline().decode(encoding='ascii').split(" ")[-1]
                if type == 'F':
                    values_read[name] = float(value)
                else:
                    values_read[name] = value

            self.new_data_dict.emit(values_read)
            time.sleep(self.time_delay)

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







    # Initializes seperate thread.
    # def appinit2(self):
        # self.ui.tableWidget.insertColumn(0)
        # self.ui.tableWidget.insertColumn(1)
        # self.ui.tableWidget.insertColumn(2)
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
