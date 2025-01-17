from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import time
from gui import debug


class TestWindow(QtWidgets.QDialog):
    def __init__(self):
        super(TestWindow, self).__init__()

        layout = QtWidgets.QVBoxLayout()
        self.table = QtWidgets.QTableWidget(2,2)
        # self.table.show()

        self.tableItem = QtWidgets.QLineEdit()
        self.tableItem.setText( "Testing" )
        self.table.setCellWidget(0, 0, self.tableItem )
        # Connect signal which is emmited when done editing qlineedit box
        self.ui = debug.Ui_Dialog()
        self.ui.setupUi(self)

        # self.ui.show()
        # self.tableItem.textEdited.connect(self.doNot)
        # self.tableItem.focusInEvent = self.change

        # self.tableItem.copyAvailable = self.available

        layout.addWidget(self.table)

        # self.comboBox = QtWidgets.QComboBox()
        # self.table.setCellWidget(1,1, self.comboBox)
        self.doSomething()


    # self.text_box.installEventFilter(self)
    # https://stackoverflow.com/a/57698918
        self.tableItem.installEventFilter(self)
    def eventFilter(self, obj, event):
    	# print("eventFilter")
    	if event.type() == QtCore.QEvent.KeyPress and obj is self.tableItem:
    		print("TYPE")
    		if event.key() == QtCore.Qt.Key_Return and self.tableItem.hasFocus():
    			print('Enter pressed')
    			return True

    	return False
        # return False

    # def available(self, value):
    # 	print("Has been selected")
    # 	print(value)


    # def doNot(self):
    # 	print("Updated text")

    # def change(self, extra):
    # 	print("CHANGED SELCTION")


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
    	# if not self.tableItem.hasFocus():
	    # 	self.tableItem.setText(str(data))

        new_widget = QtWidgets.QLabel("GOT HERE{}".format(data))
        # self.ui.listView.addItem(QtWidgets.QListWidgetItem("TRIAL"))
        self.ui.listView.addItems(['a','s','d'])

        if not self.ui.listView.hasFocus():
            print("Has focus")
            self.ui.listView.scrollToBottom()

    	# print("The box is being clicked: {}".format(self.tableItem.hasFocus()))


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


# if __name__ == '__main__':

#     app = QtWidgets.QApplication(sys.argv)


#     listWidget = QtWidgets.QListWidget()
#     listWidget.show()

#     ls = ['test', 'test2', 'test3']

#     listWidget.addItem('test')
#     listWidget.addItem('test2')
#     listWidget.addItem('test3')

#     listWidget.addItems(ls)

#     sys.exit(app.exec_())