# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(343, 453)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(21, 28, 300, 81))
        self.frame.setAccessibleName(_fromUtf8(""))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setMidLineWidth(1)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.direct_checkBox = QtWidgets.QCheckBox(self.frame)
        self.direct_checkBox.setGeometry(QtCore.QRect(120, 46, 81, 20))
        self.direct_checkBox.setObjectName(_fromUtf8("direct_checkBox"))
        self.refresh_pushButton = QtWidgets.QPushButton(self.frame)
        self.refresh_pushButton.setGeometry(QtCore.QRect(198, 10, 93, 28))
        self.refresh_pushButton.setObjectName(_fromUtf8("refresh_pushButton"))
        self.set_pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.set_pushButton_2.setGeometry(QtCore.QRect(198, 43, 93, 28))
        self.set_pushButton_2.setObjectName(_fromUtf8("set_pushButton_2"))
        self.baud_rate_lineEdit = QtWidgets.QLineEdit(self.frame)
        self.baud_rate_lineEdit.setGeometry(QtCore.QRect(11, 44, 61, 26))
        self.baud_rate_lineEdit.setInputMask(_fromUtf8(""))
        self.baud_rate_lineEdit.setMaxLength(6)
        self.baud_rate_lineEdit.setObjectName(_fromUtf8("baud_rate_lineEdit"))
        self.com_port_comboBox = QtWidgets.QComboBox(self.frame)
        self.com_port_comboBox.setGeometry(QtCore.QRect(11, 11, 121, 26))
        self.com_port_comboBox.setObjectName(_fromUtf8("com_port_comboBox"))
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(80, 48, 41, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(21, 140, 301, 291))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setAccessibleName(_fromUtf8(""))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setMidLineWidth(1)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.events_pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.events_pushButton_3.setGeometry(QtCore.QRect(198, 10, 93, 28))
        self.events_pushButton_3.setObjectName(_fromUtf8("events_pushButton_3"))
        self.version_pushButton_4 = QtWidgets.QPushButton(self.frame_2)
        self.version_pushButton_4.setGeometry(QtCore.QRect(10, 250, 93, 28))
        self.version_pushButton_4.setObjectName(_fromUtf8("version_pushButton_4"))
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(10, 13, 81, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.time_spinBox = QtWidgets.QSpinBox(self.frame_2)
        self.time_spinBox.setGeometry(QtCore.QRect(90, 10, 61, 22))
        self.time_spinBox.setMinimum(200)
        self.time_spinBox.setMaximum(999999)
        self.time_spinBox.setObjectName(_fromUtf8("time_spinBox"))
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(160, 13, 21, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.debug_pushButton_5 = QtWidgets.QPushButton(self.frame_2)
        self.debug_pushButton_5.setGeometry(QtCore.QRect(198, 250, 93, 28))
        self.debug_pushButton_5.setObjectName(_fromUtf8("debug_pushButton_5"))
        self.debug_pushButton_6 = QtWidgets.QPushButton(self.frame_2)
        self.debug_pushButton_6.setGeometry(QtCore.QRect(104, 250, 93, 28))
        self.debug_pushButton_6.setObjectName(_fromUtf8("debug_pushButton_6"))
        self.tableWidget = QtWidgets.QTableWidget(self.frame_2) #Remove row numbers from tableWidget
        self.tableWidget.setGeometry(QtCore.QRect(10, 49, 280, 192))
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setVisible(False)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(23, 8, 71, 16))
        self.label_4.setText(_fromUtf8("COM Port"))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(24, 120, 55, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.direct_checkBox.setText(_translate("Dialog", "Direct", None))
        self.refresh_pushButton.setText(_translate("Dialog", "Refresh", None))
        self.set_pushButton_2.setText(_translate("Dialog", "Set", None))
        self.baud_rate_lineEdit.setText(_translate("Dialog", "125000", None))
        self.label.setText(_translate("Dialog", "Baud", None))
        self.events_pushButton_3.setText(_translate("Dialog", "Events", None))
        self.version_pushButton_4.setText(_translate("Dialog", "Version", None))
        self.label_2.setText(_translate("Dialog", "Sync every", None))
        self.label_3.setText(_translate("Dialog", "ms", None))
        self.debug_pushButton_5.setText(_translate("Dialog", "Debug", None))
        self.debug_pushButton_6.setText(_translate("Dialog", "Debug", None))
        self.label_5.setText(_translate("Dialog", "Data", None))