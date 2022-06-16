import numpy as np
from colour.models.rgb import (
    RGB_Colourspace,
    RGB_COLOURSPACE_ADOBE_RGB1998,
    RGB_COLOURSPACE_ADOBE_WIDE_GAMUT_RGB,
    RGB_COLOURSPACE_APPLE_RGB,
    RGB_COLOURSPACE_NTSC1953, 
    RGB_COLOURSPACE_NTSC1987,
    RGB_COLOURSPACE_CIE_RGB,
    RGB_COLOURSPACE_BT2020,
    RGB_COLOURSPACE_sRGB,
)
from colour.models import xy_to_Luv_uv
# print(RGB_COLOURSPACE_NTSC1953.primaries)

Areas_Colourspaces ={
    "ITU-R BT.2020"    : 0.2118665,
    "NTSC (1953)"      : 0.1582,
    "sRGB"             : 0.11205,
    'adobe1998'        : 0.15115,
    "Apple RGB"        : 0.1065
}

Areas_Colourspaces_uv ={
    "ITU-R BT.2020"    : 0.11182263089,
    "NTSC (1953)"      : 0.0744257331755,
    "sRGB"             : 0.0648918180133,
    'adobe1998'        : 0.0757067297097,
    "Apple RGB"        : 0.0583397540708
}

def sample_area(colourspace, xy_bool):
    if xy_bool:
        R = colourspace.primaries[0]
        G = colourspace.primaries[1]
        B = colourspace.primaries[2]
    else:
        R = xy_to_Luv_uv(colourspace.primaries[0])
        G = xy_to_Luv_uv(colourspace.primaries[1])
        B = xy_to_Luv_uv(colourspace.primaries[2])       
    R_x1 = R[0]
    R_y1 = R[1]
    G_x2 = G[0]
    G_y2 = G[1]
    B_x3 = B[0]
    B_y3 = B[1]

    Area = (abs( (R_x1*G_y2 + G_x2*B_y3 + B_x3*R_y1) - (G_x2*R_y1 + B_x3*G_y2 + R_x1*B_y3) ))/2
    return Area

def sample_points(colourspace, xy_bool):
    # Reference:
    # https://umitsen.wordpress.com/2013/04/07/nokta-ucgenin-icinde-mi-degil-mi-test-etme/
    if xy_bool:
        R = colourspace.primaries[0]
        G = colourspace.primaries[1]
        B = colourspace.primaries[2]
    else:
        R = xy_to_Luv_uv(colourspace.primaries[0])
        G = xy_to_Luv_uv(colourspace.primaries[1])
        B = xy_to_Luv_uv(colourspace.primaries[2])       
    R_x1 = R[0]
    R_y1 = R[1]
    G_x2 = G[0]
    G_y2 = G[1]
    B_x3 = B[0]
    B_y3 = B[1]

    quanta = 90
    ii = np.linspace(0, 0.9, quanta)
    jj = np.linspace(0, 0.9, quanta)

    p = np.zeros((1,2))
    # print(p)

    for ix in ii:
        for jy in jj:
            p = np.append(p, [[ix,jy]], axis=0)
    p = np.delete(p, 0,0)
    # print(p)

    bx = G_x2 - R_x1
    by = G_y2 - R_y1
    cx = B_x3 - R_x1
    cy = B_y3 - R_y1
    d = bx*cy - cx*by

    def points_inside(Pxy):
        x = (Pxy[0] - R_x1)
        y = (Pxy[1] - R_y1)
        wa = (x*(by-cy) + y*(cx-bx) + bx*cy - cx*by) / d
        wb = (x*cy - y*cx) / d
        wc = (y*bx - x*by) / d
        if ((wa<1 and wa > 0) and (wb<1 and wb > 0) and (wc<1 and wc > 0)):
            return Pxy
        # return None

    points = map(points_inside, p)
    points_array = np.zeros((1,2))
    for point in points:
        if type(point) == np.ndarray:
            points_array = np.append(points_array, [[point[0],point[1]]], axis=0)
    p = np.delete(p, 0,0)

    return points_array

# ******** Areas_Colourspaces dict'te kaydetmek için bir seferlik alan hesaplamada kullanılmış kod.
# ******** colour kütüphanesinden yeni renk uzayı eklenip hesaplatılabilir.
# colourspace = RGB_COLOURSPACE_APPLE_RGB
# # print(sample_area_uv(colourspace))
# # print(sample_area(colourspace))
# ******** Areas_Colourspaces dict'te kaydetmek için bir seferlik alan hesaplamada kullanılmış kod

# # ******* Standart Renk uzaylarının içindeki noktaları tespit etmek için tek seferlik kullanılan kod
# # ******* Data "points_database.py" içine kaydedildi.
# colourspace = RGB_COLOURSPACE_APPLE_RGB
# R = xy_to_Luv_uv(colourspace.primaries[0])
# G = xy_to_Luv_uv(colourspace.primaries[1])
# B = xy_to_Luv_uv(colourspace.primaries[2])
# R_x1 = R[0]
# R_y1 = R[1]
# G_x2 = G[0]
# G_y2 = G[1]
# B_x3 = B[0]
# B_y3 = B[1]

# quanta = 90
# ii = np.linspace(0, 0.9, quanta)
# jj = np.linspace(0, 0.9, quanta)

# p = np.zeros((1,2))
# # print(p)

# for ix in ii:
#     for jy in jj:
#         p = np.append(p, [[ix,jy]], axis=0)
# p = np.delete(p, 0,0)
# # print(p)

# bx = G_x2 - R_x1
# by = G_y2 - R_y1
# cx = B_x3 - R_x1
# cy = B_y3 - R_y1
# d = bx*cy - cx*by

# def points_inside(Pxy):
#     x = (Pxy[0] - R_x1)
#     y = (Pxy[1] - R_y1)
#     wa = (x*(by-cy) + y*(cx-bx) + bx*cy - cx*by) / d
#     wb = (x*cy - y*cx) / d
#     wc = (y*bx - x*by) / d
#     if ((wa<1 and wa > 0) and (wb<1 and wb > 0) and (wc<1 and wc > 0)):
#         return Pxy
#     # return None

# points = map(points_inside, p)
# with open("temp_points.txt", "w") as f:
#     # f.write("import numpy as np\n\n")
#     f.write("AppleRGB_points_uv = np.array(\n\t[\n")
#     for point in points:
#         if type(point) == np.ndarray:
#             f.write(f"\t\t[{point[0]}, {point[1]}],\n")
#     f.write("\t]\n)")
# # ******* Standart Renk uzaylarının içindeki noktaları tespit etmek için tek seferlik kullanılan kod