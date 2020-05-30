from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import time


class TestWindow(QtWidgets.QDialog):
    def __init__(self):
        super(TestWindow, self).__init__()

        layout = QtWidgets.QVBoxLayout()
        self.table = QtWidgets.QTableWidget(2,2)
        self.table.show()

        self.tableItem = QtWidgets.QLineEdit()
        self.tableItem.setText( "Testing" )
        self.table.setCellWidget(0, 0, self.tableItem )
        # Connect signal which is emmited when done editing qlineedit box
        self.tableItem.textEdited.connect(self.doNot)
        self.tableItem.focusOutEvent = self.change

        self.tableItem.copyAvailable = self.available

        layout.addWidget(self.table)

        self.comboBox = QtWidgets.QComboBox()
        self.table.setCellWidget(1,1, self.comboBox)
        self.doSomething()


    # self.text_box.installEventFilter(self)
    # ...
        self.tableItem.installEventFilter(self)
    def eventFilter(self, obj, event):
    	# print("eventFilter")
    	if event.type() == QtCore.QEvent.KeyPress and obj is self.tableItem:
    		print("TYPE")
    		if event.key() == QtCore.Qt.Key_Return and self.text_box.hasFocus():
    			print('Enter pressed')
    			return True

    	return False
        # return False

    def available(self, value):
    	print("Has been selected")
    	print(value)


    def doNot(self):
    	print("Updated text")

    def change(self, extra):
    	print("CHANGED SELCTION")


    def doSomething(self):
    	# value = self.tableItem.text()
    	# print("GOT THIS VALUE: {}".format(value))
        #Launch seperate thread to get variable from coms hub.
        self.thread = DataCollectionThread()
        self.thread.new_data_dict.connect(self.update_data_view)

        # https://stackoverflow.com/questions/45668961/send-data-to-qthread-when-in-have-changes-in-gui-windows-pyqt5
        # self.thread.setup()
        self.thread.start()

    def update_data_view(self, data):
    	self.tableItem.setText(str(data))


class DataCollectionThread(QThread):

    new_data_dict = pyqtSignal(int)
    def __init__(self):
        QThread.__init__(self, parent = app)
        self.i = 0


    def run(self):
    	while True:
	        print("Looped {}".format(self.i))
	        self.new_data_dict.emit(self.i)
	        self.i = self.i + 1
	        time.sleep(1)


    #This dict is sent as a signal from the thread that started it.
    # new_data_dict = pyqtSignal(dict)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())