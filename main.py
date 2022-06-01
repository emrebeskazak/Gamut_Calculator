# import numpy as np
# import colour
import matplotlib.pyplot as plt
from colour.plotting import ( 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931, 
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1976UCS,
)

import sample

# sample.user_RGB_primaries()   # Fonksiyon için
sample_RGB = sample.RGB_primaries()

wp_bool = False
plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(['ITU-R BT.2020', sample_RGB.RGB_COLOURSPACE_SAMPLE_data, sample_RGB.RGB_COLOURSPACE_SAMPLE_user], show_whitepoints = wp_bool, standalone = False)
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
