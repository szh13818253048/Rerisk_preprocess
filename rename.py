import os
from unicodedata import digit
dataset_path = 'D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data'
patients = os.listdir(dataset_path)
changed = []
for i in patients:
    before = i
    while i[0].isalpha():
        i = i[1:]
        # print(i)
    if i[0] == '_':
        i = i[1:]
    if i[0] == ' ':
        i = i[1:]
    # print(i)
    if i[-4:] != "xlsx":
        changed.append(i)
        print(before + " " + i)
        # try:
        #     os.rename(dataset_path + '\\' + before,dataset_path  + '\\' + i)
        # except:
        #     pass

print('num_numlist:'+str(len(changed)))
print('num_numlist:'+str(len(list(dict.fromkeys(changed)))))

# print(changed[-1])

# import SimpleITK as sitk
# import os
# # read label
# import xlrd
# wb = xlrd.open_workbook('D:\\Medical Image Dateset\\Sun kun\\Recurrence risk evaluation data\\GENE LIST.xlsx')
# #按工作簿定位工作表
# sh = wb.sheet_by_name('Sheet1')
# keys = [k.strip() for k in sh.col_values(0)[1:]]
# label_dict = dict(zip(keys,sh.col_values(4)[1:]))

# # print(label_dict)

# for i in range(len(label_dict)):
#     print(changed[i] + "  " + str(int(label_dict[changed[i]])))
