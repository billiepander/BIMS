#coding:gbk
import wx

class Panel_IndexPic(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        image = wx.Image("113.png",wx.BITMAP_TYPE_PNG)
        temp = image.ConvertToBitmap()
        #获取图片大小,同时作为Frame的大小
        size = temp.GetWidth(),temp.GetHeight()

        wx.StaticBitmap(parent=self,bitmap=temp)
        # wx.StaticBitmap(parent=self,bitmap=temp)



