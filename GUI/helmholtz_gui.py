#3 booleans to use, readytostart, readytoload, testrunning
"""TODO
Start/Stop functionality
Get data for Amps, Volts, Temps
Write temp data to the table
Functionality of Time Elasped
Ensure the update function works with data gathering
"""
import sys,os
sys.path.insert(0,os.path.abspath('..'))
from PyQt5 import QtCore, QtGui, QtWidgets
from piCode.Helmholtz import HelmholtzCage
import time
import threading

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(836, 578)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonFilePath = QtWidgets.QPushButton(self.centralwidget)
        self.buttonFilePath.setGeometry(QtCore.QRect(20, 10, 93, 31))
        self.buttonFilePath.setObjectName("buttonFilePath")
        self.tableVectors = QtWidgets.QTableWidget(self.centralwidget)
        self.tableVectors.setGeometry(QtCore.QRect(20, 80, 571, 461))
        self.tableVectors.setObjectName("tableVectors")
        self.tableVectors.setColumnCount(4)
        self.tableVectors.setRowCount(0)
        self.textBrowserFilePath = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserFilePath.setGeometry(QtCore.QRect(120, 10, 471, 31))
        self.textBrowserFilePath.setObjectName("textBrowserFilePath")
        self.labelAmps = QtWidgets.QLabel(self.centralwidget)
        self.labelAmps.setGeometry(QtCore.QRect(620, 100, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelAmps.setFont(font)
        self.labelAmps.setObjectName("labelAmps")
        self.labelVolts = QtWidgets.QLabel(self.centralwidget)
        self.labelVolts.setGeometry(QtCore.QRect(620, 150, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelVolts.setFont(font)
        self.labelVolts.setAutoFillBackground(False)
        self.labelVolts.setObjectName("labelVolts")
        self.textBrowserAmps = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserAmps.setGeometry(QtCore.QRect(690, 110, 131, 31))
        self.textBrowserAmps.setObjectName("textBrowserAmps")
        self.textBrowserVolts = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserVolts.setGeometry(QtCore.QRect(690, 150, 131, 31))
        self.textBrowserVolts.setObjectName("textBrowserVolts")
        self.labelTemps = QtWidgets.QLabel(self.centralwidget)
        self.labelTemps.setGeometry(QtCore.QRect(680, 180, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelTemps.setFont(font)
        self.labelTemps.setObjectName("labelTemps")
        self.tableTemps = QtWidgets.QTableView(self.centralwidget)
        self.tableTemps.setGeometry(QtCore.QRect(610, 220, 211, 321))
        self.tableTemps.setObjectName("tableTemps")
        self.buttonStart = QtWidgets.QPushButton(self.centralwidget)
        self.buttonStart.setGeometry(QtCore.QRect(690, 10, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.buttonStart.setFont(font)
        self.buttonStart.setObjectName("buttonStart")
        self.buttonLoad = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLoad.setGeometry(QtCore.QRect(612, 10, 71, 31))
        self.buttonLoad.setObjectName("buttonLoad")
        self.labelVectors = QtWidgets.QLabel(self.centralwidget)
        self.labelVectors.setGeometry(QtCore.QRect(220, 40, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelVectors.setFont(font)
        self.labelVectors.setObjectName("labelVectors")
        self.labelTime = QtWidgets.QLabel(self.centralwidget)
        self.labelTime.setGeometry(QtCore.QRect(610, 70, 211, 31))
        self.labelTime.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelTime.setObjectName("labelTime")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.tableVectors.setHorizontalHeaderLabels(["Time", "X", "Y", "Z"])
        self.readytoload = False
        self.readytostart = False
        self.testrunning = False
        self.statusbar.showMessage("No file selected. Add file to path and press load to begin.")
        self.buttonFilePath.clicked.connect(self.selectFile)
        self.buttonLoad.clicked.connect(self.load)
        self.buttonStart.clicked.connect(self.start)
        self.buttonStart.setStyleSheet("background-color: green")


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonFilePath.setText(_translate("MainWindow", "Load File Path"))
        self.labelAmps.setText(_translate("MainWindow", "Amps"))
        self.labelVolts.setText(_translate("MainWindow", "Volts"))
        self.labelTemps.setText(_translate("MainWindow", "Temps"))
        self.buttonStart.setText(_translate("MainWindow", "Start"))
        self.buttonLoad.setText(_translate("MainWindow", "Load"))
        self.labelVectors.setText(_translate("MainWindow", "Vector Information"))
        self.labelTime.setText(_translate("MainWindow", "Time Elapsed: 00:00:00 hh:mm:ss"))
      
    def selectFile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select File","","(*.csv)")
        if filename:
            self.statusbar.showMessage("File found. Press load to load file.")
            self.path = str(filename)
            self.textBrowserFilePath.setPlainText(self.path)
            self.readytoload = True
    
    def load(self): # Loads data from csv into the tablew view.
        if self.readytoload == True:
            self.cage_model = HelmholtzCage(self.path, 0.8, 0.8 * 0.5445, 25)
            self.tableVectors.setRowCount(len(self.cage_model.get_mag_x()))
            
            for i in range(len(self.cage_model.get_mag_x())):               
                time = self.cage_model.get_time()[i].strftime("%D %I:%M:%S %p") # month/day/year H:M:S AM/PM
                self.tableVectors.setItem(i, 0, QtWidgets.QTableWidgetItem(time))
                self.tableVectors.setItem(i, 1, QtWidgets.QTableWidgetItem(str(round(self.cage_model.get_current_x()[i], 5))))
                self.tableVectors.setItem(i, 2, QtWidgets.QTableWidgetItem(str(round(self.cage_model.get_current_y()[i], 5))))
                self.tableVectors.setItem(i, 3, QtWidgets.QTableWidgetItem(str(round(self.cage_model.get_current_z()[i], 5))))                                                
            self.statusbar.showMessage("Load success. Review data and press start to begin test.")
            self.readytostart = True
        else:
            self.statusbar.showMessage("Some load error occurred. Ensure file is selected properly and try again.")

    def start(self):
        try:
            if self.readytostart == True:
                # start_test(self.cage_model) # waiting for this to be implemented
                self.testrunning = True
                self.readytoload = False
                #u = threading.Thread(target=self.update)
                #u.start()
                ##self.update #make this a thread probably
                ##self.readytostart = False #Do we really need this Boolean?
                self.statusbar.showMessage("Test started.")
                self.buttonStart.setText("Stop")
                self.buttonStart.clicked.connect(self.stop)
                self.buttonStart.setStyleSheet("background-color: red")
            else:
                self.statusbar.showMessage("Test is not ready to start. Ensure file is selected and loaded properly.")
                #with the new stop changes this should never print
        except:
            self.statusbar.showMessage("Some error occurred when starting the test.")
   
    def stop(self):
        try:
            if self.testrunning == True:
                # stop_test(self.cage_model) #TODO this
                self.testrunning = False
                self.readytoload = True
                #self.readytostart = True #Do we really need this Boolean?
                self.statusbar.showMessage("Test stopped.")
                self.buttonStart.setText("Start")
                self.buttonStart.clicked.connect(self.start)
                self.buttonStart.setStyleSheet("background-color: green")
            else:
                self.statusbar.showMessage("Test is not currently running.")
                #probably should not show up when I code the start button changing
                
        except:    
            self.statusbar.showMessage("Some error occurred when stopping the test.")
    
    #constantly running function while the test has started
    def update(self):
        self.buttonFilePath.setStyleSheet("background-color: blue")
        while(self.testrunning):
            #get data for amps temps and volts
            self.buttonLoad.setStyleSheet("background-color: yellow")
            #u.sleep(10000)
            #self.textBrowserAmps.setPlainText("0.00")#Cannot create children for a parent that is in a different thread.
            #self.textBrowserVolts.setPlainText("0.00")
            
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
