#coding:gbk
import wx

class Frame(wx.Frame):
    """
    ����һ��wx.Frame������
    """
    def __init__(self,image,parent=None,id=-1,pos=wx.DefaultPosition,title="Hello,wxPython!"):
        """
        __init__����Щ�����Ǳ����,ÿ����ô�����,˭�ܼǵ�ס.
        ����,����û��˳��Ҫ��.����,����һ��frame��Ҫ��Щ����,�޷Ǿ���λ��,��С,����,ID֮�������.
        """

        #ת��Ϊbmp,�����Ƿ��㴦��
        temp = image.ConvertToBitmap()

        #��ȡͼƬ��С,ͬʱ��ΪFrame�Ĵ�С
        size = temp.GetWidth(),temp.GetHeight()
        wx.Frame.__init__(self,parent,id,title,pos,size)

        #���Կ���StaticBitmap(parent=self),�˴�selfָ��Frame,����ͼ����ʾ��Frame��.
        #�����Frame�д���һ��panel,�Ƿ�Ҫ�޸�parent��,������һ��.
        #ע������Ĳ��,����parent������һ��.���к�,���Կ��������frame�ϻ�ͼ,�ᱻpanel��ס.
        #�����panel�ϻ�ͼ,�򲻻�������. ���ǲ�����panel,��frame�ϻ�ͼ,Ҳ����������.��Щ,�������self�Ĳ��ֺ�����.
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