import win32com
from win32com.client import Dispatch, constants
w = win32com.client.Dispatch('Word.Application')
# ����ʹ������ķ�����ʹ�����������Ľ��̣�
# w = win32com.client.DispatchEx('Word.Application')
# ��̨���У�����ʾ��������
w.Visible = 0
w.DisplayAlerts = 0
# ���µ��ļ�
doc = w.Documents.Open( FileName = filenamein )
# worddoc = w.Documents.Add() # �����µ��ĵ�
# ��������
myRange = doc.Range(0,0)
myRange.InsertBefore('Hello from Python!')
# ʹ����ʽ
wordSel = myRange.Select()
wordSel.Style = constants.wdStyleHeading1
# ���������滻
w.Selection.Find.ClearFormatting()
w.Selection.Find.Replacement.ClearFormatting()
w.Selection.Find.Execute(OldStr,False,False,False,False,False,True,1,True,NewStr,2)
# ҳü�����滻
w.ActiveDocument.Sections[0].Headers[0].Range.Find.ClearFormatting()
w.ActiveDocument.Sections[0].Headers[0].Range.Find.Replacement.ClearFormatting()
w.ActiveDocument.Sections[0].Headers[0].Range.Find.Execute(OldStr,False,False,False,False,False,True,1,False,NewStr,2)
# ������
doc.Tables[0].Rows[0].Cells[0].Range.Text ='123123'
worddoc.Tables[0].Rows.Add() # ����һ��
# ת��Ϊhtml
wc = win32com.client.constants
w.ActiveDocument.WebOptions.RelyOnCSS = 1
w.ActiveDocument.WebOptions.OptimizeForBrowser = 1
w.ActiveDocument.WebOptions.BrowserLevel = 0 # constants.wdBrowserLevelV4
w.ActiveDocument.WebOptions.OrganizeInFolder = 0
w.ActiveDocument.WebOptions.UseLongFileNames = 1
w.ActiveDocument.WebOptions.RelyOnVML = 0
w.ActiveDocument.WebOptions.AllowPNG = 1
w.ActiveDocument.SaveAs( FileName = filenameout, FileFormat = wc.wdFormatHTML )
# ��ӡ��ע���˴�ӡ�ܹ�����ѡ�񱣴�Ϊ�ĸ�ʽ������Ĭ��ΪPDF
doc.PrintOut()
# �ر�
# doc.Close()
w.Documents.Close(wc.wdDoNotSaveChanges)
w.Quit()