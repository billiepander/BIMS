#coding:gbk
import wx
import wx.grid as gridlib
class panel_searchResultShow(wx.Panel):
    def __init__(self,parent,amount=0):
        wx.Panel.__init__(self,parent=parent)
        self.griddetail = gridlib.Grid(self)
        self.griddetail.CreateGrid(20,5,)
        self.griddetail.SetColSize(1,300)
        self.griddetail.SetColSize(0,100)
        # self.griddetail.SetRowSize(0,50)
        self.subbtn = wx.Button(self,-1,label = "查看详细信息")
        self.subbtn.SetBackgroundColour("black")
        self.subbtn.SetForegroundColour("white")
        # self.info = wx.StaticText(self,-1,"共有%d条数据，现在是第%d条")
        self.numinfo = wx.StaticText(self,-1,"一共有%d条相关数据"%amount)
        self.advicenum = wx.StaticText(self,-1,"在下面输入要跳转到的条数")
        # self.numinfo2 = wx.StaticText(self,-1,"跳转到")
        self.which2see = wx.TextCtrl(self, -1, value="1")
        # self.numinfo3 = wx.StaticText(self,-1,"条")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.subbtn, 0, wx.CENTER)
        sizer.Add(self.griddetail, 0,wx.CENTER)
        sizer.Add(self.numinfo, 0, wx.CENTER)
        sizer.Add(self.advicenum, 0, wx.CENTER)
        sizer.Add(self.which2see, 0, wx.CENTER)
        self.SetSizer(sizer)