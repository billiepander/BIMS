#coding:utf-8
import xlrd,os
import win32com
from win32com.client import constants


def savedocpdf(oriroute,toroute):
    w = win32com.client.DispatchEx('Word.Application')
    # 后台运行，不显示，不警告
    w.Visible = 0
    w.DisplayAlerts = 0
    # 打开新的文件
    doc = w.Documents.Open( FileName = u"D:\\pycharm code\\wxpythonBluePrint\\moduledoc.docx" )
    # doc = w.Documents.Add() # 创建新的文档

    #找出其下所有的xls文件并将文件名保存到files中
    orifiles = os.listdir(oriroute)
    files = []
    for i in orifiles:
        if u'xls' in i:
            files.append(i)
    print "files:",files

    content = ''
    for i in files:

        workbook = xlrd.open_workbook(oriroute + r'\%s'% i)
        # os.listdir(r'C:\Users\Administrator\Desktop\%s'%u'牛逼桥日常检查')
        # workbook = xlrd.open_workbook(r'templates\test1.xls')
        #抓取所有sheet页的名称
        worksheets = workbook.sheet_names()
        content += worksheets[0]+'\n'
        # print('worksheets is %s' %worksheets)
            #定位到sheet1
        # worksheet1 = workbook.sheet_by_name(u'sheet1')
        worksheet1 = workbook.sheet_by_name(worksheets[0])
            #遍历sheet1中所有行row


        for curr_row in range(10,25):
            # 使用行列索引
            # cell_A1 = table.row(0)[0].value
            # cell_A2 = table.col(1)[0].value
            column = 0
            while True:
                try:
                    content += worksheet1.row(curr_row)[column].value+'  '
                    column += 1
                except:
                    break
            content += '\n'
        content += '\n'

        # print worksheet1.row(12)[11].value
        # print worksheet1.row(12)[1].value
        # for curr_row in range(10,25):
        #     row = worksheet1.row_values(curr_row)
        #     # print('row%d is %s' %(curr_row,row))
        #     for i in range(len(row)):
        #         content += row[i]
        #         # if i==0 and u':' not in row[i] and len(row[i]) != 0:
        #         #     content += ':'
        #         # content += '\t'
        #     content += '\n'

    myRange = doc.Range()
    myRange.InsertAfter(content)

    doc.SaveAs(toroute+r"\%s.docx"%files[0][:-7])
    # 打印，注：此打印能够跳出选择保存为的格式，并且默认为PDF
    doc.PrintOut()

    doc.Close()
    w.Quit()

# savedocpdf(r'D:\pycharm code\wxpythonBluePrint\templates\705173052',r'C:\Users\Administrator\Desktop\%s'%u'牛逼桥日常检查')