#coding:gbk
import wx
class panel_search(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.label_1 = wx.StaticText( self, -1, '������',pos = (550,250))
        self.input_1 = wx.TextCtrl(self, -1,pos = (650,250))
        self.label_2 = wx.StaticText( self, -1, '�������',pos = (550,300))
        mylist_1 = ['�ճ����','���ڼ��','������']
        self.choice_1 = wx.Choice(self, -1, choices = mylist_1,pos = (650,300),size=(100,50))
        self.label_3 = wx.StaticText(self,-1,"���ʱ��", pos=(550,350))
        self.input_3 = wx.TextCtrl(self, -1, pos = (650,350))
        self.label_4 = wx.StaticText(self,-1,"ʱ�����Ϊ�գ�Ҳ���������꣬���뵽�£����뵽�죬��2016-04-01", pos=(650,400))
        self.bt = wx.Button( self , -1,label = "����" ,pos = (800,450))