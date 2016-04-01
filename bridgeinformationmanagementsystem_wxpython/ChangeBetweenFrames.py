#coding:gbk
import wx, xlwt, xlrd, os
import wx.grid as gridlib

class panel_login(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.gs = wx.GridSizer(4,2,5,5)
        self.label_1 = wx.StaticText( self, -1, 'login as:')
        mylist = ['sheng','shi','bumen','visitor']
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
        if self.ID == "visitor":
            self.login.input_2.SetValue("visitor")
            self.login.input_3.SetValue("123")

    def OnButton(self,event):
        self.name = str(self.login.input_2.GetValue())
        self.passwd = str(self.login.input_3.GetValue())
        if self.name == "bumen" and self.passwd == "123" and self.ID == "bumen":
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
        self.label_1 = wx.StaticText( self, -1, '桥名：',pos = (550,150))
        self.input_1 = wx.TextCtrl(self, -1,pos = (650,150))
        self.label_2 = wx.StaticText( self, -1, '检测类型',pos = (550,200))
        mylist_1 = ['日常检查','定期检测','特殊检测']
        self.choice_1 = wx.Choice(self, -1, choices = mylist_1,pos = (650,200),size=(100,50))
        self.label_3 = wx.StaticText(self,-1,"检测时间", pos=(550,250))
        self.input_3 = wx.TextCtrl(self, -1, pos = (650,250))
        self.label_3_5 = wx.StaticText(self,-1,"所属网络", pos=(550,300))
        self.input_3_5 = wx.TextCtrl(self, -1, pos = (650,300))
        self.label_4 = wx.StaticText(self,-1,"是否申报维修费：",pos=(550,350))
        mylist_2 = ['是','否']
        self.choice_2 = wx.Choice(self, -1, choices = mylist_2,pos = (650,350),size=(100,50))
        self.label_6 = wx.StaticText(self,-1,"申报费用：",pos=(550,400))
        self.input_6 = wx.TextCtrl(self,-1,pos = (650,400))
        self.label_5 = wx.StaticText(self,-1,"申报陈述：",pos=(550,450))
        self.input_5 = wx.TextCtrl(self,-1,pos = (650,450),size = (300,150), style=wx.TE_MULTILINE )
        self.bt_7 = wx.Button( self , -1,label = "进入详细页" ,pos = (880,620))

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


class frame_depart(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None, title = "桥梁信息管理系统")
        self.CreateStatusBar()  # A Statusbar in the bottom of the window

        #桥梁信息输入那里有两个界面，有两个函数，导致变量不能共享，故在此初始化。待解决，应该用一个函数，这样占内存小一点
        self.askmoney,self.reason4askmoney,self.bridgename,self.detecttime,self.detecttype,self.parentWeb = ["","","","","",""]

        # 顶部的菜单项
        filemenu= wx.Menu()
        upermenu = wx.Menu()

        # 向菜单项添加about与exit两项，中间以横线分割
        self.bumem_importfiel = filemenu.Append(wx.ID_ADD,"导入","在录入下具体信息录入时才可用")
        self.bumem_importfiel.Enable(False)
        self.bumen_writein = filemenu.Append(wx.ID_ABOUT, "录入"," 正在录入 ")
        self.bumem_search = filemenu.Append(wx.ID_HELP_SEARCH, "项目检索"," 查询项目级桥梁信息 ")
        # filemenu.AppendSeparator()
        # self.bumen_exit = filemenu.Append(wx.ID_EXIT,"E&xit"," 退出程序 ")
        self.uper_givemoney = upermenu.Append(wx.ID_HELP, "预算批示", "批示项目级预算")
        self.uper_webinfosearch = upermenu.Append(wx.ID_HARDDISK,"网级项目检索","网级桥梁信息查询")
        # self.uper_webinfosearch.Enable(False)         #使此菜单项无效

        # 创建菜单栏并且将前面的菜单项捆绑进去
        menuBar = wx.MenuBar()               #创建菜单栏
        menuBar.Append(filemenu,"操作")      #将菜单项"filemenu"放入菜单栏并且取名为。。。
        menuBar.Append(upermenu,"高级")
        self.SetMenuBar(menuBar)             #将菜单栏放入Frame

        self.panelwritein = panel_writein(self)
        self.panelwritein.Hide()
        self.paneldetail = panel_detail(self)
        self.paneldetail.Hide()


        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(self.panelbumen, 1, wx.EXPAND)
        self.sizer.Add(self.panelwritein, 1, wx.EXPAND)
        self.sizer.Add(self.paneldetail, 1 , wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_MENU,self.writein, self.bumen_writein)

        # self.Bind(wx.EVT_MENU,self.search, self.bumem_search)

        self.panelwritein.choice_2.Bind( wx.EVT_CHOICE,self.choice4money )
        self.panelwritein.bt_7.Bind( wx.EVT_BUTTON,self.detailinfo )

        self.paneldetail.subbtn.Bind(wx.EVT_BUTTON,self.submitdetail)

    def writein(self , event):
        self.panelwritein.Show()
        self.Layout()

    def choice4money(self,event):
        self.whethermoney = self.panelwritein.choice_2.GetStringSelection()
        if self.whethermoney == u"否":        #出错提醒(故加u):Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
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
        self.askmoney = self.panelwritein.input_6.GetValue()
        self.reason4askmoney = self.panelwritein.input_5.GetValue()

        print type(self.askmoney),self.reason4askmoney,self.bridgename,type(self.detecttime),self.detecttype,self.parentWeb
        if self.bridgename=="" or self.detecttime=="" or self.detecttype == u"" or self.parentWeb=="":
            self.dialogue_info = wx.Dialog(self,-1,"提示框",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n请全部输入\n不能留空",style = wx.ALIGN_CENTER)
            self.dialogue_info.ShowModal()
        else:
            self.panelwritein.Hide()
            self.paneldetail.Show()
            self.Layout()

            self.bumem_importfiel.Enable(True)
            self.Bind(wx.EVT_MENU,self.importfile, self.bumem_importfiel)

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
        sheet1.write(3,0,'是否报预算：'.decode("gbk"))
        sheet1.write(3,1,self.whethermoney)
        sheet1.write(4,0,"申报费用：".decode("gbk"))
        sheet1.write(4,1,self.askmoney)
        sheet1.write(5,0,"申报陈述".decode("gbk"))
        sheet1.write(5,1,self.reason4askmoney)
        for i in range(rowflag):
            for j in range(columnflag):
                sheet1.write(i+8,j,self.paneldetail.griddetail.GetCellValue(i,j))
        # 保存该excel文件,有同名文件时直接覆盖
        workbook.save(r'templates\%s.xls'%(self.bridgename+self.detecttime))
        print '创建excel文件完成'

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



app = wx.App()
frame1 = frame_login()
frame1.Show()
app.MainLoop()