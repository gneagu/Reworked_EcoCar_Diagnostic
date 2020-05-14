import serial
import time
import ast
import cProfile
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from gui import mainUI2, trial
import sys

debug = 0

# Not a mainwindow (Is a dialog), so need to inherit from it
# https://stackoverflow.com/questions/29303901/attributeerror-startqt4-object-has-no-attribute-accept
class EventWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EventWindow, self).__init__(parent)
        self.ui2 = trial.Ui_Dialog()
        self.ui2.setupUi(self)
        # self.ui2.setupUi(self)

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


        self.ui.set_pushButton_2.clicked.connect(self.set_data_view_variables)
        self.ui.refresh_pushButton.clicked.connect(self.set_port_comboBox_selections)
        self.ui.version_pushButton_4.clicked.connect(self.show_trial_screen)

        # This searches active com ports, and adds them to the comboBox
        self.set_port_comboBox_selections()

    def show_trial_screen(self):
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
        if not self.connection:
            print("MAKING A NEW CONNECTION")

            portConnection = serial.Serial(COM_port, baud_rate, bytesize=8, parity='N', stopbits=1)
            self.connection = portConnection


    # Remove rows and columns. (Needs to be reversed since removing column at start
    # remaps proceeding)
    def empty_table_widget(self):
        totalColumns = self.ui.tableWidget.columnCount()
        totalRows = self.ui.tableWidget.rowCount() 

        for index in range(totalRows):
            self.ui.tableWidget.removeRow(index)

        for index in range(totalColumns)[::-1]:
            self.ui.tableWidget.removeColumn(index)

        print("done")

    # https://stackoverflow.com/questions/40815730/how-to-add-and-retrieve-items-to-and-from-qtablewidget
    def add_columns(self, numOfVars):
        self.empty_table_widget()

        #Add columns here to table.
        self.ui.tableWidget.insertColumn(0)
        self.ui.tableWidget.insertColumn(1)
        self.ui.tableWidget.insertColumn(2)

        # Given dict with variables, query board for value and upgate gui

        self.buttons = []


        for i in range(int(self.numOfVars)):
            self.ui.tableWidget.insertRow(i - 1)

            #Create Button to push to tableWidget
            self.buttons.append(QtWidgets.QPushButton(self.ui.tableWidget))
            self.buttons[i].setText("Graph".format(i))

            #Set cell as button
            self.ui.tableWidget.setCellWidget(i, 2, self.buttons[i])

    def get_value_name_dict(self, serial):
        ser = self.connection
        dict_value_type = {}

        print(serial)
        print(self.connection)

        # Wipe serial connection buffer
        ser.flushInput()
        ser.flushOutput()

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
            ports = ['COM{}'.format(i + 1) for i in range(255)]

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
            self.ui.set_pushButton_2.setEnabled(True);
            for port in list_of_ports:
                self.ui.com_port_comboBox.addItem(port)

    # Emmited data from DataCollectionThread come here.
    # This function updates the values in the main window.
    def update_data_view(self, data):
        #Create text name
        i = 0
        for (name, value) in data.items():
             # = data[i]
            self.ui.tableWidget.setItem(i, 0,QtWidgets.QTableWidgetItem(name[:-1]))
            self.ui.tableWidget.setItem(i, 1,QtWidgets.QTableWidgetItem(str(value).replace('\n','')))
            i = i + 1

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






# import time
# import sys
# from PyQt5 import QtWidgets, QtGui, QtCore

# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.worker_thread = WorkerThread()
#         self.worker_thread.job_done.connect(self.on_job_done)
#         self.create_ui()

#     def create_ui(self):
#         self.button = QtWidgets.QPushButton('Test', self)
#         self.button.clicked.connect(self.start_thread)
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(self.button)

#     def start_thread(self):
#         self.worker_thread.gui_text = self.button.text()
#         self.worker_thread.start()

#     def on_job_done(self, generated_str):
#         print("Generated string : ", generated_str)
#         self.button.setText(generated_str)


# class WorkerThread(QtCore.QThread):

#     job_done = QtCore.pyqtSignal('QString')

#     def __init__(self, parent=None):
#         super(WorkerThread, self).__init__(parent)
#         self.gui_text = None

#     def do_work(self):

#         for i in range(0, 1000):
#             print(self.gui_text)
#             self.job_done.emit(self.gui_text + str(i))
#             time.sleep(0.5)

#     def run(self):
#         self.do_work()


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     test = MainWindow()
#     test.show()
#     app.exec_()

# import time
# import sys
# from PyQt5 import QtWidgets, QtGui, QtCore

# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.worker_thread = WorkerThread()
#         self.worker_thread.job_done.connect(self.on_job_done)
#         print(dir(self.worker_thread))
#         self.create_ui()
#         self.create_button()
#         self.layout = 0




#     def create_ui(self):
#         self.button = QtWidgets.QPushButton('Test', self)
#         self.button.clicked.connect(self.start_thread)
#         self.layout = QtWidgets.QGridLayout(self)
#         self.layout.addWidget(self.button)

#     def create_button(self):
#         self.xbutton = QtWidgets.QPushButton('trial', self)
#         self.xbutton.clicked.connect(self.check_if_running)
#         # layout = QtWidgets.QVBoxLayout(self)
#         self.layout.addWidget(self.xbutton)
#         self.layout.setGeometry(QtCore.QRect(120, 46, 81, 30))
#         # self.layout.xbutton.move(50,50)

#     def check_if_running(self):
#         print("thread is running {}".format(self.worker_thread.isRunning()))

#     def start_thread(self):
#         self.worker_thread.gui_text = self.button.text()
#         self.worker_thread.start()

#     def on_job_done(self, generated_str):
#         print("Generated string : ", generated_str)
#         self.button.setText(generated_str)


# class WorkerThread(QtCore.QThread):

#     job_done = QtCore.pyqtSignal('QString')

#     def __init__(self, parent=None):
#         super(WorkerThread, self).__init__(parent)
#         self.gui_text = None

#     def do_work(self):

#         for i in range(0, 1000):
#             print("GUI TEXT")
#             print(self.gui_text)
#             self.job_done.emit(self.gui_text + str(i))
#             time.sleep(0.5)

#     def change_text(self, text):
#         self.gui_text = text

#     def run(self):
#         self.do_work()


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     test = MainWindow()
#     test.show()
#     app.exec_()




# from PyQt5 import QtGui, QtCore, QtWidgets
# import sys
# import time


# class Second(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super(Second, self).__init__(parent)
#         self.textt = "click me"

#         self.pushDisButton = QtWidgets.QPushButton("trial")
#         self.setCentralWidget(self.pushDisButton)

#         self.pushDisButton.clicked.connect(self.run_this)
       


#     def run_this(self):


#         for i in range(100):
#             time.sleep(1)
#             print("In loop")
#             pass




# class First(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super(First, self).__init__(parent)
#         self.pushButton = QtWidgets.QPushButton("click me")

#         self.setCentralWidget(self.pushButton)

#         self.pushButton.clicked.connect(self.on_pushButton_clicked)
#         self.dialog = Second(self)

#     def on_pushButton_clicked(self):
#         print("CLICKED")
#         self.dialog.show()


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     main = First()
#     main.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()