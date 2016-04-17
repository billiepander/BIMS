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

# if __name__ == '__main__':
#   app = wx.App()
#   dialog = MyBrowser()
#   dialog.browser.LoadURL("http://www.gpsspg.com/maps.htm")
#   dialog.Show()
#   app.MainLoop()




# class MyBrowser(wx.Dialog):
#   def __init__(self, *args, **kwds):
#     wx.Dialog.__init__(self, *args, **kwds)
#     sizer = wx.BoxSizer(wx.VERTICAL)
#     self.browser = wx.html2.WebView.New(self)
#     sizer.Add(self.browser, 1, wx.EXPAND, 10)
#     self.SetSizer(sizer)
#     self.SetSize((1400,800))
#
# if __name__ == '__main__':
#   app = wx.App()
#   dialog = MyBrowser(None, -1)
#   dialog.browser.LoadURL("http://www.gpsspg.com/maps.htm")
#   dialog.Show()
#   app.MainLoop()
