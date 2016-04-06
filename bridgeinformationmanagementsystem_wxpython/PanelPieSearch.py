#coding:gbk
import wx
import MySqlUnit
class panel_WebSituation(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        searchWebName = "select FatherWeb from bridgeinfo GROUP by FatherWeb"
        WebNames = MySqlUnit.exe_search(searchWebName)
        mylist=[]
        for i in WebNames:
            for j in i:
                mylist.append(j)
        self.choice = wx.Choice(self, -1, choices = mylist,size=(100,30),pos = (680,90))
        self.choice.Bind(wx.EVT_CHOICE,self.ChooseWeb)

    def ChooseWeb(self,event):
        self.WebName = self.choice.GetStringSelection()
        self.image = wx.Image(".\\templates\\%s.png"%abs(hash(self.WebName)))
        self.sb = wx.StaticBitmap(self,-1,wx.BitmapFromImage(self.image),pos=(500,120))