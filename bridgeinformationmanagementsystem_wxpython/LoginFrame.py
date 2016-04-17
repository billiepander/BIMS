#coding:gbk
"""
    第一步的登录界面
"""
import wx
from mainFrame import frame_depart
from ShortCutLine import genLinePic

class panel_login(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.gs = wx.GridSizer(4,2,5,5)
        self.label_1 = wx.StaticText( self, -1, 'login as:')
        mylist = ['省级','市级','检测部门']
        self.choice = wx.Choice(self, -1, choices = mylist,)
        self.label_2 = wx.StaticText(self,-1,"name:")
        self.input_2 = wx.TextCtrl(self, -1)
        self.label_3 = wx.StaticText(self,-1,"password:")
        self.input_3 = wx.TextCtrl(self,-1)
        self.label_4 = wx.StaticText(self,-1,"")
        self.submit = wx.Button(self,-1, label = "submmit")
        self.gs.AddMany([(self.label_1,0,wx.ALIGN_RIGHT),(self.choice,0,wx.ALIGN_LEFT),
                         (self.label_2,0,wx.ALIGN_RIGHT),(self.input_2,0,wx.ALIGN_LEFT),
                         (self.label_3,0,wx.ALIGN_RIGHT),(self.input_3,0,wx.ALIGN_LEFT),
                         (self.label_4,0,wx.ALIGN_LEFT),(self.submit,0,wx.ALIGN_LEFT)])
        self.SetSizer(self.gs)

class frame_login(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,size=(300, 250),pos = (520,260),style = wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN, title = "登录")
        self.login = panel_login(self)
        self.login.choice.Bind(wx.EVT_CHOICE, self.OnCheck)
        self.login.submit.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnCheck(self,event):
        self.ID = self.login.choice.GetStringSelection()

    def OnButton(self,event):
        self.name = str(self.login.input_2.GetValue())
        self.passwd = str(self.login.input_3.GetValue())
        if self.name == "bumen" and self.passwd == "123" and self.ID == u"检测部门":
            depart = frame_depart('bumen')
        elif self.name == 'shiji' and self.passwd == '123':
            depart = frame_depart('shiji')
        elif self.name == 'shengji' and self.passwd == '123':
            depart = frame_depart('shengji')
        else:
            self.dialogue = wx.Dialog(self,-1,"提示框",size = (200,150))
            self.errorlabel = wx.StaticText(self.dialogue,-1,"\n\n您输入的用户名或密码有误\n请输入正确的用户名与密码\n如果没有请选用访客模式",style = wx.ALIGN_CENTER)
            self.dialogue.ShowModal()
        self.Hide()
        depart.Show()
        depart.Maximize()

genLinePic()
app = wx.App()
frame1 = frame_login()
frame1.Show()
app.MainLoop()