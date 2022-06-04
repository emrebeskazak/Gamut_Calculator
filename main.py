import numpy as np
# import colour
import matplotlib.pyplot as plt
from colour.plotting import ( 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931, 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1976UCS,
)

import sample
import area
import points_database

# sample.user_RGB_primaries()   # Fonksiyon için
sample_RGB = sample.RGB_primaries()

# ALAN HESAPLAMA:
# sample_A = area.sample_area(sample_RGB.RGB_COLOURSPACE_SAMPLE_user)
# bt2020_A = area.Areas_Colourspaces["BT.2020"]
# ratio = (sample_A / bt2020_A)*100
# print(f"Örnek Alan: {sample_A} \nbt2020 Alan: {bt2020_A}")
# print(f"Oranı %{ratio}")
# ALAN HESAPLAMA

# COVERAGE HESAPLAMA:
sample_p = area.sample_points(sample_RGB.RGB_COLOURSPACE_SAMPLE_user)
bt2020_p = points_database.BT2020_points
# print(np.shape(bt2020_p))
counter = 0
for p1 in sample_p:
    for p2 in bt2020_p:
        if ((p1[0] == p2 [0]) and (p1[1] == p2 [1])):
            counter+=1
print(f"counter: {counter} \n length: {len(bt2020_p)}")
coverage = (counter / len(bt2020_p))*100
print(f"Coverage: {coverage}")
# COVERAGE HESAPLAMA

wp_bool = False
plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(['ITU-R BT.2020', sample_RGB.RGB_COLOURSPACE_SAMPLE_user], show_whitepoints = wp_bool, standalone = False)
# Show White point
# if wp_bool:
#     plt.plot(sample_RGB.w_xy[0],sample_RGB.w_xy[1],"o")
#Show White point
# plt.plot(sample_RGB.r_xy[0],sample_RGB.r_xy[1],"o")
# plt.plot(sample_RGB.g_xy[0],sample_RGB.g_xy[1],"o")
# plt.plot(sample_RGB.b_xy[0],sample_RGB.b_xy[1],"o")
plt.show()

# plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(['ITU-R BT.2020', sample.RGB_COLOURSPACE_SAMPLE])

# plot_RGB_colourspaces_in_chromaticity_diagram_CIE1976UCS(['ITU-R BT.2020', sample.RGB_COLOURSPACE_SAMPLE])
