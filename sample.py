import numpy as np
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
import os
import glob

# file_path = os.path.join(os.path.dirname(__file__), 'samples', 'sample1.*')

# for file_path_ext in glob.glob(file_path) :
#     with open(file_path_ext, "r") as file :
#         pass


class RGB_primaries:
    # def __init__(self):
    #     self.user_RGB_primaries()
    #     # self.file_RGB_primaries()
    
    # DOSYADAN OKUYUP KOORDİNAT HESAPLAYAN METHOD ###############
    def file_RGB_primaries(self):
        def data_to_xy(min = 360, max = 780):
            line_number = 0
            data_dict = {}
            while True:
                if file_list[line_number][1].isnumeric():
                    if int(file_list[line_number][0:4]) >= min:
                        line_tuple = file_list[line_number].strip().partition(" ")
                        # print(line_tuple)
                        # break
                        data_dict[float(line_tuple[0].strip())] = float(line_tuple[2].strip()) 
                    if int(file_list[line_number][0:4]) >= max:
                        break
                line_number += 1
                if line_number >= len(file_list):
                    print ("Dosya çözülemedi!")
                    break
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
            # print(data_sd)
            w_XYZ = sd_to_XYZ_integration(data_sd)
            return XYZ_to_xy(w_XYZ)

        file_path = os.path.join(os.path.dirname(__file__), 'samples', 'sample1.*')
        file_path_ext = [*glob.glob(file_path)] # Unpacking with * works with any object that is iterable. Listeye dönüştürme.
        # for file_path_ext in glob.glob(file_path) :
        with open(file_path_ext[0], "r") as file :
            file_list = file.readlines()
        self.w_xy = data_to_xy()
        # print(self.w_xy)
        self.b_xy = data_to_xy(max = 490)
        self.g_xy = data_to_xy(min=490, max=578)
        # print(self.g_xy)
        self.r_xy = data_to_xy(min=578)
        
        # *** GAUSSIAN SD
        # sd_g_gauss = sd_gaussian_fwhm(525.8, 23.6)
        # g_gauss_XYZ = sd_to_XYZ_integration(sd_g_gauss)
        # self.g_xy = XYZ_to_xy(g_gauss_XYZ)
        # *** GAUSSIAN SD

        PRIMARIES_SAMPLE = np.array(
            [
                self.r_xy,   #R
                self.g_xy,   #G
                self.b_xy,   #B
            ]
        )
        """*SAMPLE* colourspace primaries."""

        WHITEPOINT_NAME_SAMPLE: str = "SAMPLE_data"
        """*SAMPLE* colourspace whitepoint name."""

        CCS_WHITEPOINT_SAMPLE = self.w_xy
        """*SAMPLE* colourspace whitepoint chromaticity coordinates."""

        MATRIX_SAMPLE_TO_XYZ = normalised_primary_matrix(
            PRIMARIES_SAMPLE, CCS_WHITEPOINT_SAMPLE
        )
        """*SAMPLE* colourspace to *CIE XYZ* tristimulus values matrix."""

        MATRIX_XYZ_TO_SAMPLE = np.linalg.inv(MATRIX_SAMPLE_TO_XYZ)
        """*CIE XYZ* tristimulus values to *SAMPLE* colourspace matrix."""

        # Değerlerle RGB_Colourspace sınıfı yeni bir obje oluşturma -------#
        self.RGB_COLOURSPACE_SAMPLE = RGB_Colourspace(
            "Sample_data",
            PRIMARIES_SAMPLE,
            CCS_WHITEPOINT_SAMPLE,
            WHITEPOINT_NAME_SAMPLE
        )
        #------------------------------------------------------------------#


    # DOSYADAN OKUYUP KOORDİNAT HESAPLAYAN METHOD ###############

    # DIŞARIDAN ELLE GİRİLEN DEĞERLERİ ALAN METHOD ################################################
    def user_RGB_primaries(
        self,
        PRIMARIES_SAMPLE,
        CCS_WHITEPOINT_SAMPLE,# = np.array([0,0]),
        WHITEPOINT_NAME_SAMPLE = "Sample"
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
            PRIMARIES_SAMPLE, CCS_WHITEPOINT_SAMPLE
        )
        """*SAMPLE* colourspace to *CIE XYZ* tristimulus values matrix."""

        MATRIX_XYZ_TO_SAMPLE = np.linalg.inv(MATRIX_SAMPLE_TO_XYZ)
        """*CIE XYZ* tristimulus values to *SAMPLE* colourspace matrix."""

        # Değerlerle RGB_Colourspace sınıfı yeni bir obje oluşturma -------#
        self.RGB_COLOURSPACE_SAMPLE = RGB_Colourspace(
            name = WHITEPOINT_NAME_SAMPLE,
            primaries = PRIMARIES_SAMPLE,
            whitepoint = CCS_WHITEPOINT_SAMPLE,
            whitepoint_name = WHITEPOINT_NAME_SAMPLE
        )
        #------------------------------------------------------------------#
    # DIŞARIDAN ELLE GİRİLEN DEĞERLERİ ALAN METHOD #################################################


# def user_RGB_primaries():
# # DIŞARIDAN ELLE GİRİLEN DEĞERLERİ ALAN FONKSİYON ################################################
# #
#     PRIMARIES_SAMPLE = np.array(
#         [
#             [0.6717, 0.3147],   #R
#             [0.2912, 0.6625],   #G
#             [0.1573, 0.0560],   #B
#         ]
#     )
#     """*SAMPLE* colourspace primaries."""

#     WHITEPOINT_NAME_SAMPLE: str = "SAMPLE"
#     """*SAMPLE* colourspace whitepoint name."""

#     CCS_WHITEPOINT_SAMPLE = np.array([0.3102, 0.3056])
#     """*SAMPLE* colourspace whitepoint chromaticity coordinates."""

#     MATRIX_SAMPLE_TO_XYZ = normalised_primary_matrix(
#         PRIMARIES_SAMPLE, CCS_WHITEPOINT_SAMPLE
#     )
#     """*SAMPLE* colourspace to *CIE XYZ* tristimulus values matrix."""

#     MATRIX_XYZ_TO_SAMPLE = np.linalg.inv(MATRIX_SAMPLE_TO_XYZ)
#     """*CIE XYZ* tristimulus values to *SAMPLE* colourspace matrix."""

#     # Değerlerle RGB_Colourspace sınıfı yeni bir obje oluşturma -------#
#     #                                 ********
#     global RGB_COLOURSPACE_SAMPLE   # *GLOBAL* OLARAK TANIMLAMAK ZORUNDA KALDIM. #***************
#     #                                 ********
#     RGB_COLOURSPACE_SAMPLE = RGB_Colourspace(
#         "Sample",
#         PRIMARIES_SAMPLE,
#         CCS_WHITEPOINT_SAMPLE,
#         WHITEPOINT_NAME_SAMPLE
#     )
# #
# #------------------------------------------------------------------#
# #
# # DIŞARIDAN ELLE GİRİLEN DEĞERLERİ ALAN FONKSİYON #################################################



# # DENEME DEĞERLERİ ################################################
# #
# PRIMARIES_SAMPLE = np.array(
#     [
#         [0.6717, 0.3147],   #R
#         [0.2912, 0.6625],   #G
#         [0.1573, 0.0560],   #B
#     ]
# )
# """*SAMPLE* colourspace primaries."""

# WHITEPOINT_NAME_SAMPLE: str = "SAMPLE"
# """*SAMPLE* colourspace whitepoint name."""

# CCS_WHITEPOINT_SAMPLE = np.array([0.3102, 0.3056])
# """*SAMPLE* colourspace whitepoint chromaticity coordinates."""

# MATRIX_SAMPLE_TO_XYZ = normalised_primary_matrix(
#     PRIMARIES_SAMPLE, CCS_WHITEPOINT_SAMPLE
# )
# """*SAMPLE* colourspace to *CIE XYZ* tristimulus values matrix."""

# MATRIX_XYZ_TO_SAMPLE = np.linalg.inv(MATRIX_SAMPLE_TO_XYZ)
# """*CIE XYZ* tristimulus values to *SAMPLE* colourspace matrix."""

# # Değerlerle RGB_Colourspace sınıfı yeni bir obje oluşturma -------#
# #
# RGB_COLOURSPACE_SAMPLE = RGB_Colourspace(
#     "Sample",
#     PRIMARIES_SAMPLE,
#     CCS_WHITEPOINT_SAMPLE,
#     WHITEPOINT_NAME_SAMPLE
# )
# #
# #------------------------------------------------------------------#
# #
# # DENEME DEĞERLERİ #################################################
