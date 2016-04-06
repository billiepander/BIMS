#coding:gbk
import wx
class panel_search(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.label_1 = wx.StaticText( self, -1, '桥名：',pos = (550,250))
        self.input_1 = wx.TextCtrl(self, -1,pos = (650,250))
        self.label_2 = wx.StaticText( self, -1, '检测类型',pos = (550,300))
        mylist_1 = ['日常检查','定期检测','特殊检测']
        self.choice_1 = wx.Choice(self, -1, choices = mylist_1,pos = (650,300),size=(100,50))
        self.label_3 = wx.StaticText(self,-1,"检测时间", pos=(550,350))
        self.input_3 = wx.TextCtrl(self, -1, pos = (650,350))
        self.label_4 = wx.StaticText(self,-1,"时间可以为空，也可以输入年，输入到月，输入到天，如2016-04-01", pos=(650,400))
        self.bt = wx.Button( self , -1,label = "搜索" ,pos = (800,450))