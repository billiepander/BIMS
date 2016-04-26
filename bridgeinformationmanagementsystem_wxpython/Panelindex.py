import wx
import wx.html2


class Panel_gis(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent=parent)
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.browser = wx.html2.WebView.New(self)
    self.browser.LoadURL(r"templates\index.jpg")
    sizer.Add(self.browser, 1, wx.EXPAND, 10)
    self.SetSizer(sizer)


app = wx.App()
frame = wx.Frame(None,-1)
pane = Panel_gis(frame)
frame.Show()
app.MainLoop()