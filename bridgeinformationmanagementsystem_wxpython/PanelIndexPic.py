#coding:gbk
import wx

class Panel_IndexPic(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        image = wx.Image("113.png",wx.BITMAP_TYPE_PNG)
        temp = image.ConvertToBitmap()
        #��ȡͼƬ��С,ͬʱ��ΪFrame�Ĵ�С
        size = temp.GetWidth(),temp.GetHeight()

        wx.StaticBitmap(parent=self,bitmap=temp)
        # wx.StaticBitmap(parent=self,bitmap=temp)



