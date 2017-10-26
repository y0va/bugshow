# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(815, 777)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pbLevel = QtGui.QProgressBar(self.centralwidget)
        self.pbLevel.setMaximum(1000)
        self.pbLevel.setProperty("value", 123)
        self.pbLevel.setTextVisible(False)
        self.pbLevel.setOrientation(QtCore.Qt.Vertical)
        self.pbLevel.setObjectName(_fromUtf8("pbLevel"))
        self.horizontalLayout.addWidget(self.pbLevel)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.grFFT_long = PlotWidget(self.frame_2)
        self.grFFT_long.setObjectName(_fromUtf8("grFFT_long"))
        self.horizontalLayout_2.addWidget(self.grFFT_long)
        self.frame_4 = QtGui.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.img_gk = QtGui.QLabel(self.frame_4)
        self.img_gk.setObjectName(_fromUtf8("img_gk"))
        self.verticalLayout.addWidget(self.img_gk)
        self.img_kk = QtGui.QLabel(self.frame_4)
        self.img_kk.setObjectName(_fromUtf8("img_kk"))
        self.verticalLayout.addWidget(self.img_kk)
        self.logo_it = QtGui.QLabel(self.frame_4)
        self.logo_it.setObjectName(_fromUtf8("logo_it"))
        self.verticalLayout.addWidget(self.logo_it)
        self.logo_uni = QtGui.QLabel(self.frame_4)
        self.logo_uni.setObjectName(_fromUtf8("logo_uni"))
        self.verticalLayout.addWidget(self.logo_uni)
        self.horizontalLayout_2.addWidget(self.frame_4)
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame_3 = QtGui.QFrame(self.frame)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_fps = QtGui.QLabel(self.frame_3)
        self.label_fps.setObjectName(_fromUtf8("label_fps"))
        self.horizontalLayout_3.addWidget(self.label_fps)
        self.label = QtGui.QLabel(self.frame_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.label_top = QtGui.QLabel(self.frame_3)
        self.label_top.setObjectName(_fromUtf8("label_top"))
        self.horizontalLayout_3.addWidget(self.label_top)
        self.nextView = QtGui.QToolButton(self.frame_3)
        self.nextView.setObjectName(_fromUtf8("nextView"))
        self.horizontalLayout_3.addWidget(self.nextView)
        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionNext = QtGui.QAction(MainWindow)
        self.actionNext.setObjectName(_fromUtf8("actionNext"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
             # Set background of title & legend white 
        self.frame_4.setAutoFillBackground(True)
        p = self.frame_4.palette()
        p.setColor(self.frame_4.backgroundRole(), QtCore.Qt.white)
        self.frame_4.setPalette(p)
        
        self.frame_3.setAutoFillBackground(True)
        p = self.frame_3.palette()
        p.setColor(self.frame_3.backgroundRole(), QtCore.Qt.white)
        self.frame_3.setPalette(p)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.img_gk.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/bug/picture/mini/Getreidekapuziner.png\"/></p></body></html>", None))
        self.img_kk.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/bug/picture/mini/Kornkaefer.png\"/></p></body></html>", None))
        self.logo_it.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/logo/picture/insecttap.png\"/></p></body></html>", None))
        self.logo_uni.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/logo/picture/uni_logo.gif\"/></p></body></html>", None))
        self.label_fps.setText(_translate("MainWindow", "FPS", None))
        self.label.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">InsectTap</span></p></body></html>", None))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><img src=\":/logo/picture/ptble.jpg\"/></p></body></html>", None))
        self.label_top.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>", None))
        self.nextView.setText(_translate("MainWindow", "Next", None))
        self.actionNext.setText(_translate("MainWindow", "next", None))

from pyqtgraph import PlotWidget
import ressources_rc
