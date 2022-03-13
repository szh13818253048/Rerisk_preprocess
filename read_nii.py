import numpy as np
import nibabel as nib
import os
from PIL import Image

# img = nib.load("D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\CHENXIAOQIN_002086013\\chenxiaoqin.nii.gz")
# (384, 384, 112)
# img = nib.load("D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\CHENJIPING002012410\\002012410.nii.gz")
# (512, 512, 108)
# img = nib.load("D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\DAILONGFEN600205349\\205349.nii.gz")
# (512, 512, 108)
img = nib.load("D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\LIULILI1214124\\1214124.nii.gz")
data = img.get_fdata()
print(data.shape)
# (512, 512, 108)