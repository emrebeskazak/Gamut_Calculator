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
# print(RGB_COLOURSPACE_NTSC1953.primaries)

# ******** Areas_Colourspaces dict'te kaydetmek için bir seferlik alan hesaplamada kullanılmış kod.
# ******** colour kütüphanesinden yeni renk uzayı eklenip hesaplatılabilir.
# colourspace = RGB_COLOURSPACE_ADOBE_RGB1998
# R_x1 = colourspace.primaries[0][0]
# R_y1 = colourspace.primaries[0][1]
# G_x2 = colourspace.primaries[1][0]
# G_y2 = colourspace.primaries[1][1]
# B_x3 = colourspace.primaries[2][0]
# B_y3 = colourspace.primaries[2][1]


# Area = (abs( (R_x1*G_y2 + G_x2*B_y3 + B_x3*R_y1) - 
# (G_x2*R_y1 + B_x3*G_y2 + R_x1*B_y3) ))/2

# print(Area)
# ******** Areas_Colourspaces dict'te kaydetmek için bir seferlik alan hesaplamada kullanılmış kod

Areas_Colourspaces ={
    "ITU-R BT.2020"    : 0.2118665,
    "NTSC (1953)"      : 0.1582,
    "sRGB"             : 0.11205,
    'adobe1998'        : 0.15115,
    "Apple RGB"        : 0.1065
}

# # ******* Standart Renk uzaylarının içindeki noktaları tespit etmek için tek seferlik kullanılan kod
# # ******* Data "points_database.py" içine kaydedildi.
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
#     f.write(f"{colourspace.name}_points = np.array(\n\t[\n")
#     for point in points:
#         if type(point) == np.ndarray:
#             f.write(f"\t\t[{point[0]}, {point[1]}],\n")
#     f.write("\t]\n)")
# # ******* Standart Renk uzaylarının içindeki noktaları tespit etmek için tek seferlik kullanılan kod


def sample_area(colourspace):
    R_x1 = colourspace.primaries[0][0]
    R_y1 = colourspace.primaries[0][1]
    G_x2 = colourspace.primaries[1][0]
    G_y2 = colourspace.primaries[1][1]
    B_x3 = colourspace.primaries[2][0]
    B_y3 = colourspace.primaries[2][1]

    Area = (abs( (R_x1*G_y2 + G_x2*B_y3 + B_x3*R_y1) - (G_x2*R_y1 + B_x3*G_y2 + R_x1*B_y3) ))/2
    return Area

def sample_points(colourspace):
    R_x1 = colourspace.primaries[0][0]
    R_y1 = colourspace.primaries[0][1]
    G_x2 = colourspace.primaries[1][0]
    G_y2 = colourspace.primaries[1][1]
    B_x3 = colourspace.primaries[2][0]
    B_y3 = colourspace.primaries[2][1]

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
