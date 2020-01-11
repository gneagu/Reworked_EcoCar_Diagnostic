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

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # thread = AThread()
    # thread.finished.connect(app.exit)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())


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
