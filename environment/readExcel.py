'''
Author: your name
Date: 2020-11-05 10:13:25
LastEditTime: 2020-11-05 11:24:07
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \environment\readExcel.py
'''
#-- encoding: utf-8 --
import openpyxl
import xlrd

fileName = 'FS参数.xlsx'
file = xlrd.open_workbook(filename = fileName)
sheet = file.sheet_by_index(0)
name_list = []
type_list = []
Down_list = []
Up_list = []
Init_list = []
for i in range(1, 187):
    name_list.append(sheet.cell_value(i, 0))
    type_list.append(sheet.cell_value(i, 1))
    Down_list.append(sheet.cell_value(i, 7))
    Up_list.append(sheet.cell_value(i, 8))
    Init_list.append(sheet.cell_value(i, 3))
### print all params
# for i in range(len(name_list)):
#     print("%s,%s,%s,%s" %(name_list[i], type_list[i], Down_list[i], Up_list[i]))

### write name to file
# f1 = open('name.txt', 'w', encoding = 'utf-8')
# for i in range(len(name_list)):
#     f1.write('\'')
#     f1.write(name_list[i])
#     f1.write('\',')
#     f1.write('\n')
# f1.close()

### write metrics details to file
f2 = open('details.txt', 'w', encoding = 'utf-8')
for i in range(len(name_list)):
    f2.write('\'')
    f2.write(name_list[i])
    f2.write('\': [\'')
    f2.write(type_list[i])
    f2.write('\', [')
    f2.write(str(Down_list[i]))
    f2.write(', ')
    f2.write(str(Up_list[i]))
    f2.write(', ')
    f2.write(str(Init_list[i]))
    f2.write(']],')
    f2.write('\n')
f2.close()