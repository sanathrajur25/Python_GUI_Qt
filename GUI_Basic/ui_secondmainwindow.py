# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'secondmainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_SecondMainWindow(object):
    def setupUi(self, SecondMainWindow):
        if not SecondMainWindow.objectName():
            SecondMainWindow.setObjectName(u"SecondMainWindow")
        SecondMainWindow.resize(1920, 1080)
        self.centralwidget = QWidget(SecondMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.SecondFSO = QLabel(self.centralwidget)
        self.SecondFSO.setObjectName(u"SecondFSO")
        self.SecondFSO.setGeometry(QRect(370, 150, 1024, 720))
        self.SecondFSO.setScaledContents(True)
        SecondMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SecondMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 21))
        SecondMainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SecondMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        SecondMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SecondMainWindow)

        QMetaObject.connectSlotsByName(SecondMainWindow)
    # setupUi

    def retranslateUi(self, SecondMainWindow):
        SecondMainWindow.setWindowTitle(QCoreApplication.translate("SecondMainWindow", u"MainWindow", None))
        self.SecondFSO.setText("")
    # retranslateUi

