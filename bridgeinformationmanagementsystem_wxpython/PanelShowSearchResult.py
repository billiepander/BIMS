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
        self.subbtn = wx.Button(self,-1,label = "�鿴��ϸ��Ϣ")
        self.subbtn.SetBackgroundColour("black")
        self.subbtn.SetForegroundColour("white")
        # self.info = wx.StaticText(self,-1,"����%d�����ݣ������ǵ�%d��")
        self.numinfo = wx.StaticText(self,-1,"һ����%d���������"%amount)
        self.advicenum = wx.StaticText(self,-1,"����������Ҫ��ת��������")
        # self.numinfo2 = wx.StaticText(self,-1,"��ת��")
        self.which2see = wx.TextCtrl(self, -1, value="1")
        # self.numinfo3 = wx.StaticText(self,-1,"��")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.subbtn, 0, wx.CENTER)
        sizer.Add(self.griddetail, 0,wx.CENTER)
        sizer.Add(self.numinfo, 0, wx.CENTER)
        sizer.Add(self.advicenum, 0, wx.CENTER)
        sizer.Add(self.which2see, 0, wx.CENTER)
        self.SetSizer(sizer)