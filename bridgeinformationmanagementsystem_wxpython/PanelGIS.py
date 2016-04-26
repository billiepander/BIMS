import wx 
import wx.html2

class Panel_gis(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent=parent)
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.browser = wx.html2.WebView.New(self)
    self.browser.LoadURL("http://map.baidu.com/")
    sizer.Add(self.browser, 1, wx.EXPAND, 10)
    self.SetSizer(sizer)