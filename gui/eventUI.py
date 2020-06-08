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
        self.widget = QtWidgets.QWidget(EventWindow)
        self.widget.setGeometry(QtCore.QRect(20, 20, 361, 441))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 174, 437))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.eventList = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.eventList.setGeometry(QtCore.QRect(0, 0, 181, 441))
        self.eventList.setObjectName("eventList")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.widget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 174, 437))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.alarmList = QtWidgets.QListView(self.scrollAreaWidgetContents_2)
        self.alarmList.setGeometry(QtCore.QRect(0, 0, 181, 441))
        self.alarmList.setObjectName("alarmList")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.scrollArea_2)

        self.retranslateUi(EventWindow)
        QtCore.QMetaObject.connectSlotsByName(EventWindow)

    def retranslateUi(self, EventWindow):
        _translate = QtCore.QCoreApplication.translate
        EventWindow.setWindowTitle(_translate("EventWindow", "Dialog"))
