import sys

from colour import RGB_COLOURSPACES
from Gamut import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
# from PyQt5.Qt import Qt, QApplication, QClipboard

import numpy as np
import matplotlib.pyplot as plt
from colour.plotting import ( 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931, 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1976UCS,
)
import colour
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
        self.ui.pB_calculate.clicked.connect(self.calculate)
        self.ui.cb_bt2020.stateChanged.connect(self.f_2020)
        self.ui.cb_ntcs1953.stateChanged.connect(self.f_ntsc)
        self.ui.cb_srgb.stateChanged.connect(self.f_srgb)
        self.ui.cb_adobe.stateChanged.connect(self.f_adobe)
        self.calculate_reference = True



    def load_table(self, clrspace):
        table_row = 0
        for item in RGB_COLOURSPACES[clrspace].primaries:
            self.ui.tW_reference.setItem(table_row,0,QTableWidgetItem(str(item[0])))
            self.ui.tW_reference.setItem(table_row,1,QTableWidgetItem(str(item[1])))
            table_row +=1
        self.ui.tW_reference.setItem(3,0,QTableWidgetItem(str(RGB_COLOURSPACES[clrspace].whitepoint[0])))
        self.ui.tW_reference.setItem(3,1,QTableWidgetItem(str(RGB_COLOURSPACES[clrspace].whitepoint[1])))
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
        else:
            self.ui.le_reference_name.setEnabled(True)
            self.calculate_reference = True
            self.ui.tW_reference.clearContents()
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
        else:
            self.ui.le_reference_name.setEnabled(True)
            self.calculate_reference = True
            self.ui.tW_reference.clearContents()
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
        else:
            self.ui.le_reference_name.setEnabled(True)
            self.calculate_reference = True
            self.ui.tW_reference.clearContents()
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
        else:
            self.ui.le_reference_name.setEnabled(True)
            self.calculate_reference = True
            self.ui.tW_reference.clearContents()


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

            # Get primary RGB xy coordinates from table widget cells
            PRIMARIES_SAMPLE = np.array(
                [
                    [float(self.ui.tW_sample.item(0, 0).text()), float(self.ui.tW_sample.item(0, 1).text())],   #R
                    [float(self.ui.tW_sample.item(1, 0).text()), float(self.ui.tW_sample.item(1, 1).text())],   #G
                    [float(self.ui.tW_sample.item(2, 0).text()), float(self.ui.tW_sample.item(2, 1).text())],   #B
                ]
            )
            # Get primary RGB xy coordinates from table widget cells
            
            # Get whitepoint xy coordinates from table widget cells and decide whether to show whitepoint or not        
            if type(self.ui.tW_sample.item(3,0)) == QTableWidgetItem and type(self.ui.tW_sample.item(3,1)) == QTableWidgetItem:
                if self.ui.tW_sample.item(3, 0).text().strip() != "" and self.ui.tW_sample.item(3, 1).text().strip() != "":
                    if (float(self.ui.tW_sample.item(3, 0).text()) < 0.9) and (float(self.ui.tW_sample.item(3, 0).text()) > 0) and (float(self.ui.tW_sample.item(3, 1).text()) < 0.9) and (float(self.ui.tW_sample.item(3, 1).text()) > 0):
                        CCS_WHITEPOINT_SAMPLE = np.array([float(self.ui.tW_sample.item(3, 0).text()), float(self.ui.tW_sample.item(3, 1).text())])
                        self.wp_s_bool = True
                else:
                    self.wp_s_bool = False
                    CCS_WHITEPOINT_SAMPLE = np.array([0.3,0.3]) 
            else:
                self.wp_s_bool = False
                CCS_WHITEPOINT_SAMPLE = np.array([0.3,0.3])     # Values not important. Whitepoint won't show.
            # Get whitepoint xy coordinates from table widget cells and decide whether to show whitepoint or not  

            # Get sample name name from line edit form and set generic name if empty
            if self.ui.le_sample_name.text().strip() != "":
                WHITEPOINT_NAME_SAMPLE = self.ui.le_sample_name.text()
            else:
                WHITEPOINT_NAME_SAMPLE = "Sample"
            # Get sample name name from line edit form and set generic name if empty

            # Initialize an RGB_Colourspace object from colour-science module with the data above
            self.sample_RGB.user_RGB_primaries(
                PRIMARIES_SAMPLE = PRIMARIES_SAMPLE,
                CCS_WHITEPOINT_SAMPLE = CCS_WHITEPOINT_SAMPLE,
                WHITEPOINT_NAME_SAMPLE = WHITEPOINT_NAME_SAMPLE
            )
            # Initialize an RGB_Colourspace object from colour-science module with the data above
        def calculate_reference_xy():
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

            # Get primary RGB xy coordinates from table widget cells
            PRIMARIES_SAMPLE = np.array(
                [
                    [float(self.ui.tW_reference.item(0, 0).text()), float(self.ui.tW_reference.item(0, 1).text())],   #R
                    [float(self.ui.tW_reference.item(1, 0).text()), float(self.ui.tW_reference.item(1, 1).text())],   #G
                    [float(self.ui.tW_reference.item(2, 0).text()), float(self.ui.tW_reference.item(2, 1).text())],   #B
                ]
            )
            # Get primary RGB xy coordinates from table widget cells
            
            # Get whitepoint xy coordinates from table widget cells and decide whether to show whitepoint or not        
            if type(self.ui.tW_reference.item(3,0)) == QTableWidgetItem and type(self.ui.tW_reference.item(3,1)) == QTableWidgetItem:
                if self.ui.tW_reference.item(3, 0).text().strip() != "" and self.ui.tW_reference.item(3, 1).text().strip() != "":
                    if (float(self.ui.tW_reference.item(3, 0).text()) < 0.9) and (float(self.ui.tW_reference.item(3, 0).text()) > 0) and (float(self.ui.tW_reference.item(3, 1).text()) < 0.9) and (float(self.ui.tW_reference.item(3, 1).text()) > 0):
                        CCS_WHITEPOINT_SAMPLE = np.array([float(self.ui.tW_reference.item(3, 0).text()), float(self.ui.tW_reference.item(3, 1).text())])
                        self.wp_r_bool = True
                else:
                    self.wp_r_bool = False
                    CCS_WHITEPOINT_SAMPLE = np.array([0.3,0.3]) 
            else:
                self.wp_r_bool = False
                CCS_WHITEPOINT_SAMPLE = np.array([0.3,0.3])     # Values not important. Whitepoint won't show.
            # Get whitepoint xy coordinates from table widget cells and decide whether to show whitepoint or not  

            # Get sample name name from line edit form and set generic name if empty
            if self.ui.le_sample_name.text().strip() != "":
                WHITEPOINT_NAME_SAMPLE = self.ui.le_reference_name.text()
            else:
                WHITEPOINT_NAME_SAMPLE = "Reference"
            # Get sample name name from line edit form and set generic name if empty

            # Initialize an RGB_Colourspace object from colour-science module with the data above
            self.reference_RGB.user_RGB_primaries(
                PRIMARIES_SAMPLE = PRIMARIES_SAMPLE,
                CCS_WHITEPOINT_SAMPLE = CCS_WHITEPOINT_SAMPLE,
                WHITEPOINT_NAME_SAMPLE = WHITEPOINT_NAME_SAMPLE
            )
            # Initialize an RGB_Colourspace object from colour-science module with the data above

            self.reference_RGBcolourspace = self.reference_RGB.RGB_COLOURSPACE_SAMPLE
        
        calculate_user_xy()
        if self.calculate_reference:
            calculate_reference_xy()
        self.compare_area()
        self.gamut_coverage()
        self.ui.textBrowser.setText(f"Area ratio: %{self.ratio}\nCoverage: %{self.coverage}")
        # Plot colourspace diagrams
        if self.reference_RGBcolourspace == "NTSC (1953)":
            self.reference_RGBcolourspace = "NTSC \\(1953\\)"
        self.wp_bool = self.wp_r_bool and self.wp_s_bool
        plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931([self.reference_RGBcolourspace, self.sample_RGB.RGB_COLOURSPACE_SAMPLE], show_whitepoints = self.wp_bool, standalone = True)
    ##
    # THE METHOD FOR CALCULATIONS BASED ON THE COORDINATES ENTERED INTO TABLE
    ##

    # ALAN HESAPLAMA:
    def compare_area(self):
        sample_A = area.sample_area(self.sample_RGB.RGB_COLOURSPACE_SAMPLE)
        if self.calculate_reference:
            reference_A = area.sample_area(self.reference_RGBcolourspace) #(self.reference_RGB.RGB_COLOURSPACE_SAMPLE)
        else:
            reference_A = area.Areas_Colourspaces[self.reference_RGBcolourspace]
        self.ratio = (sample_A / reference_A)*100
        # print(f"Örnek Alan: {sample_A} \nbt2020 Alan: {reference_A}")
        # print(f"Alanlar Oranı %{self.ratio}")
  
    # ALAN HESAPLAMA

    # COVERAGE HESAPLAMA:
    def gamut_coverage(self):        
        sample_p = area.sample_points(self.sample_RGB.RGB_COLOURSPACE_SAMPLE)
        if self.calculate_reference:
            reference_p = area.sample_points(self.reference_RGBcolourspace)
        else:    
            reference_p = points_database.Points_Colourspaces[self.reference_RGBcolourspace]
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



# sample_RGB = sample.RGB_primaries()


# self.wp_bool = False
# plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(['ITU-R BT.2020', sample_RGB.RGB_COLOURSPACE_SAMPLE_user], show_whitepoints = self.wp_bool, standalone = False)
# # Show White point
# # if self.wp_bool:
# #     plt.plot(sample_RGB.w_xy[0],sample_RGB.w_xy[1],"o")
# #Show White point
# # plt.plot(sample_RGB.r_xy[0],sample_RGB.r_xy[1],"o")
# # plt.plot(sample_RGB.g_xy[0],sample_RGB.g_xy[1],"o")
# # plt.plot(sample_RGB.b_xy[0],sample_RGB.b_xy[1],"o")
# plt.show()

# # plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(['ITU-R BT.2020', sample.RGB_COLOURSPACE_SAMPLE])

# # plot_RGB_colourspaces_in_chromaticity_diagram_CIE1976UCS(['ITU-R BT.2020', sample.RGB_COLOURSPACE_SAMPLE])

# pyuic5 Gamut.ui -o Gamut.py