# Colour spaces yani 
#
# BT. 2020, 
# NTSC, 
# sRGB 
#
# gibi renk uzayları:
#
# <class 'colour.models.rgb.rgb_colourspace.RGB_Colourspace'>
#
# sınıfının objeleri olarak tanımlanmışlardır. Bu renk uzaylarının "primary"leri yani 3 renklerinin koordinat bilgileri 
# "colour/models/rgb/datasets" klasöründe bulunan .py dosyalarındadır. Aynı zamanda obje tanımlamaları da bu dosyaların
# sonunda, dosyalardaki veriler kullanılarak yapılmıştır.
#
# Mesela sRGB renk uzayı "RGB_COLOURSPACE_sRGB" adıyla obje olarak tanımlanmıştır.
# Bunları kullanabilmek için:
# import colour
from colour.models import RGB_COLOURSPACE_sRGB, RGB_COLOURSPACE_BT2020, RGB_COLOURSPACE_NTSC1953

# Bu objelerin elemanlarına ulaşarak kullanmak lazım. Örneğin renk uzaylarının koordinatlarına ulaşmak için (<class 'numpy.ndarray'>):

print(RGB_COLOURSPACE_NTSC1953.primaries)

# colour.models.rgb.rgb_colourspace.RGB_Colourspace
# Attributes:
# ~colour.RGB_Colourspace.name
# ~colour.RGB_Colourspace.primaries
# ~colour.RGB_Colourspace.whitepoint
# ~colour.RGB_Colourspace.whitepoint_name
# ~colour.RGB_Colourspace.matrix_RGB_to_XYZ
# ~colour.RGB_Colourspace.matrix_XYZ_to_RGB
# ~colour.RGB_Colourspace.cctf_encoding
# ~colour.RGB_Colourspace.cctf_decoding
# ~colour.RGB_Colourspace.use_derived_matrix_RGB_to_XYZ
# ~colour.RGB_Colourspace.use_derived_matrix_XYZ_to_RGB


