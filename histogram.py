# -*- coding: utf-8 -*-
import cv2
import os
from matplotlib import pyplot as plt

path_image = str(os.getcwd()) + "/Image/"
path_img_enc = path_image + "/ImageEncrypted"


img = cv2.imread(path_img_enc + "photo_ecc.bmp",0)
plt.hist(img.ravel(),256,[0,256]); plt.show()
