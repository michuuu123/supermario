# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scene.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(598, 340)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(50, 20, 400, 250))
        self.graphicsView.setObjectName("graphicsView")
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(490, 20, 100, 23))
        self.startBtn.setObjectName("startBtn")

        self.recordBtn = QtWidgets.QPushButton(self.centralwidget)
        self.recordBtn.setGeometry(QtCore.QRect(490, 200, 100, 23))
        self.recordBtn.setObjectName("recordBtn")

        self.saveBtn = QtWidgets.QPushButton(self.centralwidget)
        self.saveBtn.setGeometry(QtCore.QRect(490, 160, 100, 23))
        self.saveBtn.setObjectName("saveBtn")

        self.watchBtn = QtWidgets.QPushButton(self.centralwidget)
        self.watchBtn.setGeometry(QtCore.QRect(490, 230, 100, 23))
        self.watchBtn.setObjectName("watchBtn")

        self.loadBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loadBtn.setGeometry(QtCore.QRect(490, 130, 100, 23))
        self.loadBtn.setObjectName("loadBtn")

        self.endBtn = QtWidgets.QPushButton(self.centralwidget)
        self.endBtn.setGeometry(QtCore.QRect(490, 50, 100, 23))
        self.endBtn.setObjectName("endBtn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(500, 80, 47, 13))
        self.label.setObjectName("label")
        self.scoreBox = QtWidgets.QLineEdit(self.centralwidget)
        self.scoreBox.setEnabled(False)
        self.scoreBox.setGeometry(QtCore.QRect(500, 100, 30, 20))
        self.scoreBox.setObjectName("scoreBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 598, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Super Mario"))
        self.startBtn.setText(_translate("MainWindow", "New Game"))
        self.endBtn.setText(_translate("MainWindow", "Pause"))
        self.recordBtn.setText(_translate("MainWindow", "Record"))
        self.saveBtn.setText(_translate("MainWindow", "Save"))
        self.loadBtn.setText(_translate("MainWindow", "Load"))
        self.watchBtn.setText(_translate("MainWindow", "Watch"))
        self.label.setText(_translate("MainWindow", "Score"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

