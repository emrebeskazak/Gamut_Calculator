import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from colour.models.rgb import (
    RGB_Colourspace,
    normalised_primary_matrix
)
from colour.models import XYZ_to_xy
from colour.colorimetry import (
    SpectralDistribution, 
    sd_to_XYZ, 
    sd_to_XYZ_integration, 
    sd_to_XYZ_ASTME308, 
    sd_to_XYZ_tristimulus_weighting_factors_ASTME308,
    sd_gaussian_fwhm
)
# import os
# import glob

# file_path = os.path.join(os.path.dirname(__file__), 'samples', 'sample1.*')

# for file_path_ext in glob.glob(file_path) :
#     with open(file_path_ext, "r") as file :
#         pass


class RGB_primaries:
    # def __init__(self):
    #     self.user_RGB_primaries()
    #     # self.file_RGB_primaries()
    
    # DOSYADAN OKUYUP KOORDİNAT HESAPLAYAN METHOD ###############
    def file_RGB_primaries(self, 
        file_path,
        WHITEPOINT_NAME,
        filter_path,
        filter_bool
        ):
        def data_to_xy(min = 360, max = 780):
            line_number = 0
            data_dict = {}
            detection = False
            while True:
                if file_list[line_number][1].isnumeric():
                    # if int(file_list[line_number][0:4]) >= min:
                    if detection == False:
                        if file_list[line_number].strip().find(";") != -1: 
                            partition_character = ";"
                            detection = True
                        elif file_list[line_number].strip().find(",") != -1: 
                            partition_character = ","
                            detection = True
                        elif file_list[line_number].strip().find(" ") != -1:
                            partition_character = " "
                            detection = True                               
                        else:
                            print ("Dosya çözülemedi!1")
                            break
                    line_tuple = file_list[line_number].strip().partition(partition_character)
                    # print(line_tuple)
                    # break
                    data_dict[float(line_tuple[0].strip())] = float(line_tuple[2].strip()) 
                    # if
                    # if int(file_list[line_number][0:4]) >= max:
                    #     break
                line_number += 1
                if line_number >= len(file_list):
                    # print ("Dosya çözülemedi!2")
                    break
            # print(data_dict)
            # print(list(data_dict.keys())[0])
            interval= list(data_dict.keys())[1] - list(data_dict.keys())[0]
            i=360
            while i<min:
                data_dict[i]=0
                i=i+interval
            j=max+1
            while j<=780:
                data_dict[j]=0
                j=j+interval
            # print(data_dict)
            data_sd = SpectralDistribution(data_dict)
            # data_sd_to_np = np.array([data_sd.wavelengths, data_sd.values])
            # print(data_sd_to_np.transpose())
            w_XYZ = sd_to_XYZ_integration(data_sd)
            return XYZ_to_xy(w_XYZ), data_sd

        def filter_to_xy():
            filter_path_ext = filter_path
            filter_df = pd.read_excel(filter_path_ext)
            wavelength = filter_df.iloc[1:,0]
            # blu = filter_df.iloc[1:,1]
            cf_w = filter_df.iloc[1:,2]           
            cf_r = filter_df.iloc[1:,3]
            cf_g = filter_df.iloc[1:,4]
            cf_b = filter_df.iloc[1:,5]
            # Cell Filters SDs
            # blu_sd = SpectralDistribution(pd.Series(data = blu.to_numpy(), index = wavelength.to_numpy()))
            cf_w_sd = SpectralDistribution(pd.Series(data = cf_w.to_numpy(), index = wavelength.to_numpy()))
            cf_r_sd = SpectralDistribution(pd.Series(data = cf_r.to_numpy(), index = wavelength.to_numpy()))
            cf_b_sd = SpectralDistribution(pd.Series(data = cf_b.to_numpy(), index = wavelength.to_numpy()))
            cf_g_sd = SpectralDistribution(pd.Series(data = cf_g.to_numpy(), index = wavelength.to_numpy()))
            # plt.plot(self.w_sd_BLU.normalise().wavelengths,self.w_sd_BLU.normalise().values)
            # plt.show()
            # print(self.w_sd_BLU.shape)
            # print(cf_r_sd.shape)
            # BLU spectrum values (NDarray) multiplied by cell filters
            blu_cf_w = self.w_sd_BLU.align(cf_w_sd.shape).normalise().values * cf_w_sd.normalise().values
            blu_cf_r = self.w_sd_BLU.align(cf_r_sd.shape).normalise().values * cf_r_sd.normalise().values
            blu_cf_g = self.w_sd_BLU.align(cf_g_sd.shape).normalise().values * cf_g_sd.normalise().values
            blu_cf_b = self.w_sd_BLU.align(cf_b_sd.shape).normalise().values * cf_b_sd.normalise().values
            # Cell Filtered SDs
            blu_cf_w_sd = SpectralDistribution(pd.Series(data= blu_cf_w, index = cf_w_sd.wavelengths))
            blu_cf_r_sd = SpectralDistribution(pd.Series(data= blu_cf_r, index = cf_r_sd.wavelengths))
            blu_cf_g_sd = SpectralDistribution(pd.Series(data= blu_cf_g, index = cf_g_sd.wavelengths))
            blu_cf_b_sd = SpectralDistribution(pd.Series(data= blu_cf_b, index = cf_b_sd.wavelengths))
            # SDs to xy
            w_xy = XYZ_to_xy(sd_to_XYZ_integration(blu_cf_w_sd))
            r_xy = XYZ_to_xy(sd_to_XYZ_integration(blu_cf_r_sd))
            g_xy = XYZ_to_xy(sd_to_XYZ_integration(blu_cf_g_sd))
            b_xy = XYZ_to_xy(sd_to_XYZ_integration(blu_cf_b_sd))

            

            # plt.plot(blu_cf_r_sd.wavelengths, blu_cf_r_sd.values)
            # plt.plot(blu_cf_g_sd.wavelengths, blu_cf_g_sd.values)
            # plt.plot(blu_cf_b_sd.wavelengths, blu_cf_b_sd.values)
            # plt.show()

            return w_xy, r_xy, g_xy, b_xy

            

        # file_path = os.path.join(os.path.dirname(__file__), 'samples', 'sample1.*')
        # file_path_ext = [*glob.glob(file_path)] # Unpacking with * works with any object that is iterable. Listeye dönüştürme.
        # # for file_path_ext in glob.glob(file_path) :
        file_path_ext = file_path
        with open(file_path_ext, "r") as file :
            file_list = file.readlines()
        self.w_xy, self.w_sd_BLU = data_to_xy()
        if not filter_bool or filter_path == "":
            self.b_xy, b_sd_BLU = data_to_xy(max = 490)
            self.g_xy, g_sd_BLU = data_to_xy(min=490, max=578)
            self.r_xy, r_sd_BLU = data_to_xy(min=578)
        if filter_bool and filter_path != "":
            self.w_xy, self.r_xy, self.g_xy, self.b_xy = filter_to_xy()
            
        
        # *** GAUSSIAN SD
        # sd_g_gauss = sd_gaussian_fwhm(525.8, 23.6)
        # g_gauss_XYZ = sd_to_XYZ_integration(sd_g_gauss)
        # self.g_xy = XYZ_to_xy(g_gauss_XYZ)
        # *** GAUSSIAN SD

        PRIMARIES = np.array(
            [
                self.r_xy,   #R
                self.g_xy,   #G
                self.b_xy,   #B
            ]
        )
        """*SAMPLE* colourspace primaries."""

        # WHITEPOINT_NAME: str = "SAMPLE_data"
        # """*SAMPLE* colourspace whitepoint name."""

        CCS_WHITEPOINT = self.w_xy
        """*SAMPLE* colourspace whitepoint chromaticity coordinates."""

        MATRIX_SAMPLE_TO_XYZ = normalised_primary_matrix(
            PRIMARIES, CCS_WHITEPOINT
        )
        """*SAMPLE* colourspace to *CIE XYZ* tristimulus values matrix."""

        MATRIX_XYZ_TO_SAMPLE = np.linalg.inv(MATRIX_SAMPLE_TO_XYZ)
        """*CIE XYZ* tristimulus values to *SAMPLE* colourspace matrix."""

        # Değerlerle RGB_Colourspace sınıfı yeni bir obje oluşturma -------#
        self.RGB_COLOURSPACE_SAMPLE = RGB_Colourspace(
            name = WHITEPOINT_NAME,
            primaries = PRIMARIES,
            whitepoint = CCS_WHITEPOINT,
            whitepoint_name = WHITEPOINT_NAME
        )
        #------------------------------------------------------------------#


    # DOSYADAN OKUYUP KOORDİNAT HESAPLAYAN METHOD ###############

    # DIŞARIDAN ELLE GİRİLEN DEĞERLERİ ALAN METHOD ################################################
    def user_RGB_primaries(
        self,
        PRIMARIES,
        CCS_WHITEPOINT,# = np.array([0,0]),
        WHITEPOINT_NAME
        ):

        # PRIMARIES_SAMPLE = np.array(
        #     [
        #         [0.6717, 0.3147],   #R
        #         [0.2912, 0.6625],   #G
        #         [0.1573, 0.0560],   #B
        #     ]
        # )
        # """*SAMPLE* colourspace primaries."""

        # WHITEPOINT_NAME_SAMPLE: str = "SAMPLE_user"
        # """*SAMPLE* colourspace whitepoint name."""

        # CCS_WHITEPOINT_SAMPLE = np.array([0.3102, 0.3056])
        # """*SAMPLE* colourspace whitepoint chromaticity coordinates."""

        MATRIX_SAMPLE_TO_XYZ = normalised_primary_matrix(
            PRIMARIES, CCS_WHITEPOINT
        )
        """*SAMPLE* colourspace to *CIE XYZ* tristimulus values matrix."""

        MATRIX_XYZ_TO_SAMPLE = np.linalg.inv(MATRIX_SAMPLE_TO_XYZ)
        """*CIE XYZ* tristimulus values to *SAMPLE* colourspace matrix."""

        # Değerlerle RGB_Colourspace sınıfı yeni bir obje oluşturma -------#
        self.RGB_COLOURSPACE_SAMPLE = RGB_Colourspace(
            name = WHITEPOINT_NAME,
            primaries = PRIMARIES,
            whitepoint = CCS_WHITEPOINT,
            whitepoint_name = WHITEPOINT_NAME
        )
        #------------------------------------------------------------------#
    # DIŞARIDAN ELLE GİRİLEN DEĞERLERİ ALAN METHOD #################################################


# a=RGB_primaries()
# a.file_RGB_primaries("C:/Users/emre/Documents/Python_Projeleri/colour-science/Gamut_Calculator/samples/sample1.IRR", "at", "C:/Users/emre/Documents/Python_Projeleri/colour-science/Gamut_Calculator/LCD_filter/T1004-P3 32inch FHD CELL CF.XLSX", True)
