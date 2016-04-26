#coding:utf-8
import win32com
from win32com.client import constants

# w = win32com.client.Dispatch('Word.Application')
# 或者使用下面的方法，使用启动独立的进程：
w = win32com.client.DispatchEx('Word.Application')
# 后台运行，不显示，不警告
w.Visible = 0
w.DisplayAlerts = 0
# 打开新的文件
# doc = w.Documents.Open( FileName = u"C:\\Users\\Administrator\\Desktop\\pd2.docx" )
doc = w.Documents.Add() # 创建新的文档
# 插入文字
myRange = doc.Range(0,0)
myRange.InsertBefore('take or add??\njello\nkitty')

doc.SaveAs( r"C:\Users\Administrator\Desktop\pd3.docx" )
# 打印，注：此打印能够跳出选择保存为的格式，并且默认为PDF
doc.PrintOut()

doc.Close()
w.Quit()
