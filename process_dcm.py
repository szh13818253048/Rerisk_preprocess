import SimpleITK as sitk
import os
filename = 'D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\BAOCHUNE_002097680\\PLAIN'
def load_itkfilewithtrucation(filename, upper=200, lower=-200):  # 600,-1000
    """
    load mhd\dicom files,set truncted value range and normalization 0-255
    :param filename:
    :param upper:
    :param lower:
    :return:
    """
    # 1,tructed outside of liver value
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(filename)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    srcitkimagearray = sitk.GetArrayFromImage(image)  # z, y, x
    print(srcitkimagearray.shape)
 
    srcitkimagearray[srcitkimagearray > upper] = upper
    srcitkimagearray[srcitkimagearray < lower] = lower
    # 2,get tructed outside of liver value image
    sitktructedimage = sitk.GetImageFromArray(srcitkimagearray)

reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(filename)
reader.SetFileNames(dicom_names)
# print(dicom_names)
image = reader.Execute()
srcitkimagearray = sitk.GetArrayFromImage(image)  # z, y, x
print(srcitkimagearray.shape)

# srcitkimagearray[srcitkimagearray > upper] = upper
# srcitkimagearray[srcitkimagearray < lower] = lower
# # 2,get tructed outside of liver value image
# sitktructedimage = sitk.GetImageFromArray(srcitkimagearray)