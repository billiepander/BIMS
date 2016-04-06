#coding:gbk
import wx
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\Fonts\simsun.ttc",size=11)
class panel_ItemSituation(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.input = wx.TextCtrl(self,-1,pos=(580,40))
        self.btn = wx.Button(self,-1,label="查询",pos=(690,37))
        self.input.SetValue(u'输入桥名')
        self.btn.Bind(wx.EVT_BUTTON, self.SearchItem)

    def SearchItem(self,event):
        windowSize = self.GetSizeTuple()
        try:
            self.sb.Destroy()           #去除上次的图片显示以免重叠
        except:
            pass
        self.bridgeName = self.input.GetValue()
        self.image = wx.Image(".\\templates\\%s.png"%abs(hash(self.bridgeName)))
        self.sb = wx.StaticBitmap(self,-1,wx.BitmapFromImage(self.image))
        partSize = self.sb.GetSizeTuple()
        pos = ((windowSize[0]-partSize[0])/2,(windowSize[1]-partSize[1])/2)
        self.sb.SetPosition(pos)
