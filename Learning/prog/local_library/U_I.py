import pandas as pd
import numpy as np
from scipy.stats import beta, ev, genpareto
from scipy.optimize import minimize
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

class DistributionFitting(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Distribution Fitting"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Create Open File button
        self.openFile = QtWidgets.QPushButton(self)
        self.openFile.setText("Open File")
        self.openFile.move(10,10)
        self.openFile.clicked.connect(self.open_file)
        
        # Create Fit Distribution button
        self.fitDistribution = QtWidgets.QPushButton(self)
        self.fitDistribution.setText("Fit Distribution")
        self.fitDistribution.move(100,10)
        self.fitDistribution.clicked.connect(self.fit_distribution)
        self.fitDistribution.setEnabled(False)
        
        # Create result textbox
        self.result = QtWidgets.QTextEdit(self)
        self.result.move(10, 50)
        self.result.resize(620, 400)
        
        self.show()
    
    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self,"Open Data File", "","All Files (*);;Text Files (*.csv)", options=options)
        if fileName:
            self.data = pd.read_csv(fileName)
            self.fitDistribution.setEnabled(True)
            self.result.append("Data Loaded: " + fileName + '\n')
    
    def fit_distribution(self):
        self.result.append("Fitting distributions...\n")
        self.result.append("Beta Distribution:\n")
        beta_params = beta.fit(self.data)
        self.result.append(str(beta_params) + '\n')
        self.result.append("Extreme Value Distribution:\n")
        ev_params = ev.fit(self.data)
        self.result.append(str(ev_params) + '\n')
        self.result.append("Generalized Pareto Distribution:\n")
        gpd_params = genpareto.fit(self.data, floc=0)
        self.result.append(str(gpd_params) + '\


import pandas as pd
from scipy.stats import beta, ev, genpareto
from PyQt5 import QtWidgets, QtGui, QtCore

class DistributionFitter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Distribution Fitter")
        self.setGeometry(300, 300, 300, 300)

        # Create distribution selection combo box
        self.distribution_label = QtWidgets.QLabel("Select distribution:", self)
        self.distribution_label.move(10, 10)
        self.distribution_combo = QtWidgets.QComboBox(self)
        self.distribution_combo.addItem("Beta")
        self.distribution_combo.addItem("Extreme Value")
        self.distribution_combo.addItem("Generalized Pareto")
        self.distribution_combo.move(10, 30)

        # Create file selection button
        self.file_button = QtWidgets.QPushButton("Select file", self)
        self.file_button.move(10, 60)
        self.file_button.clicked.connect(self.select_file)

        # Create fit button
        self.fit_button = QtWidgets.QPushButton("Fit", self)
        self.fit_button.move(10, 90)
        self.fit_button.clicked.connect(self.fit)
        
        self.show()
        
    def select_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        self.file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if self.file_name:
            self.data = pd.read_csv(self.file_name)
            
    def fit(self):
        distribution = self.distribution_combo.currentText()
        
        if distribution == "Beta":
            self.fit_beta()
        elif distribution == "Extreme Value":
            self.fit_ev()
        elif distribution == "Generalized Pareto":
            self.fit_genpareto()
            
    def fit_beta(self):
        a, b, _, _ = beta.fit(self.data)
        print("Beta Distribution - a: {}, b: {}".format(a, b))
        
    def fit_ev(self):
        c, loc, scale = ev.fit(self.data)
        print("Extreme Value Distribution - c: {}, loc: {}, scale: {}".format(c, loc, scale))
        
    def fit_genpareto(self):
        c, loc,