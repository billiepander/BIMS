#coding:gbk
import wx
import MySqlUnit
import wx.grid as gridlib

class panel_MoneyTable(wx.Panel):
    def __init__(self, parent,result):
        self.result = result
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(len(result)):
            self.griddetail = gridlib.Grid(self)
            self.griddetail.CreateGrid(1,3)
            self.griddetail.SetDefaultCellOverflow(False)
            # self.griddetail.SetRowAttr("colAtr")
            self.griddetail.SetColSize(2,300)
            self.griddetail.SetRowSize(0,50)
            self.griddetail.SetRowLabelValue(0,str(i+1))
            self.griddetail.SetColLabelValue(0,"����".decode("gbk"))
            self.griddetail.SetColLabelValue(1,"�걨��".decode("gbk"))
            self.griddetail.SetColLabelValue(2,"�걨����".decode("gbk"))
            self.griddetail.SetCellValue(0,0,result[i][0])
            self.griddetail.SetCellValue(0,1,result[i][7])
            self.griddetail.SetCellValue(0,2,result[i][8])
            mylist = ['��׼','����']
            self.choice = wx.Choice(self, -1, choices = mylist,pos = (650,300),size=(100,50),name = "��%d���걨��Ϣ"%i)
            self.choice.Bind(wx.EVT_CHOICE, lambda evt,mark=i,choice=self.choice:self.changewhichone(evt,mark,choice))
            # print self.choice.Name        #�ɻ��ÿ���������nameֵ
            sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer1.Add(self.griddetail, 0, wx.EXPAND)
            sizer1.Add(self.choice, 0, wx.EXPAND)
            sizer.Add(sizer1,0,wx.CENTER)

        self.SetSizer(sizer)


    def changewhichone(self,event,mark,choice):
        self.ratifyresult = choice.GetStringSelection()

        #�û��ı���׼������ͬ�������ݿ�
        sql = "UPDATE bridgeinfo SET DeclareProgress = '%s' WHERE FileRoute = '%s'" % (self.ratifyresult,self.result[mark][10])
        MySqlUnit.exe_update(sql)