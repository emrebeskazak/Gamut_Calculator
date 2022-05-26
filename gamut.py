
rec2020_R_x1 = 0.708
rec2020_R_y1 = 0.292
rec2020_G_x2 = 0.170
rec2020_G_y2 = 0.797
rec2020_B_x3 = 0.131
rec2020_B_y3 = 0.046

e06_R_x1 = 0.6713
e06_R_y1 = 0.3186
e06_G_x2 = 0.2872
e06_G_y2 = 0.6717
e06_B_x3 = 0.1579
e06_B_y3 = 0.0494

A_r2020 = (abs( (rec2020_R_x1*rec2020_G_y2 + rec2020_G_x2*rec2020_B_y3 + rec2020_B_x3*rec2020_R_y1) - 
(rec2020_G_x2*rec2020_R_y1 + rec2020_B_x3*rec2020_G_y2 + rec2020_R_x1*rec2020_B_y3) ))/2

A_e06 = (abs( (e06_R_x1*e06_G_y2 + e06_G_x2*e06_B_y3 + e06_B_x3*e06_R_y1) - 
(e06_G_x2*e06_R_y1 + e06_B_x3*e06_G_y2 + e06_R_x1*e06_B_y3) ))/2

print(f"Gamut ratio of E06 to the Rec. 2020 is %{A_e06/A_r2020*100}")