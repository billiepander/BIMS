#coding:gbk
import wx
import wx.grid as gridlib

class panel_writein(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.label_1 = wx.StaticText( self, -1, '������',pos = (550,50))
        self.input_1 = wx.TextCtrl(self, -1,pos = (650,50))
        self.label_2 = wx.StaticText( self, -1, '�������',pos = (550,100))
        mylist_1 = ['�ճ����','���ڼ��','������']
        self.choice_1 = wx.Choice(self, -1, choices = mylist_1,pos = (650,100),size=(100,50))
        self.choice_1.SetSelection(0)
        self.label_3 = wx.StaticText(self,-1,"���ʱ��", pos=(550,150))
        self.input_3 = wx.TextCtrl(self, -1, pos = (650,150))
        self.label_3_5 = wx.StaticText(self,-1,"��������", pos=(550,200))
        self.input_3_5 = wx.TextCtrl(self, -1, pos = (650,200))
        self.label_3_rate = wx.StaticText(self,-1,"��Ŀ����", pos=(550,250))
        self.input_3_rate = wx.TextCtrl(self, -1, pos = (650,250))
        self.label_3_mainbroken = wx.StaticText(self,-1,"��Ҫ����", pos=(550,300))
        # self.input_3_mainbroken = wx.TextCtrl(self, -1, pos = (650,300))
        self.input_3_mainbroken = wx.TextCtrl(self,-1,pos = (650,300),size = (250,80), style=wx.TE_MULTILINE )
        self.label_4 = wx.StaticText(self,-1,"�Ƿ��걨ά�޷ѣ�",pos=(550,400))
        mylist_2 = ['��','��']
        self.choice_2 = wx.Choice(self, -1, choices = mylist_2,pos = (650,400),size=(100,50))
        self.choice_2.SetSelection(0)
        self.label_6 = wx.StaticText(self,-1,"�걨���ã�",pos=(550,450))
        self.input_6 = wx.TextCtrl(self,-1,pos = (650,450))
        self.label_5 = wx.StaticText(self,-1,"�걨������",pos=(550,500))
        self.input_5 = wx.TextCtrl(self,-1,pos = (650,500),size = (250,150), style=wx.TE_MULTILINE )
        self.bt_7 = wx.Button( self , -1,label = "������ϸҳ" ,pos = (920,620))

class panel_detail(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.griddetail = gridlib.Grid(self)
        self.griddetail.CreateGrid(150,50)
        mylist = [u'̼��',u'�ص�',u'������',u'�ֽ���',u'�ֽ���ʴ',u'�ְ���',u'��Ĥ���']
        self.choice = wx.Choice(self, -1, choices = mylist)
        self.choice.SetSelection(0)
        self.choice.SetBackgroundColour('black')
        self.choice.SetForegroundColour('white')
        self.subbtn = wx.Button(self,-1,label = "�ύ����")
        self.subbtn.SetBackgroundColour("black")
        self.subbtn.SetForegroundColour("white")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.choice, 0, wx.EXPAND)
        sizer.Add(self.subbtn, 0, wx.EXPAND)
        sizer.Add(self.griddetail, 0, wx.EXPAND)

        self.SetSizer(sizer)
