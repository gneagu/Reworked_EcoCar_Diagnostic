import serial
import serial.tools.list_ports
import time
import ast
import cProfile
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from gui import mainUI2, trial
import sys
import random
from functools import partial

debug = 1

# Not a mainwindow (Is a dialog), so need to inherit from it
# https://stackoverflow.com/questions/29303901/attributeerror-startqt4-object-has-no-attribute-accept
class EventWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EventWindow, self).__init__(parent)
        self.ui2 = trial.Ui_Dialog()
        self.ui2.setupUi(self)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.numOfVars = 0
        self.buttons = []
        self.time_delay = 0.2
        self.connection = 0
        self.ui = mainUI2.Ui_Dialog()
        self.ui.setupUi(self)
        self.dialog = EventWindow(self)
        self.dict_value_type = {}
        self.dialogs = {}


        self.ui.set_pushButton_2.clicked.connect(self.set_data_view_variables)
        self.ui.refresh_pushButton.clicked.connect(self.set_port_comboBox_selections)
        self.ui.version_pushButton_4.clicked.connect(self.show_trial_screen)

        # This searches active com ports, and adds them to the comboBox
        self.set_port_comboBox_selections()

    def show_trial_screen(self):
        self.thread.register()

        self.dialog.show()

    def kill_tread(self):
        self.thread.stop()

    # Taking user selection, opens a conenction on specified port.
    def port_connect(self):
        self.time_delay = self.ui.time_spinBox.value() / 100
        COM_port = self.ui.com_port_comboBox.currentText()
        baud_rate = self.ui.baud_rate_lineEdit.text()

        #TODO: Change this. (opening connection on same port twice crashes program)
        #But we can change com ports.
        if debug == 0:

            if not self.connection:
                print("MAKING A NEW CONNECTION")

                portConnection = serial.Serial(COM_port, baud_rate, bytesize=8, parity='N', stopbits=1)
                self.connection = portConnection

        else:
            pass

    # Remove rows and columns. (Needs to be reversed since removing column at start
    # remaps proceeding)
    def empty_table_widget(self):
        totalColumns = self.ui.tableWidget.columnCount()
        totalRows = self.ui.tableWidget.rowCount() 

        for index in range(totalRows):
            self.ui.tableWidget.removeRow(index)

        for index in range(totalColumns)[::-1]:
            self.ui.tableWidget.removeColumn(index)


    # https://stackoverflow.com/questions/40815730/how-to-add-and-retrieve-items-to-and-from-qtablewidget
    def add_columns(self, numOfVars):
        self.empty_table_widget()

        #Add columns here to table.
        self.ui.tableWidget.insertColumn(0)
        self.ui.tableWidget.insertColumn(1)
        self.ui.tableWidget.insertColumn(2)

        self.buttons = []

        i = 0
        print(self.dict_value_type)

        for name in self.dict_value_type:
        # for i in range(int(self.numOfVars)):
            self.ui.tableWidget.insertRow(i)

            #Create Button to push to tableWidget
            self.buttons.append(QtWidgets.QPushButton(self.ui.tableWidget))
            self.buttons[i].setText("Graph".format(i))
            # self.buttons[i].setToolTip(str(name))
            self.buttons[i].setToolTip(name)

            #Set cell as button
            self.ui.tableWidget.setCellWidget(i, 2, self.buttons[i])
            self.buttons[i].clicked.connect(partial(self.on_pushButton_clicked, self.buttons[i]))

            i = i + 1

    # https://stackoverflow.com/questions/36823841/pyqt-getting-which-button-called-a-specific-function
    # Each graph button in tablewidget has the tooltip set as corresponding variable name.
    # Simply get variable name and open graph window/register with expected variable.
    def on_pushButton_clicked(self, button):
        print("CLICKED")
        variable_name = button.toolTip()
        try:
            print("Tooltup")
            print(variable_name)
        except:
            print("Failed tooltip")

        # Check if window is there, otherwise do not open window
        if variable_name not in self.dialogs:
            self.newWindow = GraphWindow(self.thread, variable_name)

            self.dialogs[variable_name] = self.newWindow
            self.thread.register(self.dialogs[variable_name], variable_name)

        self.dialogs[variable_name].show()


    def get_value_name_dict(self, serial):
        ser = self.connection
        dict_value_type = {}

        if debug == 0:

            # Wipe serial connection buffer
            ser.flushInput()
            ser.flushOutput()

            # Send command to get number of variables from the board.
            ser.write(b'GET *VCOUNT\n')

            # Number of variables is returned as a bit array. Ex// b'VAL *VCOUNT 11\n'
            numOfVars = ser.readline().decode(encoding='ascii').split(" ")[-1]
            self.numOfVars = numOfVars

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

        else:
            self.numOfVars = 6
            dict_value_type = generate_random_data()
            print(dict_value_type)

        return dict_value_type

    # Disable buttons after com port selected (Must restart app to choose different com port)
    def disable_com_selections(self):
        self.ui.set_pushButton_2.setEnabled(False)
        self.ui.refresh_pushButton.setEnabled(False)
        self.ui.baud_rate_lineEdit.setEnabled(False)
        self.ui.direct_checkBox.setEnabled(False)
        self.ui.com_port_comboBox.setEnabled(False)

    # Recieves a dict with new data from coms board, and sends to worker thread.
    # Then starts worker thread.
    def set_data_view_variables(self):
        self.disable_com_selections()
        # self.connection = self.port_connect()
        self.port_connect()
        self.dict_value_type = self.get_value_name_dict(self.connection)

        #Set the columns here.
        self.add_columns(self.numOfVars)

        #Launch seperate thread to get variable from coms hub.
        self.thread = DataCollectionThread()
        self.thread.new_data_dict.connect(self.update_data_view)
        # https://stackoverflow.com/questions/45668961/send-data-to-qthread-when-in-have-changes-in-gui-windows-pyqt5
        self.thread.setup(self.dict_value_type, self.connection, self.time_delay)
        self.thread.start()

    # Find and add active COM ports to the gui combobox.
    def set_port_comboBox_selections(self):
        list_of_ports = []

        if debug == 0:
            # Much nice way to get com ports
            # https://pyserial.readthedocs.io/en/latest/tools.html
            port_names = list(serial.tools.list_ports.comports(include_links=False))

            for p in port_names:
                list_of_ports.append(p.device)

            #Check if any ports are available.
            if len(list_of_ports) == 0:
                self.ui.com_port_comboBox.addItem("No Ports Found")
                self.ui.set_pushButton_2.setEnabled(False);
            else:
                self.ui.set_pushButton_2.setEnabled(True);
                for port in list_of_ports:
                    self.ui.com_port_comboBox.addItem(port)
        else:
            self.ui.set_pushButton_2.setEnabled(True);
            self.ui.com_port_comboBox.addItem("DEBUG")


    # Emmited data from DataCollectionThread comes here.
    # This function updates the values in the main window.
    def update_data_view(self, data):
        i = 0

        for (name, value) in data.items():
            self.ui.tableWidget.setItem(i, 0,QtWidgets.QTableWidgetItem(name[:-1]))
            self.ui.tableWidget.setItem(i, 1,QtWidgets.QTableWidgetItem(str(value).replace('\n','')))
            i = i + 1

        print("Updating Data in Widget:")
        print(data)

# This thread works independently on the main.
# This one gets each value from the coms hub
# This thread will also work with logging data to a file
# This thread will also emit data to the graph windows to be graphed. 
# https://www.youtube.com/watch?v=eYJTcLBQKug
# https://wiki.python.org/moin/PyQt5/Threading%2C_Signals_and_Slots
# Going to try to keep everything in this one thread as the max number of threads
# corresponds to the max number of processor threads that your machine has (logical processors)
class DataCollectionThread(QThread):

    #This dict is sent as a signal from the thread that started it.
    new_data_dict = pyqtSignal(dict)

    def __init__(self):
        QThread.__init__(self, parent = app)
        self.threadactive = False
        self.connection = 0
        self.value_dict = {}
        self.graph_window_pointers = {}

    def setup(self, dict_value_names, serial_con, time_delay):
        self.connection = serial_con
        self.value_dict = dict_value_names
        self.time_delay = time_delay

    # Even though worker is running infinitely, can call this function and "register" windows with variable it requires.
    # Essentially I just pass a pointer to the window, and the name of the variable it needs. 
    def register(self, window, variable):
        print("I HAVE BEEN REGISTERED")
        if variable not in self.graph_window_pointers:
            self.graph_window_pointers[variable] = window

    # This is the main function of the thread. Purpose is to query coms hub
    # for variable from dictionary of value names and types.
    def run(self):
        values_read = {}
 
        if debug == 0:

            #From the dictionary, get value name, and expected value type.
            while True:
                for name, type in self.value_dict.items():

                    #Command to get variable
                    bitString = "GET {}".format(name)
                    self.connection.write(bitString.encode(encoding='ascii'))

                    try:
                        # Read value from Coms hub
                        value = self.connection.readline().decode(encoding='ascii').split(" ")[-1]
                        if type == 'F':
                            values_read[name] = float(value)
                        else:
                            values_read[name] = value
                    except: #Sometimes get here when reset 
                        print("Error, at reading data")
                        pass

                self.update_registered_windows(values_read)
                self.new_data_dict.emit(values_read)
                time.sleep(self.time_delay)

        else:
            while True:
                values_read = generate_random_data()
                self.new_data_dict.emit(values_read)
                time.sleep(self.time_delay)

                self.update_registered_windows(values_read)


    # Update registered windows by sending variable data they need.
    def update_registered_windows(self, values_read):
        if len(self.graph_window_pointers) != 0:
            print("Updating {} graph windows".format(self.graph_window_pointers))

            for registered_window in self.graph_window_pointers:
                print("Calling window: {}".format(registered_window))
                print(values_read[registered_window])
                self.graph_window_pointers[registered_window].receive_data("{} {}".format(registered_window, values_read[registered_window]))


    # Function to kill a thread
    # https://stackoverflow.com/questions/51135444/how-to-kill-a-running-thread
    def stop(self):
        self.threadactive = False
        self.wait()



def generate_random_data():
    values = ['data1','data2','data3','data4','data5','data6']
    data_dict = {}

    for i in values:
        data_dict[i] = random.randint(1, 10)

    return(data_dict)

# Make another worker here for the graph screen. Can connect the the function that gets coms data to multiple functions. 
# BE CAREFUL NOT TO DO ANY WORK IN THIS THREAD (Updates are okay), OTHERWISE IT LOCKS UP ALL GUI THREADS
# https://stackoverflow.com/questions/10653704/pyqt-connect-signal-to-multiple-slot
class GraphWindow(QtWidgets.QDialog):
    def __init__(self,  window_pointer, set_variable):

        super(GraphWindow, self).__init__()
        self.textt = "click me"
        print("Opened window for variable: {}".format(set_variable))

        self.layout = QtWidgets.QVBoxLayout()
        self.setWindowTitle("Graphing Variable: {}".format(set_variable))

        self.pushDisButton = QtWidgets.QPushButton("trial")
        self.resize(630, 150)
        self.layout.addWidget(self.pushDisButton)
        self.setLayout(self.layout)

    # This function receives data from the DataCollectionThread
    def receive_data(self, data):
        print("Window {} got data".format(data))
        self.pushDisButton.setText(str(data))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

