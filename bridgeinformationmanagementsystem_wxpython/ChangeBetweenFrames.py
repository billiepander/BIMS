#coding:gbk
import wx, xlwt, xlrd, os, shutil, MySQLdb, chardet, time, threading
import wx.grid as gridlib
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
font = FontProperties(fname=r"c:\windows\Fonts\simsun.ttc",size=11)
#数据库装饰器
def conclos(**kwargs):
    def ifunc(func):
        def infunc(sql):
            conn = MySQLdb.Connect(
                host=kwargs['host'],
                port = kwargs['port'],
                user = kwargs['user'],
                passwd = kwargs['passwd'],
                db = kwargs['db'],
                charset = kwargs['charset'],
            )
            cursor = conn.cursor()
            result = func(cursor,sql)
            conn.commit()
            cursor.close()
            conn.close()
            return result
        return infunc
    return ifunc

@conclos(host='127.0.0.1',port = 3306,user = 'root',passwd = 'punkisdead',db = 'bims',charset = 'utf8',)
def exe(cursor,sql):
    cursor.execute(sql)
    outcatch = cursor.fetchall()
    return outcatch


class panel_login(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.gs = wx.GridSizer(4,2,5,5)
        self.label_1 = wx.StaticText( self, -1, 'login as:')
        mylist = ['省级','市级','检测部门','访客']
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
        if self.ID == u"访客":
            self.login.input_2.SetValue("visitor")
            self.login.input_3.SetValue("123")

    def OnButton(self,event):
        self.name = str(self.login.input_2.GetValue())
        self.passwd = str(self.login.input_3.GetValue())
        if self.name == "bumen" and self.passwd == "123" and self.ID == u"检测部门":
            depart = frame_depart()
            self.Hide()
            depart.Show()
            depart.Maximize()
        else:
            self.dialogue = wx.Dialog(self,-1,"提示框",size = (200,150))
            self.errorlabel = wx.StaticText(self.dialogue,-1,"\n\n您输入的用户名或密码有误\n请输入正确的用户名与密码\n如果没有请选用访客模式",style = wx.ALIGN_CENTER)
            self.dialogue.ShowModal()

class panel_writein(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.label_1 = wx.StaticText( self, -1, '桥名：',pos = (550,50))
        self.input_1 = wx.TextCtrl(self, -1,pos = (650,50))
        self.label_2 = wx.StaticText( self, -1, '检测类型',pos = (550,100))
        mylist_1 = ['日常检查','定期检测','特殊检测']
        self.choice_1 = wx.Choice(self, -1, choices = mylist_1,pos = (650,100),size=(100,50))
        self.label_3 = wx.StaticText(self,-1,"检测时间", pos=(550,150))
        self.input_3 = wx.TextCtrl(self, -1, pos = (650,150))
        self.label_3_5 = wx.StaticText(self,-1,"所属网络", pos=(550,200))
        self.input_3_5 = wx.TextCtrl(self, -1, pos = (650,200))
        self.label_3_rate = wx.StaticText(self,-1,"项目评级", pos=(550,250))
        self.input_3_rate = wx.TextCtrl(self, -1, pos = (650,250))
        self.label_3_mainbroken = wx.StaticText(self,-1,"主要问题", pos=(550,300))
        # self.input_3_mainbroken = wx.TextCtrl(self, -1, pos = (650,300))
        self.input_3_mainbroken = wx.TextCtrl(self,-1,pos = (650,300),size = (250,80), style=wx.TE_MULTILINE )
        self.label_4 = wx.StaticText(self,-1,"是否申报维修费：",pos=(550,400))
        mylist_2 = ['是','否']
        self.choice_2 = wx.Choice(self, -1, choices = mylist_2,pos = (650,400),size=(100,50))
        self.label_6 = wx.StaticText(self,-1,"申报费用：",pos=(550,450))
        self.input_6 = wx.TextCtrl(self,-1,pos = (650,450))
        self.label_5 = wx.StaticText(self,-1,"申报陈述：",pos=(550,500))
        self.input_5 = wx.TextCtrl(self,-1,pos = (650,500),size = (250,150), style=wx.TE_MULTILINE )
        self.bt_7 = wx.Button( self , -1,label = "进入详细页" ,pos = (920,620))

class panel_detail(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.griddetail = gridlib.Grid(self)
        self.griddetail.CreateGrid(100,50)
        self.subbtn = wx.Button(self,-1,label = "提交保存")
        self.subbtn.SetBackgroundColour("black")
        self.subbtn.SetForegroundColour("white")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.subbtn, 0, wx.EXPAND)
        sizer.Add(self.griddetail, 0, wx.EXPAND)

        self.SetSizer(sizer)

class panel_search(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.label_1 = wx.StaticText( self, -1, '桥名：',pos = (550,250))
        self.input_1 = wx.TextCtrl(self, -1,pos = (650,250))
        self.label_2 = wx.StaticText( self, -1, '检测类型',pos = (550,300))
        mylist_1 = ['日常检查','定期检测','特殊检测']
        self.choice_1 = wx.Choice(self, -1, choices = mylist_1,pos = (650,300),size=(100,50))
        self.label_3 = wx.StaticText(self,-1,"检测时间", pos=(550,350))
        self.input_3 = wx.TextCtrl(self, -1, pos = (650,350))
        self.label_4 = wx.StaticText(self,-1,"时间可以为空，也可以输入年，输入到月，输入到天，如2016-04-01", pos=(650,400))
        self.bt = wx.Button( self , -1,label = "搜索" ,pos = (800,450))

class panel_searchResultShow(wx.Panel):
    def __init__(self,parent,amount=0):
        wx.Panel.__init__(self,parent=parent)
        self.griddetail = gridlib.Grid(self)
        self.griddetail.CreateGrid(20,5,)
        self.griddetail.SetColSize(1,300)
        self.griddetail.SetColSize(0,100)
        # self.griddetail.SetRowSize(0,50)
        self.subbtn = wx.Button(self,-1,label = "查看详细信息")
        self.subbtn.SetBackgroundColour("black")
        self.subbtn.SetForegroundColour("white")
        # self.info = wx.StaticText(self,-1,"共有%d条数据，现在是第%d条")
        self.numinfo = wx.StaticText(self,-1,"一共有%d条相关数据"%amount)
        self.advicenum = wx.StaticText(self,-1,"在下面输入要跳转到的条数")
        # self.numinfo2 = wx.StaticText(self,-1,"跳转到")
        self.which2see = wx.TextCtrl(self, -1, value="1")
        # self.numinfo3 = wx.StaticText(self,-1,"条")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.subbtn, 0, wx.CENTER)
        sizer.Add(self.griddetail, 0,wx.CENTER)
        sizer.Add(self.numinfo, 0, wx.CENTER)
        sizer.Add(self.advicenum, 0, wx.CENTER)
        sizer.Add(self.which2see, 0, wx.CENTER)
        self.SetSizer(sizer)



class panel_MoneyTable(wx.Panel):
    def __init__(self, parent,result):
        self.result = result
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(len(result)):
            self.griddetail = gridlib.Grid(self)
            self.griddetail.CreateGrid(1,3)
            self.griddetail.SetDefaultCellOverflow(False)
            # self.griddetail.SetRowAttr("colAtr")
            self.griddetail.SetColSize(2,300)
            self.griddetail.SetRowSize(0,50)
            self.griddetail.SetRowLabelValue(0,str(i+1))
            self.griddetail.SetColLabelValue(0,"桥名".decode("gbk"))
            self.griddetail.SetColLabelValue(1,"申报费".decode("gbk"))
            self.griddetail.SetColLabelValue(2,"申报陈述".decode("gbk"))
            self.griddetail.SetCellValue(0,0,result[i][0])
            self.griddetail.SetCellValue(0,1,result[i][7])
            self.griddetail.SetCellValue(0,2,result[i][8])
            mylist = ['批准','驳回']
            self.choice = wx.Choice(self, -1, choices = mylist,pos = (650,300),size=(100,50),name = "第%d条申报信息"%i)
            self.choice.Bind(wx.EVT_CHOICE, lambda evt,mark=i,choice=self.choice:self.changewhichone(evt,mark,choice))
            # print self.choice.Name        #可获得每个下拉框的name值
            sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer1.Add(self.griddetail, 0, wx.EXPAND)
            sizer1.Add(self.choice, 0, wx.EXPAND)
            sizer.Add(sizer1,0,wx.CENTER)

        self.SetSizer(sizer)


    def changewhichone(self,event,mark,choice):
        print mark
        print self.result[mark][10]
        self.ratifyresult = choice.GetStringSelection()

        #用户改变批准条件后同步到数据库
        db = MySQLdb.connect("localhost","root","punkisdead","BIMS", charset = "utf8")
        cursor = db.cursor()
        sql = "UPDATE bridgeinfo SET DeclareProgress = '%s' WHERE FileRoute = '%s'" % (self.ratifyresult,self.result[mark][10])
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
        db.close()

class panel_RatifyWebMoney(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        search = "select sum(bi.DeclareAmount) as 'ratified', bi.FatherWeb, wb.Ratified from bridgeinfo as bi JOIN WebBudget AS wb ON bi.FatherWeb=wb.WebName WHERE bi.DeclareProgress = '%s' GROUP BY bi.FatherWeb"%u"批准"
        # search = "select sum(DeclareAmount) as 'ratified', FatherWeb from bridgeinfo WHERE DeclareProgress = '%s' GROUP BY FatherWeb"%u"批准"
        self.result = exe(search)
        self.Budget = {u"二环":10000,u'中国':3000}
        sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(len(self.result)):
            self.griddetail = gridlib.Grid(self)
            self.griddetail.CreateGrid(1,3)
            self.griddetail.SetColSize(2,200)
            self.griddetail.SetColSize(0,100)
            self.griddetail.SetColSize(1,150)
            self.griddetail.SetRowSize(0,25)
            # self.griddetail.SetRowAttr("colAtr")
            self.griddetail.SetRowLabelValue(0,str(i+1))
            self.griddetail.SetColLabelValue(0,"网络名".decode("gbk"))
            self.griddetail.SetColLabelValue(1,"已用预算".decode("gbk"))
            self.griddetail.SetColLabelValue(2,"总预算".decode("gbk"))
            self.griddetail.SetCellValue(0,0,self.result[i][1])
            self.griddetail.SetCellValue(0,1,str(self.result[i][0]))
            print self.result[i][1]
            print type(self.result[i][1])
            self.griddetail.SetCellValue(0,2,self.result[i][2])
            self.btn = wx.Button(self,-1,label="提交预算更改",name="第%d个按钮"%i)
            self.input = wx.TextCtrl(self,-1,name="第%d个网络"%i)
            self.input.SetValue(u'在此输入总预算')
            self.btn.Bind(wx.EVT_BUTTON, lambda evt,mark=i,buuttnn=self.btn:self.changeWhichWeb(evt,mark,buuttnn))
            sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer1.Add(self.griddetail, 0, wx.EXPAND)
            sizer1.Add(self.input, 0, wx.EXPAND)
            sizer1.Add(self.btn, 0, wx.EXPAND)
            sizer.Add(sizer1,0,wx.CENTER)

        self.SetSizer(sizer)


    def changeWhichWeb(self,event,mark,buuttnn):
        print mark
        self.whichInput2Show = wx.FindWindowByName('第%d个网络'%mark)
        self.getCahngeValue = self.whichInput2Show.GetValue()

        #用户改变批准条件后同步到数据库
        db = MySQLdb.connect("localhost","root","punkisdead","BIMS", charset = "utf8")
        cursor = db.cursor()
        sql = "UPDATE WebBudget SET Ratified = '%s' WHERE WebName = '%s'" % (self.getCahngeValue,self.result[mark][1])
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
        db.close()

class panel_WebSituation(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        searchWebName = "select FatherWeb from bridgeinfo GROUP by FatherWeb"
        WebNames = exe(searchWebName)
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

class panel_ItemSituation(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.input = wx.TextCtrl(self,-1,pos=(580,40))
        self.btn = wx.Button(self,-1,label="查询",pos=(690,37))
        self.input.SetValue(u'输入桥名')
        self.btn.Bind(wx.EVT_BUTTON, self.SearchItem)
        # sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        # sizer1.Add(self.input, 0, wx.Center)
        # sizer1.Add(self.btn, 0, wx.Center)
        # self.SetSizer(sizer1)

    def SearchItem(self,event):
        self.bridgeName = self.input.GetValue()
        t=threading.Thread(target=self.Ready)
        # t=threading.Thread(target=self.Ready,args=self.bridgeName)
        t.start()
    def Ready(self):
        self.search = "select BridgeName,QualityLevel,DetectTime from bridgeinfo WHERE BridgeName='%s' ORDER BY DetectTime"%u"西直门大桥"
        self.result = exe(self.search)

        changeBridge={u'A':4,u"B":3,u'C':2,u'D':1}
        x = []
        y = []
        for i in range(len(self.result)):
            y.append(changeBridge[self.result[i][1]])
            x.append(i+1)

        print x,y
        plt.plot(x,y,"k-",label="range",color="red")
        plt.title(self.result[0][0],size=16,fontproperties=font)
        plt.axis([0,len(x)+1,0,6])
        plt.xticks( np.arange(len(x)), ['0']+[z[2] for z in self.result ] )
        plt.yticks( np.arange(5), ('0','D', 'C', 'B', 'A') )
        # plt.show()
        plt.savefig("templates//littletry.png")
        plt.close()


class frame_depart(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None, title = "桥梁信息管理系统")
        t = threading.Thread(target=self.yubeidui)
        t.start()
        self.CreateStatusBar()  # A Statusbar in the bottom of the window

        #桥梁信息输入那里有两个界面，有两个函数，导致变量不能共享，故在此初始化。待解决，应该用一个函数，这样占内存小一点
        self.routestring,self.mainbroken,self.askmoney,self.reason4askmoney,self.bridgename,self.detecttime,self.detecttype,self.parentWeb,self.bridgerate = ["","","","","","","","",""]

        self.search_bridgename,self.search_detecttype,self.search_detectime,self.result = ["","","",""]

        # 顶部的菜单项
        filemenu= wx.Menu()
        upermenu = wx.Menu()
        helpmenu = wx.Menu()

        # 向菜单项添加about与exit两项，中间以横线分割
        self.bumem_importfiel = filemenu.Append(wx.ID_ADD,"导入excel文件","在录入下的具体信息录入时用于导入excel文件")
        self.bumem_importfiel.Enable(False)
        self.bumem_importimage = filemenu.Append(wx.ID_FILE,"导入图片","在录入下的具体信息录入时用于导入图像文件")
        self.bumem_importimage.Enable(False)
        self.bumen_writein = filemenu.Append(wx.ID_ABOUT, "录入"," 正在录入 ")
        self.bumem_search = filemenu.Append(wx.ID_HELP_SEARCH, "项目检索"," 查询项目级桥梁信息 ")
        # filemenu.AppendSeparator()
        # self.bumen_exit = filemenu.Append(wx.ID_EXIT,"E&xit"," 退出程序 ")
        self.uper_SearchItemHis = upermenu.Append(wx.ID_EDIT, "单项桥梁历史纪录", "查看单项桥梁随各时间的质量变化")
        self.uper_givemoney = upermenu.Append(wx.ID_HELP, "单项预算表查看与批示", "单项预算表查看与批示")
        self.uper_ratifyWebMoney = upermenu.Append(wx.ID_APPLY,"网级预算查看与批示","网级预算查看与批示")
        self.uper_webinfosearch = upermenu.Append(wx.ID_HARDDISK,"网级项目检索","网级桥梁信息查询")
        # self.uper_webinfosearch.Enable(False)         #使此菜单项无效
        self.doctment = helpmenu.Append(wx.ID_ANY,"帮助文档","查看产品说明书")

        # 创建菜单栏并且将前面的菜单项捆绑进去
        menuBar = wx.MenuBar()               #创建菜单栏
        menuBar.Append(filemenu,"操作")      #将菜单项"filemenu"放入菜单栏并且取名为。。。
        menuBar.Append(upermenu,"高级")
        menuBar.Append(helpmenu,"帮助")
        self.SetMenuBar(menuBar)             #将菜单栏放入Frame

        self.panelwritein = panel_writein(self)
        self.panelwritein.Hide()
        self.paneldetail = panel_detail(self)
        self.paneldetail.Hide()
        self.panelsearch = panel_search(self)
        self.panelsearch.Hide()
        # self.panelshowsearchresult = panel_searchResultShow(self)
        # self.panelshowsearchresult.Hide()


        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(self.panelbumen, 1, wx.EXPAND)
        self.sizer.Add(self.panelwritein, 1, wx.EXPAND)
        self.sizer.Add(self.paneldetail, 1 , wx.EXPAND)
        self.sizer.Add(self.panelsearch, 1 , wx.EXPAND)
        # self.sizer.Add(self.panelshowsearchresult, 1 , wx.EXPAND)
        self.SetSizer(self.sizer)

        #绑定菜单事件
        self.Bind(wx.EVT_MENU,self.writein, self.bumen_writein)
        self.Bind(wx.EVT_MENU,self.search, self.bumem_search)
        self.Bind(wx.EVT_MENU,self.searchitemhis, self.uper_SearchItemHis)
        self.Bind(wx.EVT_MENU,self.ratifyitemmoney, self.uper_givemoney)
        self.Bind(wx.EVT_MENU,self.ratifyWebMoney, self.uper_ratifyWebMoney)
        self.Bind(wx.EVT_MENU,self.pieSearch, self.uper_webinfosearch)

        # self.Bind(wx.EVT_MENU,self.search, self.bumem_search)
        #输入页下拉框以及按钮的事件绑定
        self.panelwritein.choice_2.Bind( wx.EVT_CHOICE,self.choice4money )
        self.panelwritein.bt_7.Bind( wx.EVT_BUTTON,self.detailinfo )
        self.paneldetail.subbtn.Bind(wx.EVT_BUTTON,self.submitdetail)
        #项目搜索页的事件绑定
        self.panelsearch.bt.Bind(wx.EVT_BUTTON,self.submitsearch)

    def yubeidui(self):
        searchWebName = "select FatherWeb from bridgeinfo GROUP by FatherWeb"
        WebNames = exe(searchWebName)
        for i in WebNames:
            for j in i:
                search = "select COUNT(QualityLevel), QualityLevel,FatherWeb from bridgeinfo WHERE FatherWeb='%s' GROUP BY QualityLevel"%j
                result = exe(search)
                self.sumnumber = 0
                self.sumnumber = reduce(lambda x,y:x+y,[z[0] for z in result])
                # make a square figure and axes
                plt.figure(1, figsize=(4.7,4.7))
                ax = plt.axes([0.1, 0.1, 0.8, 0.8])

                # labels = ['A', 'B', 'C', 'D']
                # fracs = [result[0][0], result[1][0], result[2][0], result[3][0]]
                # explode=(0, 0, 0, 0.05)       #每块间的间隔，对应到labels，既是Hogs块的间距会是0.05
                self.labels = []
                self.fracs = []
                self.explode=[]
                for z in range(len(result)):
                    self.labels.append(chr(65+z))
                    self.fracs.append(result[z][0])
                    if z==3:
                        self.explode.append(0.05)
                    else:
                        self.explode.append(0)

                plt.pie(self.fracs, explode=self.explode, labels=self.labels, autopct='%1.1f%%', shadow=True, startangle=90,colors=['yellowgreen', 'gold', 'lightskyblue', 'red'])

                plt.title(result[0][2]+u'桥梁状况\n',fontsize=16, color="red",fontproperties=font)
                plt.xlabel(u'共有%d座桥梁'%self.sumnumber,fontproperties=font)
                plt.savefig(".\\templates\\%d.png"%abs(hash(j)))
                plt.close()

    def hideAllPanel(self):
        try:
            self.panelshowsearchresult.Hide()
        except:
            pass
        try:
            self.panelMoneyTable.Hide()
        except:
            pass
        try:
            self.paneldetail.Hide()
        except:
            pass
        try:
            self.panelRatifiWebMoney.Hide()
        except:
            pass
        try:
            self.panelwritein.Hide()
        except:
            pass
        try:
            self.panelsearch.Hide()
        except:
            pass
        try:
            self.panelShowWebPie.Hide()
        except:
            pass
        try:
            self.panelItemSearch.Hide()
        except:
            pass



    def writein(self , event):
        self.hideAllPanel()
        self.panelwritein.Show()
        self.Layout()

    def choice4money(self,event):
        self.whethermoney = self.panelwritein.choice_2.GetStringSelection()
        if self.whethermoney == u"否":        #出错提醒(故加u):Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
            self.panelwritein.input_5.SetValue("")
            self.panelwritein.input_6.SetValue("")
            self.panelwritein.input_5.Enable( False )
            self.panelwritein.input_6.Enable( False )

        elif self.whethermoney == u"是":      #若没有这个则点击了否后再点击是两个输入框任然无效
            self.panelwritein.input_5.Enable( True )
            self.panelwritein.input_6.Enable( True )
            # self.askmoney = self.panelwritein.input_6.GetValue()
            # self.reason4askmoney = self.panelwritein.input_5.GetValue()
            print self.askmoney,self.reason4askmoney

    def detailinfo( self,event ):
        self.bridgename = self.panelwritein.input_1.GetValue()
        self.detecttype = self.panelwritein.choice_1.GetStringSelection()
        self.detecttime = self.panelwritein.input_3.GetValue()
        self.parentWeb = self.panelwritein.input_3_5.GetValue()
        self.bridgerate = self.panelwritein.input_3_rate.GetValue()
        self.mainbroken = self.panelwritein.input_3_mainbroken.GetValue()
        self.askmoney = self.panelwritein.input_6.GetValue()
        self.reason4askmoney = self.panelwritein.input_5.GetValue()

        print type(self.askmoney),self.reason4askmoney,self.bridgename,type(self.detecttime),self.detecttype,self.parentWeb
        if self.bridgename=="" or self.detecttime=="" or self.detecttype == u"" or self.parentWeb=="":
            self.dialogue_info = wx.Dialog(self,-1,"提示框",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n请全部输入\n不能留空",style = wx.ALIGN_CENTER)
            self.dialogue_info.ShowModal()
        else:
            self.routestring = self.bridgename+self.detecttime+self.detecttype
            print hash(self.routestring)
            os.makedirs(r"templates\%d"%abs(hash(self.routestring)))

            self.panelwritein.Hide()
            self.paneldetail.Show()
            self.Layout()

            self.bumem_importfiel.Enable(True)
            self.Bind(wx.EVT_MENU,self.importfile, self.bumem_importfiel)
            self.bumem_importimage.Enable(True)
            self.Bind(wx.EVT_MENU,self.importimage, self.bumem_importimage)

    def submitdetail(self,event):
        # 应该有两个参数x与y来确定输入了一个x*y的数据块
        # if self.paneldetail.griddetail.GetCellValue(3,3) is None:           #GetValue出来的是unicode
        #     print "none"
        # elif self.paneldetail.griddetail.GetCellValue(3,3) == "":
        #     print "no"
        # else:
        #     print "nono"                                                     #经过实验发现是空，而不是None
        rowflag,columnflag = 0,0
        while self.paneldetail.griddetail.GetCellValue(rowflag,0) != "":
            rowflag+=1
        while self.paneldetail.griddetail.GetCellValue(0,columnflag) != "":
            columnflag+=1
        print rowflag,columnflag            #实际输入区域

        #保存为excel
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
        #向sheet页中写入数据
        sheet1.write(0,0,"桥名".decode("gbk"))
        sheet1.write(0,1,self.bridgename)
        sheet1.write(1,0,"检测类型：".decode("gbk"))
        sheet1.write(1,1,self.detecttype)
        sheet1.write(2,0,"检测时间".decode("gbk"))
        sheet1.write(2,1,self.detecttime)
        sheet1.write(3,0,"项目评级".decode("gbk"))
        sheet1.write(3,1,self.bridgerate)
        sheet1.write(4,0,"主要问题".decode("gbk"))
        sheet1.write(4,1,self.mainbroken)
        sheet1.write(5,0,'是否报预算：'.decode("gbk"))
        sheet1.write(5,1,self.whethermoney)
        sheet1.write(6,0,"申报费用：".decode("gbk"))
        sheet1.write(6,1,self.askmoney)
        sheet1.write(7,0,"申报陈述".decode("gbk"))
        sheet1.write(7,1,self.reason4askmoney)
        for i in range(rowflag):
            for j in range(columnflag):
                sheet1.write(i+10,j,self.paneldetail.griddetail.GetCellValue(i,j))
        # 保存该excel文件,有同名文件时直接覆盖
        workbook.save(r'templates\%s\%s.xls'%(abs(hash(self.routestring)),self.routestring))

        #插入数据库
        db = MySQLdb.connect("localhost","root","punkisdead","bims",charset="utf8" )
        cursor = db.cursor()
        sql = "INSERT INTO bridgeinfo VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s' )" % (self.bridgename, self.detecttype, self.detecttime, self.parentWeb, self.bridgerate,self.mainbroken,self.whethermoney,self.askmoney,self.reason4askmoney,"waiting",str(abs(hash(self.routestring))))
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
        db.close()


    def importfile(self,event):
        #接入打开文件窗口，导入excel文件路径接口
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.absolutefileroute = self.dirname+'\\'+self.filename           #返回打开文件的绝对路径
        dlg.Destroy()

        #下面是导入excel到grid中
            #打开一个workbook
        workbook = xlrd.open_workbook(self.absolutefileroute)
        # workbook = xlrd.open_workbook(r'templates\test1.xls')
            #抓取所有sheet页的名称
        worksheets = workbook.sheet_names()
        # print('worksheets is %s' %worksheets)
            #定位到sheet1
        worksheet1 = workbook.sheet_by_name(u'sheet1')
            #遍历sheet1中所有行row
        num_rows = worksheet1.nrows
        for curr_row in range(num_rows):
            row = worksheet1.row_values(curr_row)
            # print('row%s is %s' %(curr_row,row))
            #遍历sheet1中所有列col
        num_cols = worksheet1.ncols
        for curr_col in range(num_cols):
            col = worksheet1.col_values(curr_col)
            # print('col%s is %s' %(curr_col,col))
            #遍历sheet1中所有单元格cell
        for rown in range(num_rows):
            for coln in range(num_cols):
                cell = worksheet1.cell_value(rown,coln)
                self.paneldetail.griddetail.SetCellValue(rown,coln,cell)

    def importimage(self,event):
        #接入打开文件窗口，导入excel文件路径接口
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.absoluteimageroute = self.dirname+'\\'+self.filename           #返回打开文件的绝对路径
        dlg.Destroy()

        shutil.copyfile(self.absoluteimageroute,r"templates\%s\%s"%(abs(hash(self.routestring)),self.filename))

    def search(self,event):
        # self.dialogue_info = wx.Dialog(self,-1,"提示框",size = (300,150),pos=(600,300))
        # self.dialogue_info.Show()
        self.hideAllPanel()
        self.panelsearch.Show()
        self.Layout()

    def submitsearch(self,event):
        self.search_bridgename = self.panelsearch.input_1.GetValue()
        self.search_detecttype = self.panelsearch.choice_1.GetStringSelection()
        self.search_detectime = self.panelsearch.input_3.GetValue()
        # search = "select * from bridgeinfo "
        if self.search_bridgename == "" or self.search_detecttype == "":
            self.dialogue_info = wx.Dialog(self,-1,"提示框",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n桥名和检测类型\n不能留空",style = wx.ALIGN_CENTER)
            self.dialogue_info.ShowModal()
        if self.search_detectime == "":
            # self.dicthelp = {"日常检查":"normal","定期检测":"regular","特殊检测":"special"}
            search = "select * from bridgeinfo WHERE BridgeName = '%s' AND DetectType = '%s' AND detecttime LIKE '%s%%'" % (self.search_bridgename,self.search_detecttype,self.search_detectime)
        else:
            search = "select * from bridgeinfo WHERE BridgeName = '%s' AND DetectType = '%s'"%(self.search_bridgename,self.detecttype)
        self.result = exe(search)
        if not self.result:
            self.dialogue_info = wx.Dialog(self,-1,"提示框",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n并没有相关数据\n请检查输入",style = wx.ALIGN_CENTER)
            self.dialogue_info.ShowModal()
        else:
            self.panelshowsearchresult = panel_searchResultShow(self,len(self.result))
            self.panelshowsearchresult.Hide()
            self.sizer.Add(self.panelshowsearchresult, 1 , wx.EXPAND)
            self.panelsearch.Hide()
            self.panelshowsearchresult.Show()
            self.Layout()


            self.transferTo = self.panelshowsearchresult.which2see.GetValue()
            self.dbpara = ['桥名','检测类型','检测时间','所属网络','项目评级','主要问题','是否申报维修费','申报费用','申报陈述','申报进度']
            try:
                int(self.transferTo)
                self.rank = int(self.transferTo) - 1
            except:
                self.rank = 0

            self.infoaboutnum = wx.StaticText(self,-1,"这是第%d条数据"%(self.rank+1), pos=(650,550))

            for i in range(10):
                # if i == 2:
                #     self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
                #     self.panelshowsearchresult.griddetail.SetCellValue(i,1,self.result[self.rank][i].strftime('%Y-%m-%d'))
                if not self.result[self.rank][i]:
                    self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
                    self.panelshowsearchresult.griddetail.SetCellValue(i,1,"")
                elif not isinstance(self.result[self.rank][i],unicode):
                    self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
                    self.panelshowsearchresult.griddetail.SetCellValue(i,1,str(self.result[self.rank][i]))
                else:
                    self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
                    self.panelshowsearchresult.griddetail.SetCellValue(i,1,self.result[self.rank][i])


            self.Bind(wx.EVT_TEXT,self.OnEnter,self.panelshowsearchresult.which2see)
            self.Bind(wx.EVT_BUTTON,self.SeeDetailSearchResult,self.panelshowsearchresult.subbtn)

    def OnEnter(self,event):
        self.transferTo = self.panelshowsearchresult.which2see.GetValue()
        self.dbpara = ['桥名','检测类型','检测时间','所属网络','项目评级','主要问题','是否申报维修费','申报费用','申报陈述','申报进度']
        try:
            int(self.transferTo)
            self.rank = int(self.transferTo) - 1
        except:
            self.rank = 0

        self.infoaboutnum = wx.StaticText(self,-1,"这是第%d条数据"%(self.rank+1), pos=(650,550))

        for i in range(10):
            # if i == 2:
            #     self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
            #     self.panelshowsearchresult.griddetail.SetCellValue(i,1,self.result[self.rank][i].strftime('%Y-%m-%d'))
            if not self.result[self.rank][i]:
                self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
                self.panelshowsearchresult.griddetail.SetCellValue(i,1,"")
            elif not isinstance(self.result[self.rank][i],unicode):
                self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
                self.panelshowsearchresult.griddetail.SetCellValue(i,1,str(self.result[self.rank][i]))
            else:
                self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
                self.panelshowsearchresult.griddetail.SetCellValue(i,1,self.result[self.rank][i])

    def SeeDetailSearchResult(self,event):
        self.detailNum = int(self.panelshowsearchresult.which2see.GetValue())
        os.startfile( os.getcwd()+"\\templates\\"+ self.result[self.detailNum-1][10])

    def ratifyitemmoney(self,event):
        #此地有个问题待解决的是如果是从别的界面跳转到这儿，需要先关闭先前页面
        self.hideAllPanel()
        search = "select * from bridgeinfo WHERE WhetherDeclare = '%s' ORDER BY DetectTime"%u"是"
        self.result_money = exe(search)
        self.panelMoneyTable = panel_MoneyTable(self,self.result_money)
        self.sizer.Add(self.panelMoneyTable, 1 , wx.EXPAND)
        self.panelsearch.Hide()
        self.panelwritein.Hide()
        self.panelMoneyTable.Show()
        self.Layout()

    def ratifyWebMoney(self,event):
        self.hideAllPanel()
        self.panelRatifiWebMoney = panel_RatifyWebMoney(self)
        self.sizer.Add(self.panelRatifiWebMoney, 1 , wx.EXPAND)
        self.panelRatifiWebMoney.Show()
        self.Layout()

    def pieSearch(self,event):
        self.panelShowWebPie  = panel_WebSituation(self)
        self.sizer.Add(self.panelShowWebPie, 1 , wx.EXPAND)
        self.hideAllPanel()
        self.panelShowWebPie.Show()
        self.Layout()

    def searchitemhis(self,event):
        self.hideAllPanel()
        self.panelItemSearch = panel_ItemSituation(self)
        self.sizer.Add(self.panelItemSearch, 1 , wx.EXPAND)

        self.panelItemSearch.Show()
        self.Layout()

app = wx.App()
frame1 = frame_login()
frame1.Show()
app.MainLoop()