#coding:utf-8
import wx, xlwt, xlrd
import win32com
from win32com.client import constants


w = win32com.client.DispatchEx('Word.Application')
# 后台运行，不显示，不警告
w.Visible = 0
w.DisplayAlerts = 0
# 打开新的文件
# doc = w.Documents.Open( FileName = u"C:\\Users\\Administrator\\Desktop\\pd2.docx" )
doc = w.Documents.Add() # 创建新的文档

workbook = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\%s\%s'%(u'牛逼桥日常检查',u'牛逼桥2016-04-04日常检查.xls'))
os.listdir(r'C:\Users\Administrator\Desktop\%s'%u'牛逼桥日常检查')
# workbook = xlrd.open_workbook(r'templates\test1.xls')
    #抓取所有sheet页的名称
worksheets = workbook.sheet_names()
# print('worksheets is %s' %worksheets)
    #定位到sheet1
worksheet1 = workbook.sheet_by_name(u'sheet1')
    #遍历sheet1中所有行row
num_rows = worksheet1.nrows
content = ''
for curr_row in range(num_rows):
    row = worksheet1.row_values(curr_row)
    print('row%d is %s' %(curr_row,row))
    for i in range(len(row)):
        content += row[i]
        if i==0 and u':' not in row[i] and len(row[i]) != 0:
            content += ':'
        content += '\t'
    content += '\n'


myRange = doc.Range(0,0)

myRange.InsertBefore(content)

doc.SaveAs(r"C:\Users\Administrator\Desktop\%s.docx"%u'牛逼桥日常检查')
# 打印，注：此打印能够跳出选择保存为的格式，并且默认为PDF
doc.PrintOut()

doc.Close()
w.Quit()