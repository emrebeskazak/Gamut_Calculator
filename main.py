import sys

from colour import RGB_COLOURSPACES
from Gamut import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
# from PyQt5.Qt import Qt, QApplication, QClipboard

import numpy as np
# import matplotlib.pyplot as plt
from colour.plotting import ( 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931, 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1976UCS,
)
from colour.models import  (
    xy_to_Luv_uv,
    Luv_uv_to_xy
)
# import colour
import sample
import area
import points_database

# # RGB Colourspaces keys list: #
# import colour.models
# from pprint import pprint
# # pprint(sorted(colour.models.RGB_COLOURSPACES.keys()))
# pprint(RGB_COLOURSPACES["NTSC \\(1953\\)"])

class Gamut_win(QtWidgets.QMainWindow):
    def __init__(self):
        super(Gamut_win, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.sample_RGB = sample.RGB_primaries()
        self.reference_RGB = sample.RGB_primaries()
        # Radio button initial settings
        self.ui.rB_table_s.setChecked(True)
        self.ui.groupBox_import_sample.setEnabled(False)
        self.ui.rB_table_r.setChecked(True)
        self.ui.groupBox_import_reference.setEnabled(False)
        # Radio button initial settings
        self.ui.pB_calculate.clicked.connect(self.calculate)
        self.ui.cb_bt2020.stateChanged.connect(self.f_2020)
        self.ui.cb_ntcs1953.stateChanged.connect(self.f_ntsc)
        self.ui.cb_srgb.stateChanged.connect(self.f_srgb)
        self.ui.cb_adobe.stateChanged.connect(self.f_adobe)
        self.calculate_reference = True
        self.ui.rB_table_s.toggled.connect(self.f_table_s)
        self.ui.rB_file_s.toggled.connect(self.f_file_s)
        self.ui.rB_table_r.toggled.connect(self.f_table_r)
        self.ui.rB_file_r.toggled.connect(self.f_file_r)  
        self.ui.pb_browse_sample.clicked.connect(self.f_browse_sample)
        self.ui.pb_browse_reference.clicked.connect(self.f_browse_reference)
        self.ui.pb_browse_sample_filter.clicked.connect(self.f_browse_sample_filter)
        self.ui.pb_browse_reference_filter.clicked.connect(self.f_browse_reference_filter)
        self.ui.rb_1931.toggled.connect(self.f_1931)
        self.ui.rb_1976.toggled.connect(self.f_1976)
        self.xy = True
        self.ui.actionAbout.triggered.connect(self.about)

    def about(self):
        msg = QtWidgets.QMessageBox()
        msg.setTextFormat(Qt.RichText)  
        # msg.about(self, "About", "Gamut Calculator\nVersion: 1.0\n\nNo rights reserved at all cCc\n<a href='http://google.com/'>Google</a>")
        icon = QIcon()
        icon.addPixmap(QPixmap("icon.jpg"), QIcon.Normal, QIcon.Off)
        msg.setWindowIcon(icon)
        msg.setWindowTitle("About")
        msg.setIconPixmap(QPixmap("icon.jpg"))
        msg.setText('<p><span style="color:#0000a0"><span style="font-size:22px">Gamut Calculator</span></span><br><span style="font-size:15px">Version 1.0</span></p><p><span style="font-size:15px">Written in Python by using open source modules <br>by <br>Emre Beşkazak</span></p><p><span style="font-size:15px">Source code:</span><br><a href="https://github.com/emrebeskazak/Gamut_Calculator">GitHub</a></p>')
        x = msg.exec_()
              
    
    def f_browse_sample(self):
        self.ui.le_browse_sample.setText(QFileDialog.getOpenFileName()[0])
    def f_browse_reference(self):
        self.ui.le_browse_reference.setText(QFileDialog.getOpenFileName()[0])
    def f_browse_sample_filter(self):
        self.ui.le_browse_sample_filter.setText(QFileDialog.getOpenFileName()[0])
    def f_browse_reference_filter(self):
        self.ui.le_browse_reference_filter.setText(QFileDialog.getOpenFileName()[0])

    def f_1931(self):
        self.xy = True
        if self.ui.tW_sample.horizontalHeaderItem(0).text() == "u":
            item = self.ui.tW_sample.horizontalHeaderItem(0)
            item.setText("x")
            item = self.ui.tW_sample.horizontalHeaderItem(1)
            item.setText("y")
        if self.ui.tW_reference.horizontalHeaderItem(0).text() == "u":
            item = self.ui.tW_reference.horizontalHeaderItem(0)
            item.setText("x")
            item = self.ui.tW_reference.horizontalHeaderItem(1)
            item.setText("y")
    def f_1976(self):
        self.xy = False
      
    def f_table_s(self):
        if self.sender().isChecked():
            self.ui.tW_sample.setEnabled(True)
            self.ui.groupBox_import_sample.setEnabled(False)
            if self.ui.tW_sample.horizontalHeaderItem(0).text() == "u":
                item = self.ui.tW_sample.horizontalHeaderItem(0)
                item.setText("x")
                item = self.ui.tW_sample.horizontalHeaderItem(1)
                item.setText("y")
    def f_file_s(self):
        if self.sender().isChecked():
            self.ui.tW_sample.setEnabled(False)
            self.ui.groupBox_import_sample.setEnabled(True)
    def f_table_r(self):
        if self.sender().isChecked():
            self.ui.tW_reference.setEnabled(True)
            self.ui.groupBox_import_reference.setEnabled(False)
            if self.ui.tW_reference.horizontalHeaderItem(0).text() == "u":
                item = self.ui.tW_reference.horizontalHeaderItem(0)
                item.setText("x")
                item = self.ui.tW_reference.horizontalHeaderItem(1)
                item.setText("y")
    def f_file_r(self):
        if self.sender().isChecked():
            self.ui.tW_reference.setEnabled(False)
            self.ui.cb_adobe.setChecked(False)
            self.ui.cb_bt2020.setChecked(False)
            self.ui.cb_ntcs1953.setChecked(False)
            self.ui.cb_srgb.setChecked(False)
            self.ui.groupBox_import_reference.setEnabled(True)
   
    def load_table(self, clrspace):
        table_row = 0
        for item in RGB_COLOURSPACES[clrspace].primaries:
            if self.xy:
                self.ui.tW_reference.setItem(table_row,0,QTableWidgetItem(str(item[0])))
                self.ui.tW_reference.setItem(table_row,1,QTableWidgetItem(str(item[1])))
            else:
                item = xy_to_Luv_uv(item)
                self.ui.tW_reference.setItem(table_row,0,QTableWidgetItem(str(item[0])))
                self.ui.tW_reference.setItem(table_row,1,QTableWidgetItem(str(item[1])))
            table_row +=1
        if self.xy:
            self.ui.tW_reference.setItem(3,0,QTableWidgetItem(str(RGB_COLOURSPACES[clrspace].whitepoint[0])))
            self.ui.tW_reference.setItem(3,1,QTableWidgetItem(str(RGB_COLOURSPACES[clrspace].whitepoint[1])))
        else:
            self.ui.tW_reference.setItem(3,0,QTableWidgetItem(str(xy_to_Luv_uv(RGB_COLOURSPACES[clrspace].whitepoint)[0])))
            self.ui.tW_reference.setItem(3,1,QTableWidgetItem(str(xy_to_Luv_uv(RGB_COLOURSPACES[clrspace].whitepoint)[1])))        
    def f_2020(self):
        if self.sender().isChecked():
            self.ui.cb_ntcs1953.setChecked(False)
            self.ui.cb_srgb.setChecked(False)
            self.ui.cb_adobe.setChecked(False)
            self.ui.le_reference_name.setEnabled(False)
            self.reference_RGBcolourspace = 'ITU-R BT.2020'
            self.calculate_reference = False
            self.load_table(self.reference_RGBcolourspace)
            self.wp_r_bool = True
            self.ui.tW_reference.setEnabled(True)
            self.ui.rB_table_r.setChecked(True)
            if not self.xy:
                if self.ui.tW_reference.horizontalHeaderItem(0).text() == "x":
                    item = self.ui.tW_reference.horizontalHeaderItem(0)
                    item.setText("u")
                    item = self.ui.tW_reference.horizontalHeaderItem(1)
                    item.setText("v")                
        else:
            self.ui.le_reference_name.setEnabled(True)
            self.calculate_reference = True
            self.ui.tW_reference.clearContents()
            if self.ui.tW_reference.horizontalHeaderItem(0).text() == "u":
                item = self.ui.tW_reference.horizontalHeaderItem(0)
                item.setText("x")
                item = self.ui.tW_reference.horizontalHeaderItem(1)
                item.setText("y")
    def f_ntsc(self):
        if self.sender().isChecked():
            self.ui.cb_bt2020.setChecked(False)
            self.ui.cb_srgb.setChecked(False)
            self.ui.cb_adobe.setChecked(False)
            self.ui.le_reference_name.setEnabled(False)
            self.reference_RGBcolourspace = "NTSC (1953)"
            self.calculate_reference = False
            self.load_table(self.reference_RGBcolourspace)
            self.wp_r_bool = True
            self.ui.tW_reference.setEnabled(True)
            self.ui.rB_table_r.setChecked(True)
            if not self.xy:
                if self.ui.tW_reference.horizontalHeaderItem(0).text() == "x":
                    item = self.ui.tW_reference.horizontalHeaderItem(0)
                    item.setText("u")
                    item = self.ui.tW_reference.horizontalHeaderItem(1)
                    item.setText("v")              
        else:
            self.ui.le_reference_name.setEnabled(True)
            self.calculate_reference = True
            self.ui.tW_reference.clearContents()
            if self.ui.tW_reference.horizontalHeaderItem(0).text() == "u":
                item = self.ui.tW_reference.horizontalHeaderItem(0)
                item.setText("x")
                item = self.ui.tW_reference.horizontalHeaderItem(1)
                item.setText("y")
    def f_srgb(self):
        if self.sender().isChecked():
            self.ui.cb_bt2020.setChecked(False)
            self.ui.cb_ntcs1953.setChecked(False)
            self.ui.cb_adobe.setChecked(False)
            self.ui.le_reference_name.setEnabled(False)
            self.reference_RGBcolourspace = "sRGB"
            self.calculate_reference = False
            self.load_table(self.reference_RGBcolourspace)
            self.wp_r_bool = True
            self.ui.tW_reference.setEnabled(True)
            self.ui.rB_table_r.setChecked(True)
            if not self.xy:
                if self.ui.tW_reference.horizontalHeaderItem(0).text() == "x":
                    item = self.ui.tW_reference.horizontalHeaderItem(0)
                    item.setText("u")
                    item = self.ui.tW_reference.horizontalHeaderItem(1)
                    item.setText("v")  
        else:
            self.ui.le_reference_name.setEnabled(True)
            self.calculate_reference = True
            self.ui.tW_reference.clearContents()
            if self.ui.tW_reference.horizontalHeaderItem(0).text() == "u":
                item = self.ui.tW_reference.horizontalHeaderItem(0)
                item.setText("x")
                item = self.ui.tW_reference.horizontalHeaderItem(1)
                item.setText("y")
    def f_adobe(self):
        if self.sender().isChecked():
            self.ui.cb_bt2020.setChecked(False)
            self.ui.cb_ntcs1953.setChecked(False)
            self.ui.cb_srgb.setChecked(False)
            self.ui.le_reference_name.setEnabled(False)
            self.reference_RGBcolourspace = 'adobe1998'
            self.calculate_reference = False
            self.load_table(self.reference_RGBcolourspace)
            self.wp_r_bool = True
            self.ui.tW_reference.setEnabled(True)
            self.ui.rB_table_r.setChecked(True)
            if not self.xy:
                if self.ui.tW_reference.horizontalHeaderItem(0).text() == "x":
                    item = self.ui.tW_reference.horizontalHeaderItem(0)
                    item.setText("u")
                    item = self.ui.tW_reference.horizontalHeaderItem(1)
                    item.setText("v")  
        else:
            self.ui.le_reference_name.setEnabled(True)
            self.calculate_reference = True
            self.ui.tW_reference.clearContents()
            if self.ui.tW_reference.horizontalHeaderItem(0).text() == "u":
                item = self.ui.tW_reference.horizontalHeaderItem(0)
                item.setText("x")
                item = self.ui.tW_reference.horizontalHeaderItem(1)
                item.setText("y")


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.cntrl = True
        # Ctrl + V Paste code for tabel widget
        elif event.key() == Qt.Key_V:
            if self.cntrl:
                if self.ui.tW_sample.hasFocus():
                    text = QtWidgets.QApplication.clipboard().text()
                    text = text.splitlines()
                    if len(text) > 1:
                        table_row = 0
                        for line in text:
                            l_tuple = line.strip().partition("\t")
                            self.ui.tW_sample.setItem(table_row,0,QTableWidgetItem(l_tuple[0].strip()))
                            self.ui.tW_sample.setItem(table_row,1,QTableWidgetItem(l_tuple[2].strip()))
                            table_row +=1
                    else:
                        l_tuple = text[0].strip().partition("\t")
                        self.ui.tW_sample.setItem(self.ui.tW_sample.currentRow(),self.ui.tW_sample.currentColumn(),QTableWidgetItem(l_tuple[0].strip()))
                elif self.ui.tW_reference.hasFocus():  
                    text = QtWidgets.QApplication.clipboard().text()
                    text = text.splitlines()
                    if len(text) > 1:
                        table_row = 0
                        for line in text:
                            l_tuple = line.strip().partition("\t")
                            self.ui.tW_reference.setItem(table_row,0,QTableWidgetItem(l_tuple[0].strip()))
                            self.ui.tW_reference.setItem(table_row,1,QTableWidgetItem(l_tuple[2].strip()))
                            table_row +=1
                    else:
                        l_tuple = text[0].strip().partition("\t")
                        self.ui.tW_reference.setItem(self.ui.tW_reference.currentRow(),self.ui.tW_reference.currentColumn(),QTableWidgetItem(l_tuple[0].strip()))                         
        # Ctrl + C Copy code for table widget
        elif event.key() == Qt.Key_C:
            if self.cntrl:
                if self.ui.tW_sample.hasFocus():
                    QtWidgets.QApplication.clipboard().setText(f"{self.ui.tW_sample.item(0, 0).text()}\t{self.ui.tW_sample.item(0, 1).text()}\n{self.ui.tW_sample.item(1, 0).text()}\t{self.ui.tW_sample.item(1, 1).text()}\n{self.ui.tW_sample.item(2, 0).text()}\t{self.ui.tW_sample.item(2, 1).text()}\n{self.ui.tW_sample.item(3, 0).text()}\t{self.ui.tW_sample.item(3, 1).text()}")
                if self.ui.tW_reference.hasFocus():    
                    QtWidgets.QApplication.clipboard().setText(f"{self.ui.tW_reference.item(0, 0).text()}\t{self.ui.tW_reference.item(0, 1).text()}\n{self.ui.tW_reference.item(1, 0).text()}\t{self.ui.tW_reference.item(1, 1).text()}\n{self.ui.tW_reference.item(2, 0).text()}\t{self.ui.tW_reference.item(2, 1).text()}\n{self.ui.tW_reference.item(3, 0).text()}\t{self.ui.tW_reference.item(3, 1).text()}")
        elif event.key() == Qt.Key_Delete:
            if self.ui.tW_sample.hasFocus():
                self.ui.tW_sample.setItem(self.ui.tW_sample.currentRow(),self.ui.tW_sample.currentColumn(),QTableWidgetItem(""))
            if self.ui.tW_reference.hasFocus():
                self.ui.tW_reference.setItem(self.ui.tW_reference.currentRow(),self.ui.tW_reference.currentColumn(),QTableWidgetItem(""))

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.cntrl =False
    ##
    # THE METHOD FOR CALCULATIONS BASED ON THE COORDINATES ENTERED INTO TABLE
    ##
    def calculate(self):
        def calculate_user_xy():
            if self.ui.rB_file_s.isChecked():
                # Get sample name name from line edit form or set generic name if empty
                if self.ui.le_sample_name.text().strip() != "":
                    WHITEPOINT_NAME_SAMPLE = self.ui.le_sample_name.text()
                else:
                    WHITEPOINT_NAME_SAMPLE = "Sample"
                # Get sample name name from line edit form or set generic name if empty
                self.sample_RGB.file_RGB_primaries(
                    file_path = self.ui.le_browse_sample.text(),
                    WHITEPOINT_NAME = WHITEPOINT_NAME_SAMPLE,
                    filter_path = self.ui.le_browse_sample_filter.text(),
                    filter_bool = self.ui.groupBox_sample_filter.isChecked()
                    )
                self.wp_s_bool = True

                # Load table
                self.ui.tW_sample.setEnabled(True)
                table_row = 0
                for item in self.sample_RGB.RGB_COLOURSPACE_SAMPLE.primaries:
                    if self.xy:
                        self.ui.tW_sample.setItem(table_row,0,QTableWidgetItem(str(item[0])))
                        self.ui.tW_sample.setItem(table_row,1,QTableWidgetItem(str(item[1])))
                    else:
                        item = xy_to_Luv_uv(item)
                        self.ui.tW_sample.setItem(table_row,0,QTableWidgetItem(str(item[0])))
                        self.ui.tW_sample.setItem(table_row,1,QTableWidgetItem(str(item[1])))
                    table_row +=1
                if self.xy:
                    self.ui.tW_sample.setItem(3,0,QTableWidgetItem(str(self.sample_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint[0])))
                    self.ui.tW_sample.setItem(3,1,QTableWidgetItem(str(self.sample_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint[1])))
                else:
                    self.ui.tW_sample.setItem(3,0,QTableWidgetItem(str(xy_to_Luv_uv(self.sample_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint)[0])))
                    self.ui.tW_sample.setItem(3,1,QTableWidgetItem(str(xy_to_Luv_uv(self.sample_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint)[1])))                   
                # Load table

            elif self.ui.rB_table_s.isChecked():
                # Check table values if empty and between 0 and 0.9
                table_y =0
                while table_y <= 1:
                    table_x =0
                    while table_x <=2:
                        if (self.ui.tW_sample.item(table_x, table_y).text().strip() != "") and (float(self.ui.tW_sample.item(table_x, table_y).text()) < 0.9) and (float(self.ui.tW_sample.item(table_x, table_y).text()) > 0):
                            # print(f"pass ({table_x}, {table_y})")
                            pass
                        else:
                            print(f"Inappropriate table value at ({table_x}, {table_y})")
                        table_x +=1
                    table_y +=1
                # Check table values if empty and between 0 and 0.9

                # if self.xy:
                # Get primary RGB xy coordinates from table widget cells
                PRIMARIES_SAMPLE = np.array(
                    [
                        [float(self.ui.tW_sample.item(0, 0).text()), float(self.ui.tW_sample.item(0, 1).text())],   #R
                        [float(self.ui.tW_sample.item(1, 0).text()), float(self.ui.tW_sample.item(1, 1).text())],   #G
                        [float(self.ui.tW_sample.item(2, 0).text()), float(self.ui.tW_sample.item(2, 1).text())],   #B
                    ]
                )
                # Get primary RGB xy coordinates from table widget cells
                # else:
                #     # Get primary RGB uv coordinates from table widget cells
                #     PRIMARIES_SAMPLE = np.array(
                #         [
                #             Luv_uv_to_xy(np.array([float(self.ui.tW_sample.item(0, 0).text()), float(self.ui.tW_sample.item(0, 1).text())])),   #R
                #             Luv_uv_to_xy(np.array([float(self.ui.tW_sample.item(1, 0).text()), float(self.ui.tW_sample.item(1, 1).text())])),   #G
                #             Luv_uv_to_xy(np.array([float(self.ui.tW_sample.item(2, 0).text()), float(self.ui.tW_sample.item(2, 1).text())])),   #B
                #         ]
                #     )
                #     # Get primary RGB uv coordinates from table widget cells
                
                # Get whitepoint xy coordinates from table widget cells and decide whether to show whitepoint or not        
                if type(self.ui.tW_sample.item(3,0)) == QTableWidgetItem and type(self.ui.tW_sample.item(3,1)) == QTableWidgetItem:
                    if self.ui.tW_sample.item(3, 0).text().strip() != "" and self.ui.tW_sample.item(3, 1).text().strip() != "":
                        if (float(self.ui.tW_sample.item(3, 0).text()) < 0.9) and (float(self.ui.tW_sample.item(3, 0).text()) > 0) and (float(self.ui.tW_sample.item(3, 1).text()) < 0.9) and (float(self.ui.tW_sample.item(3, 1).text()) > 0):
                            # if self.xy:
                            CCS_WHITEPOINT_SAMPLE = np.array([float(self.ui.tW_sample.item(3, 0).text()), float(self.ui.tW_sample.item(3, 1).text())])
                            # else:
                            #     CCS_WHITEPOINT_SAMPLE = Luv_uv_to_xy(np.array([float(self.ui.tW_sample.item(3, 0).text()), float(self.ui.tW_sample.item(3, 1).text())]))
                            self.wp_s_bool = True
                    else:
                        self.wp_s_bool = False
                        CCS_WHITEPOINT_SAMPLE = np.array([0.3,0.3]) 
                else:
                    self.wp_s_bool = False
                    CCS_WHITEPOINT_SAMPLE = np.array([0.3,0.3])     # Values not important. Whitepoint won't show.
                # Get whitepoint xy coordinates from table widget cells and decide whether to show whitepoint or not  

                # Get sample name name from line edit form or set generic name if empty
                if self.ui.le_sample_name.text().strip() != "":
                    WHITEPOINT_NAME_SAMPLE = self.ui.le_sample_name.text()
                else:
                    WHITEPOINT_NAME_SAMPLE = "Sample"
                # Get sample name name from line edit form or set generic name if empty

                # Initialize an RGB_Colourspace object from colour-science module with the data above
                self.sample_RGB.user_RGB_primaries(
                    PRIMARIES = PRIMARIES_SAMPLE,
                    CCS_WHITEPOINT = CCS_WHITEPOINT_SAMPLE,
                    WHITEPOINT_NAME = WHITEPOINT_NAME_SAMPLE
                )
                # Initialize an RGB_Colourspace object from colour-science module with the data above

                # Reload handwritten table if uv calculation is done
                if not self.xy:
                    table_row = 0
                    for item in self.sample_RGB.RGB_COLOURSPACE_SAMPLE.primaries:
                        item = xy_to_Luv_uv(item)
                        self.ui.tW_sample.setItem(table_row,0,QTableWidgetItem(str(item[0])))
                        self.ui.tW_sample.setItem(table_row,1,QTableWidgetItem(str(item[1])))
                        table_row +=1
                    self.ui.tW_sample.setItem(3,0,QTableWidgetItem(str(xy_to_Luv_uv(self.sample_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint)[0])))
                    self.ui.tW_sample.setItem(3,1,QTableWidgetItem(str(xy_to_Luv_uv(self.sample_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint)[1])))                   
                # Reload handwritten table if uv calculation is done

        def calculate_reference_xy():
            if self.ui.rB_file_r.isChecked():
                # Get sample name name from line edit form or set generic name if empty
                if self.ui.le_reference_name.text().strip() != "":
                    WHITEPOINT_NAME_SAMPLE = self.ui.le_reference_name.text()
                else:
                    WHITEPOINT_NAME_SAMPLE = "Reference"
                # Get sample name name from line edit form or set generic name if empty
                self.reference_RGB.file_RGB_primaries(
                    file_path = self.ui.le_browse_reference.text(),
                    WHITEPOINT_NAME = WHITEPOINT_NAME_SAMPLE,
                    filter_path = self.ui.le_browse_reference_filter.text(),
                    filter_bool = self.ui.groupBox_reference_filter.isChecked()
                    )
                self.wp_r_bool = True

                # Load table
                self.ui.tW_reference.setEnabled(True)
                table_row = 0
                for item in self.reference_RGB.RGB_COLOURSPACE_SAMPLE.primaries:
                    if self.xy:
                        self.ui.tW_reference.setItem(table_row,0,QTableWidgetItem(str(item[0])))
                        self.ui.tW_reference.setItem(table_row,1,QTableWidgetItem(str(item[1])))
                    else:
                        item = xy_to_Luv_uv(item)
                        self.ui.tW_reference.setItem(table_row,0,QTableWidgetItem(str(item[0])))
                        self.ui.tW_reference.setItem(table_row,1,QTableWidgetItem(str(item[1])))                        
                    table_row +=1
                if self.xy:
                    self.ui.tW_reference.setItem(3,0,QTableWidgetItem(str(self.reference_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint[0])))
                    self.ui.tW_reference.setItem(3,1,QTableWidgetItem(str(self.reference_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint[1])))
                else:
                    self.ui.tW_reference.setItem(3,0,QTableWidgetItem(str(xy_to_Luv_uv(self.reference_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint)[0])))
                    self.ui.tW_reference.setItem(3,1,QTableWidgetItem(str(xy_to_Luv_uv(self.reference_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint)[1])))
                # Load table

            elif self.ui.rB_table_r.isChecked():            
                # Check table values if empty and between 0 and 0.9
                table_y =0
                while table_y <= 1:
                    table_x =0
                    while table_x <=2:
                        if (self.ui.tW_reference.item(table_x, table_y).text().strip() != "") and (float(self.ui.tW_reference.item(table_x, table_y).text()) < 0.9) and (float(self.ui.tW_reference.item(table_x, table_y).text()) > 0):
                            # print(f"pass ({table_x}, {table_y})")
                            pass
                        else:
                            print(f"Inappropriate table value at ({table_x}, {table_y})")
                        table_x +=1
                    table_y +=1
                # Check table values if empty and between 0 and 0.9

                # if self.xy:
                # Get primary RGB xy coordinates from table widget cells
                PRIMARIES_SAMPLE = np.array(
                    [
                        [float(self.ui.tW_reference.item(0, 0).text()), float(self.ui.tW_reference.item(0, 1).text())],   #R
                        [float(self.ui.tW_reference.item(1, 0).text()), float(self.ui.tW_reference.item(1, 1).text())],   #G
                        [float(self.ui.tW_reference.item(2, 0).text()), float(self.ui.tW_reference.item(2, 1).text())],   #B
                    ]
                )
                # Get primary RGB xy coordinates from table widget cells
                # else:
                #     # Get primary RGB uv coordinates from table widget cells
                #     PRIMARIES_SAMPLE = np.array(
                #         [
                #             Luv_uv_to_xy(np.array([float(self.ui.tW_reference.item(0, 0).text()), float(self.ui.tW_reference.item(0, 1).text())])),   #R
                #             Luv_uv_to_xy(np.array([float(self.ui.tW_reference.item(1, 0).text()), float(self.ui.tW_reference.item(1, 1).text())])),   #G
                #             Luv_uv_to_xy(np.array([float(self.ui.tW_reference.item(2, 0).text()), float(self.ui.tW_reference.item(2, 1).text())])),   #B
                #         ]
                #     )
                #     # Get primary RGB uv coordinates from table widget cells                
                # Get whitepoint xy coordinates from table widget cells and decide whether to show whitepoint or not        
                if type(self.ui.tW_reference.item(3,0)) == QTableWidgetItem and type(self.ui.tW_reference.item(3,1)) == QTableWidgetItem:
                    if self.ui.tW_reference.item(3, 0).text().strip() != "" and self.ui.tW_reference.item(3, 1).text().strip() != "":
                        if (float(self.ui.tW_reference.item(3, 0).text()) < 0.9) and (float(self.ui.tW_reference.item(3, 0).text()) > 0) and (float(self.ui.tW_reference.item(3, 1).text()) < 0.9) and (float(self.ui.tW_reference.item(3, 1).text()) > 0):
                            # if self.xy:
                            CCS_WHITEPOINT_SAMPLE = np.array([float(self.ui.tW_reference.item(3, 0).text()), float(self.ui.tW_reference.item(3, 1).text())])
                            # else:
                            #     CCS_WHITEPOINT_SAMPLE = Luv_uv_to_xy(np.array([float(self.ui.tW_reference.item(3, 0).text()), float(self.ui.tW_reference.item(3, 1).text())]))
                            self.wp_r_bool = True
                    else:
                        self.wp_r_bool = False
                        CCS_WHITEPOINT_SAMPLE = np.array([0.3,0.3]) 
                else:
                    self.wp_r_bool = False
                    CCS_WHITEPOINT_SAMPLE = np.array([0.3,0.3])     # Values not important. Whitepoint won't show.
                # Get whitepoint xy coordinates from table widget cells and decide whether to show whitepoint or not  

                # Get sample name name from line edit form or set generic name if empty
                if self.ui.le_reference_name.text().strip() != "":
                    WHITEPOINT_NAME_SAMPLE = self.ui.le_reference_name.text()
                else:
                    WHITEPOINT_NAME_SAMPLE = "Reference"
                # Get sample name name from line edit form or set generic name if empty

                # Initialize an RGB_Colourspace object from colour-science module with the data above
                self.reference_RGB.user_RGB_primaries(
                    PRIMARIES = PRIMARIES_SAMPLE,
                    CCS_WHITEPOINT = CCS_WHITEPOINT_SAMPLE,
                    WHITEPOINT_NAME = WHITEPOINT_NAME_SAMPLE
                )
                # Initialize an RGB_Colourspace object from colour-science module with the data above

                # Reload handwritten table if uv calculation is done
                if not self.xy:
                    table_row = 0
                    for item in self.reference_RGB.RGB_COLOURSPACE_SAMPLE.primaries:
                        item = xy_to_Luv_uv(item)
                        self.ui.tW_reference.setItem(table_row,0,QTableWidgetItem(str(item[0])))
                        self.ui.tW_reference.setItem(table_row,1,QTableWidgetItem(str(item[1])))                        
                        table_row +=1
                    self.ui.tW_reference.setItem(3,0,QTableWidgetItem(str(xy_to_Luv_uv(self.reference_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint)[0])))
                    self.ui.tW_reference.setItem(3,1,QTableWidgetItem(str(xy_to_Luv_uv(self.reference_RGB.RGB_COLOURSPACE_SAMPLE.whitepoint)[1])))
                # Reload handwritten table if uv calculation is done

            self.reference_RGBcolourspace = self.reference_RGB.RGB_COLOURSPACE_SAMPLE
        
        calculate_user_xy()
        if self.calculate_reference:
            calculate_reference_xy()
        
        if not self.xy:
            item = self.ui.tW_sample.horizontalHeaderItem(0)
            item.setText("u")
            item = self.ui.tW_sample.horizontalHeaderItem(1)
            item.setText("v")
            item = self.ui.tW_reference.horizontalHeaderItem(0)
            item.setText("u")
            item = self.ui.tW_reference.horizontalHeaderItem(1)
            item.setText("v")  
        
        # If not calculate reference (means one of the standard colourspaces is chosen) and not xy (uv), load table again
        if not self.calculate_reference and not self.xy:    
            self.load_table(self.reference_RGBcolourspace)
        self.compare_area()
        self.gamut_coverage()

        # Results text
        if self.xy:
            self.ui.textBrowser.setText(f"in CIE 1931 (xy) colorspace\nArea ratio: %{self.ratio}\nCoverage: %{self.coverage}")
        else:
            self.ui.textBrowser.setText(f"in CIE 1976 (uv) colorspace\nArea ratio: %{self.ratio}\nCoverage: %{self.coverage}")

        # Plot colourspace diagrams
        if self.reference_RGBcolourspace == "NTSC (1953)":
            self.reference_RGBcolourspace = "NTSC \\(1953\\)"
        self.wp_bool = self.wp_r_bool and self.wp_s_bool
        if self.xy:
            plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931([self.reference_RGBcolourspace, self.sample_RGB.RGB_COLOURSPACE_SAMPLE], show_whitepoints = self.wp_bool, standalone = True)
        else:
            plot_RGB_colourspaces_in_chromaticity_diagram_CIE1976UCS([self.reference_RGBcolourspace, self.sample_RGB.RGB_COLOURSPACE_SAMPLE], show_whitepoints = self.wp_bool, standalone = True)
        if self.reference_RGBcolourspace == "NTSC \\(1953\\)":
            self.reference_RGBcolourspace = "NTSC (1953)" 
    ##
    # THE METHOD FOR CALCULATIONS BASED ON THE COORDINATES ENTERED INTO TABLE
    ##

    # ALAN HESAPLAMA:
    def compare_area(self):
        sample_A = area.sample_area(self.sample_RGB.RGB_COLOURSPACE_SAMPLE, self.xy)
        if self.calculate_reference:
            reference_A = area.sample_area(self.reference_RGBcolourspace, self.xy) #(self.reference_RGB.RGB_COLOURSPACE_SAMPLE)
        else:
            if self.xy:
                reference_A = area.Areas_Colourspaces[self.reference_RGBcolourspace]
            else:
                reference_A = area.Areas_Colourspaces_uv[self.reference_RGBcolourspace]
        self.ratio = (sample_A / reference_A)*100
        # print(f"Örnek Alan: {sample_A} \nbt2020 Alan: {reference_A}")
        # print(f"Alanlar Oranı %{self.ratio}")
  
    # ALAN HESAPLAMA

    # COVERAGE HESAPLAMA:
    def gamut_coverage(self):        
        sample_p = area.sample_points(self.sample_RGB.RGB_COLOURSPACE_SAMPLE, self.xy)
        if self.calculate_reference:
            reference_p = area.sample_points(self.reference_RGBcolourspace, self.xy)
        else:
            if self.xy:    
                reference_p = points_database.Points_Colourspaces[self.reference_RGBcolourspace]
            else:
                reference_p = points_database.Points_Colourspaces_uv[self.reference_RGBcolourspace]
        counter = 0
        for p1 in sample_p:
            for p2 in reference_p:
                if ((p1[0] == p2 [0]) and (p1[1] == p2 [1])):
                    counter+=1
        # print(f"counter: {counter} \n length: {len(reference_p)}")
        self.coverage = (counter / len(reference_p))*100
        # print(f"Coverage: %{self.coverage}")
    # COVERAGE HESAPLAMA



app = QtWidgets.QApplication(sys.argv)
win = Gamut_win()

win.show()
sys.exit(app.exec_())


# pyuic5 Gamut.ui -o Gamut.py

