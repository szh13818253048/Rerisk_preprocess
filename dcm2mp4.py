# import imp
# import SimpleITK as sitk
# import os
# filename = 'D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\BAOCHUNE_002097680\\PLAIN'
# reader = sitk.ImageSeriesReader()
# dicom_names = reader.GetGDCMSeriesFileNames(filename)
# reader.SetFileNames(dicom_names)
# # print(dicom_names)
# image = reader.Execute()
# srcitkimagearray = sitk.GetArrayFromImage(image)  # z, y, x
# print(srcitkimagearray.shape)


# import matplotlib.pyplot as plt
# import matplotlib.image  as mpimg
# import numpy as np
# import matplotlib.pyplot as mp
# for i in range(0,len(srcitkimagearray)):
#     mp.xticks([])
#     mp.yticks([])
#     plt.imshow(srcitkimagearray[i,:,:],cmap='gray')  #将像素转换为单通道照片，照片一般是3通道的rgb模式
#     plt.savefig('./test_video/{}.jpg'.format(i))
#     # plt.show()


import cv2
import os
import cv2
img_root = './test_video/'#这里写你的文件夹路径，比如：/home/youname/data/img/,注意最后一个文件夹要有斜杠
fps = 1    #保存视频的FPS，可以适当调整
size = (640, 480)
#可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
videoWriter = cv2.VideoWriter('./out.avi',fourcc,fps,size)#最后一个是保存图片的尺寸

for i in range(0,108):
    print(i)
    
    frame = cv2.imread(img_root+str(i)+'.jpg')
    print(frame.shape)
    videoWriter.write(frame)
videoWriter.release()