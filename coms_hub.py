import serial
import serial.tools.list_ports
import time
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from gui import mainUI_v6
from gui import debug as debug_window
from gui import eventUI as event_window

import random
from functools import partial
import csv
import datetime
import math
import tkinter
from shutil import copy
from tkinter import filedialog
import tkinter as tk
import os
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from numpy import linspace

debug = 0


class ErrorWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ErrorWindow, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Error: Coms Hub has \nbeen Disconnected"))

        self.setLayout(self.layout)

# Need to open DebugWindow as a dialog so I can show it and interact.
# https://stackoverflow.com/questions/29303901/attributeerror-startqt4-object-has-no-attribute-accept
class DebugWindow(QtWidgets.QDialog):
    def __init__(self, dct_thread_pointer, parent=None):
        super(DebugWindow, self).__init__(parent)
        self.ui2 = debug_window.Ui_Dialog()
        self.ui2.setupUi(self)
        self.unregister_pointer = dct_thread_pointer

    # https://stackoverflow.com/a/12366684
    def closeEvent(self, evnt):
        self.unregister_pointer.unregister_debugger()
        super(DebugWindow, self).closeEvent(evnt)

# Need to open DebugWindow as a dialog so I can show it and interact.
# https://stackoverflow.com/questions/29303901/attributeerror-startqt4-object-has-no-attribute-accept
class EventWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EventWindow, self).__init__(parent)
        self.ui3 = event_window.Ui_EventWindow()
        self.ui3.setupUi(self)

class MainWindow(QtWidgets.QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.numOfVars = 0
        self.buttons = []
        self.textedits = {} # Dict because I can't set a tooltip on a textedit
        self.connection = 0
        self.ui = mainUI_v6.Ui_Dialog()
        self.ui.setupUi(self)
        self.dict_value_type = {}
        self.dialogs = {}
        self.time_delay = self.ui.time_spinBox.value()
        self.thread = 0
        self.error_window = ErrorWindow()

        # Connecting push buttons to their functions
        self.ui.set_pushButton_2.clicked.connect(self.set_data_view_variables)
        self.ui.refresh_pushButton.clicked.connect(self.set_port_comboBox_selections)
        self.ui.version_pushButton_4.clicked.connect(self.open_version_window)
        self.ui.export_pushButton_5.clicked.connect(self.open_file_save_dialog)
        self.ui.debug_pushButton_6.clicked.connect(self.open_debug_window)
        self.ui.events_pushButton_3.clicked.connect(self.open_event_window)

        # This searches active com ports, and adds them to the comboBox
        self.set_port_comboBox_selections()

    # Simple function. Bind window to a variable, else garbage collection gets it
    def open_version_window(self):
        self.new_window = VersionWindow()
        self.new_window.show()

    def open_debug_window(self):
        self.thread.register_debugger(self)

    def open_event_window(self):
        self.thread.show_events_window(self)

    # Over-riding close event so I can end the DataCollectionThread also.
    def closeEvent(self, event):
        # Close thread if it was opened (avoid error)
        if self.thread:
            self.thread.killthread()
        event.accept() # let the window close

    # Taking user selection, opens a conenction on specified port.
    def port_connect(self):
        self.time_delay = self.ui.time_spinBox.value()
        COM_port = self.ui.com_port_comboBox.currentText()
        baud_rate = self.ui.baud_rate_lineEdit.text()

        if debug == 0:

            try:
                if not self.connection:
                    print("MAKING A NEW CONNECTION")

                    portConnection = serial.Serial(COM_port, baud_rate, bytesize=8, parity='N', stopbits=1)
                    self.connection = portConnection
            except:
                print("Failed To Make Connection")
                return

        else:
            pass

    # Need to launch from contet of widget for dialog to open (little weird)
    # Need to send context of widget to the function in the DatCollectionThread
    def open_file_save_dialog(self):
        self.thread.save_data_file(self)

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

        for name in self.dict_value_type:
        # for i in range(int(self.numOfVars)):
            self.ui.tableWidget.insertRow(i)

            # Create Button to push to tableWidget
            self.buttons.append(QtWidgets.QPushButton(self.ui.tableWidget))
            self.buttons[i].setText("Graph".format(i))
            self.buttons[i].setToolTip(name)

            # Create textedit, and link to variable
            new_text_edit = QtWidgets.QLineEdit()
            self.textedits[name] = new_text_edit

            # Connecting custom event filter (press enter) so I know when to send new data to the coms hub
            self.textedits[name].installEventFilter(self)
            self.ui.tableWidget.setCellWidget(i, 1, self.textedits[name])

            # Set cell as button
            self.ui.tableWidget.setCellWidget(i, 2, self.buttons[i])
            self.buttons[i].clicked.connect(partial(self.on_pushButton_clicked, self.buttons[i]))

            i = i + 1

    # https://stackoverflow.com/a/57698918
    # Custom event filter to know when to send data to coms.
    # When activated, calls function in worker thread to add data to stack (send when available)
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj in self.textedits.values():
            print("TYPE")
            if event.key() == QtCore.Qt.Key_Return and obj.hasFocus():
                print('Enter pressed')

                # TODO: Beautify with a lambda statment
                value = [key for key,value in self.textedits.items() if value == obj]
                self.thread.add_to_stack('SET', value[0], obj.text())
                return True

        return False

    # https://stackoverflow.com/questions/36823841/pyqt-getting-which-button-called-a-specific-function
    # Each graph button in tablewidget has the tooltip set as corresponding variable name.
    # Simply get variable name and open graph window/register with expected variable.
    def on_pushButton_clicked(self, button):
        print("CLICKED")
        variable_name = button.toolTip()
        try:
            print("Tooltip")
            print(variable_name)
        except:
            print("Failed tooltip")

        # Simply call DCT.register with window reference, and variable name.
        # Let DCT create window and keep track, so we only have one list.
        self.thread.register(self.thread, variable_name)

    def get_value_name_dict(self, serial):
        ser = self.connection
        dict_value_type = {}

        if debug == 0:

            # Wipe com port buffer
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
            # print(dict_value_type)

        return dict_value_type

    # Enable Events, Debug, and Export button
    def enable_com_buttons(self):
        self.ui.events_pushButton_3.setEnabled(True)
        self.ui.debug_pushButton_6.setEnabled(True)
        self.ui.export_pushButton_5.setEnabled(True)

    # Disable buttons after com port selected (Must restart app to choose different com port)
    def disable_com_selections(self):
        self.ui.set_pushButton_2.setEnabled(False)
        self.ui.refresh_pushButton.setEnabled(False)
        self.ui.baud_rate_lineEdit.setEnabled(False)
        self.ui.direct_checkBox.setEnabled(False)
        self.ui.com_port_comboBox.setEnabled(False)

    # Recieves a dict with new data from coms board, and sends to worker thread.
    # Then starts worker thread.
    @QtCore.pyqtSlot()
    def set_data_view_variables(self):
        self.disable_com_selections()
        self.enable_com_buttons()
        # self.connection = self.port_connect()
        self.port_connect()

        # Adding condition because unless a connection is made, or debug. don't want to go any further.
        if self.connection or debug == 1:
            self.dict_value_type = self.get_value_name_dict(self.connection)

            #Set the columns here.0
            self.add_columns(self.numOfVars)

            #Launch seperate thread to get variable from coms hub.
            self.thread = DataCollectionThread()
            self.thread.new_data_dict.connect(self.update_data_view)
            self.thread.error_signal.connect(self.show_error)

            # https://stackoverflow.com/questions/45668961/send-data-to-qthread-when-in-have-changes-in-gui-windows-pyqt5
            self.thread.setup(self.dict_value_type, self.connection, self.time_delay, self)
            self.thread.start()

            # Connect spinbox to worker thread, but only after thread created.
            self.ui.time_spinBox.valueChanged.connect(self.thread.change_delay)

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
                self.ui.com_port_comboBox.addItem("No Com Ports Found")
                self.ui.set_pushButton_2.setEnabled(False);
            else:
                self.ui.set_pushButton_2.setEnabled(True);
                for port in list_of_ports:
                    self.ui.com_port_comboBox.addItem(port)
        else:
            self.ui.set_pushButton_2.setEnabled(True);
            self.ui.com_port_comboBox.addItem("DEBUG")



    def show_error(self, signal):
        print("OH BOY")

        self.error_window.show()



    # Emmited data from DataCollectionThread comes here.
    # This function updates the values in the main window.
    def update_data_view(self, data):
        i = 0

        for (name, value) in data.items():
            self.ui.tableWidget.setItem(i, 0,QtWidgets.QTableWidgetItem(name[:-1]))
  
            # Check if textedit is being modified before updating it.
            if not self.textedits[name].hasFocus():           
                self.textedits[name].setText(str(data[name]))
    
            i = i + 1

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
    #This signal is sent when the DCT ends due to the coms hub being disconnected.
    error_signal = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self, parent = None)
        self.threadactive = False
        self.connection = 0
        self.value_dict = {}
        self.graph_window_pointers = {}
        self.stack = []
        self.debugger = 0
        self.eventWindow = EventWindow()
        self.com_disconnect = 0


    def setup(self, dict_value_names, serial_con, time_delay, masterwindow_pointer):
        self.connection = serial_con
        self.value_dict = dict_value_names
        self.time_delay = time_delay
        # Including this pointer because I need to open an error window on 
        # com disconnect, but that also destroys the DCT.
        self.master_pointer = masterwindow_pointer

    # Update delay. Called when delay spinbox changed.
    def change_delay(self, new_time_delay):
        print("Delay has been changed to: {}".format(new_time_delay))
        self.time_delay = new_time_delay

    # Even though worker is running infinitely, can call this function and "register" windows with variable it requires.
    # Essentially I just pass a pointer to the window, and the name of the variable it needs. 
    def register(self, dct_reference, variable_name):
        if variable_name not in self.graph_window_pointers:
            print("REGISTERED NEW WINDOW")

            # Create new graph window, and keep pointer.
            newWindow = GraphWindow(dct_reference, variable_name)
            self.graph_window_pointers[variable_name] = newWindow

            # Show window.
            self.graph_window_pointers[variable_name].show()

    # Remove a window from list of windows to be updated.
    # Once reference to window is gone, garbage collection can get it.
    def unregister(self, variable):
        print("Unregistering graph: {}".format(variable))
        print(self.graph_window_pointers)
        if variable in self.graph_window_pointers:
            self.graph_window_pointers.pop(variable)

    # Register debug window so it can be updated when open.
    def register_debugger(self, main_window_reference):
        print("Registered debugger window.")

        if not self.debugger:
            self.debugger = DebugWindow(self, main_window_reference)
            self.debugger.show()

    # Unregister debug window so can stop updating it.
    def unregister_debugger(self):
        print("Unregistered debugger window.")
        self.debugger = 0

    # Keeping reference to window so I can update it
    def show_events_window(self, main_window_reference):
        print("Registered event window.")
    
        self.eventWindow.show()

    # Need to be able to send values to the coms_hub. 
    # Creating stack as functions can send data, and only coms hub has access to write to connection
    def add_to_stack(self, command, variable, value):
        self.stack.append((command, variable, value))
        print(self.stack)


    # Idea here is that we can recieve an error or alarm from the coms hub at any time. 
    # Either Ex// b'VAL *VCOUNT 11\n' or Ex// b'EVT HORN\n' or Ex// b'ALM HORN\n'
    def check_serial_buffer(self):
 
        # Have to have this conditional, otherwise the thread returns before actually reading any data, and then data is off by few spots.
        # So wait until get data. 
        while not self.connection.inWaiting():
            print("Waiting for data")
        while self.connection.inWaiting():
            received = self.connection.readline().decode(encoding='ascii').replace("\n",'')

            if received.split(" ")[0] == "VAL":
                return(received)
            elif received.split(" ")[0] == "EVT":
                current_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
                evt_string = received.replace("EVT ","")
                self.eventWindow.ui3.eventList.addItem("{} : {}".format(evt_string, current_time))
            elif received.split(" ")[0] == "ALM":
                current_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
                alm_string = received.replace("ALM ","")
                self.eventWindow.ui3.alarmList.addItem("{} : {}".format(alm_string, current_time))
            else:
                print("Unhandled data returned from coms hub.")

            return 0

    # This is the main function of the thread. Purpose is to query coms hub
    # for variable from dictionary of value names and types.
    def run(self):
        values_read = {}

        self.time_stamp_thread_start = time.time() * 1000
        self.file_name = str(datetime.datetime.now()).split(".")[0].replace(":",'-') + '.tsv'

        # https://docs.python.org/3/library/csv.html#csv.DictWriter
        # By using DictWriter, can supply writer with a dictionary, and it will take care of placing data.
        with open('temp/{}'.format(self.file_name), 'w', newline='') as self.csvfile:
            fieldnames = ["Timestamp"] + list(self.value_dict.keys())
            self.writer = csv.DictWriter(self.csvfile, delimiter = "\t", fieldnames=fieldnames)
            self.writer.writeheader()

            if self.connection:
                # Wipe com port buffer
                self.connection.flushInput()
                self.connection.flushOutput()


            #From the dictionary, get value name, and expected value type.
            while self.com_disconnect == 0:
                # Getting time in milliseconds
                time_start = time.time() * 1000
                timestamp = time_start - self.time_stamp_thread_start

                values_read = {}

                if debug == 0:

                    try:

                        # TODO: Need to check 
                        for name, type in self.value_dict.items():

                            #Command to get variable
                            bitString = "GET {}".format(name)
                            self.connection.write(bitString.encode(encoding='ascii'))
                            time.sleep(0.003)

                            # Update debug window we know what command was sent.
                            self.update_debugger(bitString.replace("\n",''))


                            print("Before debug")
                            print("WROTE: {}".format(str(bitString)))

                            # Read value from Coms hub
                            received = self.check_serial_buffer()


                            print("After update")

                            print("Got")
                            if received:
                                print(received)
                                value = received.split(" ")[-1]
                                
                                # Update debug window so we know what info was received.
                                self.update_debugger(received)

                                if type == 'F':
                                    values_read[name] = float(value)
                                else:
                                    values_read[name] = value

                            self.empty_stack()

                    except: #Sometimes get here when reset 
                        print("Error, at reading data")

                        # Check if com port is still connected, otherwise stop loop.
                        try:
                            print(self.connection.inWaiting())
                        except:
                            print("Coms hub has been disconnected.")
                            # Emit signal to main thread to open error window.
                            
                            self.com_disconnect = 1
                            self.error_signal.emit('error')

                        pass

                    # Code to run if debugging without coms_hub
                else:
                    values_read = generate_random_data()

                    # Randomly populate events window with alarm and event entries.
                    if (math.floor(time.time() * 1000)) % 7 == 0:
                        if self.eventWindow:
                            self.eventWindow.ui3.eventList.addItem("Had an event")
                            self.eventWindow.ui3.alarmList.addItem("Had an alarm")

                    # Update debugger window
                    self.update_debugger("Got fake data.")

                self.update_registered_windows(values_read, timestamp)
                print("Emit")
                print(values_read)
                self.new_data_dict.emit(values_read)

                self.write_to_file(values_read)

                #Send out data from the stack
                self.empty_stack()

                # Getting time in milliseconds
                time_end = time.time() * 1000

                # Subtract worked timed from time_delay so actually get next data at x milliseconds from 
                # last, and not just y milliseconds work + x milliseconds delay
                time_to_sleep = (self.time_delay - (time_end - time_start)) / 1000

                # print("With delay of {} will sleep {}".format(self.time_delay, time_to_sleep * 1000))

                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)

    # Check if debugWindow has been opened, then update. If not in focus, scroll to bottom of page.
    def update_debugger(self, string):
        if self.debugger:

            self.debugger.ui2.listView.addItem(string)

            if not self.debugger.ui2.listView.hasFocus():
                print("Not focussed")
                self.debugger.ui2.listView.scrollToBottom()

    # Update registered windows by sending variable data they need.
    def update_registered_windows(self, values_read, timestamp):
        if len(self.graph_window_pointers) != 0:
            print("Updating {} graph windows".format(self.graph_window_pointers))

            try:
                for registered_window in self.graph_window_pointers:
                    # print("Calling window: {}".format(registered_window))
                    # print(values_read[registered_window])
                    print(self.graph_window_pointers)
                    self.graph_window_pointers[registered_window].receive_data(int(values_read[registered_window]), timestamp)
            except RuntimeError as e:
                print("Encountered error: {} ".format(e))
                print("Usually dictionary changing size (unregister) while this function is looping")
            except:
                print("Don't know what error occured.")

    def empty_stack(self):
        if len(self.stack) > 0:
            # Empty stack
            for (command, variable_name, value) in self.stack:
                to_send = "{} {} {}\n".format(command, variable_name.replace('\n',''), value)
                print("Command sent to coms_hub: {}".format(to_send))

                # Only write if we have a connection open
                if debug == 0:
                    self.connection.write(to_send.encode(encoding='ascii'))
                self.stack.pop(0)

    # Simply write data to file and then "Flush" (write data)
    def write_to_file(self, values):
        #Get time stamp in miliseconds since thread start
        timestamp = (time.time() * 1000) - self.time_stamp_thread_start

        dict_to_write = values.copy()
        dict_to_write["Timestamp"] = math.floor(timestamp)

        self.writer.writerow(dict_to_write)
        self.csvfile.flush()

    # https://stackoverflow.com/questions/15416334/qfiledialog-how-to-set-default-filename-in-save-as-dialog
    # Open a dialog to determine save location, and then copy file from the temp location.
    def save_data_file(self, parent_window):
        destination_location = str(QtWidgets.QFileDialog.getSaveFileName(parent_window, "Select Directory", self.file_name)[0])

        # User can click cancel which leaves desination_location empty
        if destination_location != '':
            source_location = './temp/{}'.format(self.file_name)
            print("Save location: {}".format(destination_location))
            try:
                copy(source_location, destination_location)
            except:
                print("Could not copy file.")

    # Function to kill a thread
    # https://stackoverflow.com/questions/51135444/how-to-kill-a-running-thread
    def killthread(self):

        # End thread
        self.threadactive = False
        self.quit()
        self.terminate()

        # Release file so we can close it
        self.csvfile.close()

        # Delete data file if it has not been saved.
        try:
            location = '{}/temp/{}'.format(os.getcwd(), self.file_name).replace('\\','''/''')
            print(location)
            os.remove(location)
        except:
            print("Could not remove file from temp folder")

# Generate random data so I don't have to connect Com Hub
def generate_random_data():
    values = ['data1','data2','data3','data4','data5','data6']
    data_dict = {}

    for i in values:
        data_dict[i] = random.randint(1, 10)

    return(data_dict)

# Make another worker here for the graph screen. Can connect the the function that gets coms data to multiple functions. 
# BE CAREFUL NOT TO DO ANY WORK IN THIS THREAD (Updates are okay), OTHERWISE IT LOCKS UP GUI THREAD
# https://www.learnpyqt.com/courses/graphics-plotting/plotting-pyqtgraph/
# https://stackoverflow.com/a/45203110
class GraphWindow(QtWidgets.QDialog):
    def __init__(self,  parent_pointer, set_variable):
        super(GraphWindow, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)
        self.setLayout(layout)
        self.dct_pointer = parent_pointer
        self.title = set_variable # Need to keep the variable name so I can unregister from DCT

        self.setWindowTitle("Graphing Variable: {}".format(self.title))
        self.graphWidget.setMouseEnabled(x=False, y=False)

        self.time = list(range(100))
        self.value = [0] * 100

        self.data_line = self.graphWidget.plot(self.time, self.value)

    # Simple update is okay as it doesn't impact performance.
    # Very quick, so wont block GUI from responding.
    def receive_data(self, data, timestamp):
        # print("Got data: {}".format(data))
        self.value.pop(0)
        self.value.append(int(data))

        self.time.pop(0)
        self.time.append(int(timestamp))
        self.data_line.setData(self.time, self.value)

    # Overriding closeEvent, so I can unregister window from DataCollectionThread
    # https://stackoverflow.com/a/12366684
    def closeEvent(self, evnt):
        self.dct_pointer.unregister(self.title)
        super(GraphWindow, self).closeEvent(evnt)

# Simple little window to show some information
class VersionWindow(QtWidgets.QDialog):
    def __init__(self):
        super(VersionWindow, self).__init__()
        self.layout = QtWidgets.QVBoxLayout()

        self.version_label = QtWidgets.QLabel("Version: 0.02")
        self.layout.addWidget(self.version_label)

        self.setWindowTitle("Version")
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

