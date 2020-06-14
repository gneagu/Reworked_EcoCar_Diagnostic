# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eventUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EventWindow(object):
    def setupUi(self, EventWindow):
        EventWindow.setObjectName("EventWindow")
        EventWindow.resize(401, 476)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EventWindow.sizePolicy().hasHeightForWidth())
        EventWindow.setSizePolicy(sizePolicy)
        EventWindow.setMinimumSize(QtCore.QSize(401, 476))
        EventWindow.setMaximumSize(QtCore.QSize(401, 476))
        self.layoutWidget = QtWidgets.QWidget(EventWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 361, 431))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.layoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 174, 427))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.eventList = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.eventList.setGeometry(QtCore.QRect(0, 0, 181, 441))
        self.eventList.setObjectName("eventList")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.layoutWidget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 174, 427))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.alarmList = QtWidgets.QListWidget(self.scrollAreaWidgetContents_2)
        self.alarmList.setGeometry(QtCore.QRect(0, 0, 181, 441))
        self.alarmList.setObjectName("alarmList")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.scrollArea_2)
        self.label = QtWidgets.QLabel(EventWindow)
        self.label.setGeometry(QtCore.QRect(20, 10, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(EventWindow)
        self.label_2.setGeometry(QtCore.QRect(210, 10, 55, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(EventWindow)
        QtCore.QMetaObject.connectSlotsByName(EventWindow)

    def retranslateUi(self, EventWindow):
        _translate = QtCore.QCoreApplication.translate
        EventWindow.setWindowTitle(_translate("EventWindow", "Dialog"))
        self.label.setText(_translate("EventWindow", "Events"))
        self.label_2.setText(_translate("EventWindow", "Alarms"))
