#coding:gbk
import wx

class Frame(wx.Frame):
    """
    创建一个wx.Frame的子类
    """
    def __init__(self,image,parent=None,id=-1,pos=wx.DefaultPosition,title="Hello,wxPython!"):
        """
        __init__中哪些参数是必须的,每次这么多参数,谁能记得住.
        不过,参数没有顺序要求.想想,创建一个frame需要哪些东西,无非就是位置,大小,标题,ID之类的内容.
        """

        #转换为bmp,估计是方便处理
        temp = image.ConvertToBitmap()

        #获取图片大小,同时作为Frame的大小
        size = temp.GetWidth(),temp.GetHeight()
        wx.Frame.__init__(self,parent,id,title,pos,size)

        #可以看到StaticBitmap(parent=self),此处self指向Frame,所以图像显示在Frame上.
        #如果在Frame中创建一个panel,是否要修改parent呢,可以试一下.
        #注意两句的差别,在于parent参数不一样.运行后,可以看到如果在frame上画图,会被panel盖住.
        #如果在panel上画图,则不会有问题. 或是不创建panel,在frame上画图,也不会有问题.至些,可以理解self的部分含义了.
        panel = wx.Panel(self,-1)
        wx.StaticBitmap(parent=self,bitmap=temp)
        wx.StaticBitmap(parent=panel,bitmap=temp)


class App(wx.App):

    def OnInit(self):
        image = wx.Image("113.png",wx.BITMAP_TYPE_PNG)
        self.frame = Frame(image)

        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App()
    app.MainLoop()

if __name__ == "__main__":
    main()