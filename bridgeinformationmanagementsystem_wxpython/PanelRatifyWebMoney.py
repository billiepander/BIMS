#coding:gbk
import wx
import MySqlUnit
import wx.grid as gridlib

class panel_RatifyWebMoney(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        search = "select sum(bi.DeclareAmount) as 'ratified', bi.FatherWeb, wb.Ratified from bridgeinfo as bi JOIN WebBudget AS wb ON bi.FatherWeb=wb.WebName WHERE bi.DeclareProgress = '%s' GROUP BY bi.FatherWeb"%u"批准"
        # search = "select sum(DeclareAmount) as 'ratified', FatherWeb from bridgeinfo WHERE DeclareProgress = '%s' GROUP BY FatherWeb"%u"批准"
        self.result = MySqlUnit.exe_search(search)[:8]
        self.Budget = {u"二环":10000,u'中国':3000}
        sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(len(self.result)):
            self.griddetail = gridlib.Grid(self)
            self.griddetail.CreateGrid(1,3)
            self.griddetail.SetColSize(2,200)
            self.griddetail.SetColSize(0,100)
            self.griddetail.SetColSize(1,150)
            self.griddetail.SetRowSize(0,25)
            # self.griddetail.SetRowAttr("colAtr")
            self.griddetail.SetRowLabelValue(0,str(i+1))
            self.griddetail.SetColLabelValue(0,"网络名".decode("gbk"))
            self.griddetail.SetColLabelValue(1,"已用预算".decode("gbk"))
            self.griddetail.SetColLabelValue(2,"总预算".decode("gbk"))
            self.griddetail.SetCellValue(0,0,self.result[i][1])
            self.griddetail.SetCellValue(0,1,str(self.result[i][0]))
            print self.result[i][1]
            print type(self.result[i][1])
            self.griddetail.SetCellValue(0,2,self.result[i][2])
            self.btn = wx.Button(self,-1,label="提交预算更改",name="第%d个按钮"%i)
            self.input = wx.TextCtrl(self,-1,name="第%d个网络"%i)
            self.input.SetValue(u'在此输入总预算')
            self.btn.Bind(wx.EVT_BUTTON, lambda evt,mark=i,buuttnn=self.btn:self.changeWhichWeb(evt,mark,buuttnn))
            sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer1.Add(self.griddetail, 0, wx.EXPAND)
            sizer1.Add(self.input, 0, wx.EXPAND)
            sizer1.Add(self.btn, 0, wx.EXPAND)
            sizer.Add(sizer1,0,wx.CENTER)

        self.SetSizer(sizer)


    def changeWhichWeb(self,event,mark,buuttnn):
        print mark
        self.whichInput2Show = wx.FindWindowByName('第%d个网络'%mark)
        self.getCahngeValue = self.whichInput2Show.GetValue()

        #用户改变批准条件后同步到数据库
        sql = "UPDATE WebBudget SET Ratified = '%s' WHERE WebName = '%s'" % (self.getCahngeValue,self.result[mark][1])
        MySqlUnit.exe_update(sql)