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
        wx.Frame.__init__(self,None,size=(300, 250),pos = (520,260),style = wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN, title = "��¼")
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
            self.dialogue = wx.Dialog(self,-1,"��ʾ��",size = (200,150))
            self.errorlabel = wx.StaticText(self.dialogue,-1,"\n\n��������û�������������\n��������ȷ���û���������\n���û����ѡ�÷ÿ�ģʽ",style = wx.ALIGN_CENTER)
            self.dialogue.ShowModal()

class panel_writein(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.label_1 = wx.StaticText( self, -1, '������',pos = (550,150))
        self.input_1 = wx.TextCtrl(self, -1,pos = (650,150))
        self.label_2 = wx.StaticText( self, -1, '�������',pos = (550,200))
        mylist_1 = ['�ճ����','���ڼ��','������']
        self.choice_1 = wx.Choice(self, -1, choices = mylist_1,pos = (650,200),size=(100,50))
        self.label_3 = wx.StaticText(self,-1,"���ʱ��", pos=(550,250))
        self.input_3 = wx.TextCtrl(self, -1, pos = (650,250))
        self.label_3_5 = wx.StaticText(self,-1,"��������", pos=(550,300))
        self.input_3_5 = wx.TextCtrl(self, -1, pos = (650,300))
        self.label_4 = wx.StaticText(self,-1,"�Ƿ��걨ά�޷ѣ�",pos=(550,350))
        mylist_2 = ['��','��']
        self.choice_2 = wx.Choice(self, -1, choices = mylist_2,pos = (650,350),size=(100,50))
        self.label_6 = wx.StaticText(self,-1,"�걨���ã�",pos=(550,400))
        self.input_6 = wx.TextCtrl(self,-1,pos = (650,400))
        self.label_5 = wx.StaticText(self,-1,"�걨������",pos=(550,450))
        self.input_5 = wx.TextCtrl(self,-1,pos = (650,450),size = (300,150), style=wx.TE_MULTILINE )
        self.bt_7 = wx.Button( self , -1,label = "������ϸҳ" ,pos = (880,620))

class panel_detail(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.griddetail = gridlib.Grid(self)
        self.griddetail.CreateGrid(100,50)
        self.subbtn = wx.Button(self,-1,label = "�ύ����")
        self.subbtn.SetBackgroundColour("black")
        self.subbtn.SetForegroundColour("white")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.subbtn, 0, wx.EXPAND)
        sizer.Add(self.griddetail, 0, wx.EXPAND)

        self.SetSizer(sizer)


class frame_depart(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None, title = "������Ϣ����ϵͳ")
        self.CreateStatusBar()  # A Statusbar in the bottom of the window

        #������Ϣ�����������������棬���������������±������ܹ������ڴ˳�ʼ�����������Ӧ����һ������������ռ�ڴ�Сһ��
        self.askmoney,self.reason4askmoney,self.bridgename,self.detecttime,self.detecttype,self.parentWeb = ["","","","","",""]

        # �����Ĳ˵���
        filemenu= wx.Menu()
        upermenu = wx.Menu()

        # ��˵������about��exit����м��Ժ��߷ָ�
        self.bumem_importfiel = filemenu.Append(wx.ID_ADD,"����","��¼���¾�����Ϣ¼��ʱ�ſ���")
        self.bumem_importfiel.Enable(False)
        self.bumen_writein = filemenu.Append(wx.ID_ABOUT, "¼��"," ����¼�� ")
        self.bumem_search = filemenu.Append(wx.ID_HELP_SEARCH, "��Ŀ����"," ��ѯ��Ŀ��������Ϣ ")
        # filemenu.AppendSeparator()
        # self.bumen_exit = filemenu.Append(wx.ID_EXIT,"E&xit"," �˳����� ")
        self.uper_givemoney = upermenu.Append(wx.ID_HELP, "Ԥ����ʾ", "��ʾ��Ŀ��Ԥ��")
        self.uper_webinfosearch = upermenu.Append(wx.ID_HARDDISK,"������Ŀ����","����������Ϣ��ѯ")
        # self.uper_webinfosearch.Enable(False)         #ʹ�˲˵�����Ч

        # �����˵������ҽ�ǰ��Ĳ˵��������ȥ
        menuBar = wx.MenuBar()               #�����˵���
        menuBar.Append(filemenu,"����")      #���˵���"filemenu"����˵�������ȡ��Ϊ������
        menuBar.Append(upermenu,"�߼�")
        self.SetMenuBar(menuBar)             #���˵�������Frame

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
        if self.whethermoney == u"��":        #��������(�ʼ�u):Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
            self.panelwritein.input_5.Enable( False )
            self.panelwritein.input_6.Enable( False )

        elif self.whethermoney == u"��":      #��û����������˷���ٵ���������������Ȼ��Ч
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
            self.dialogue_info = wx.Dialog(self,-1,"��ʾ��",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n��ȫ������\n��������",style = wx.ALIGN_CENTER)
            self.dialogue_info.ShowModal()
        else:
            self.panelwritein.Hide()
            self.paneldetail.Show()
            self.Layout()

            self.bumem_importfiel.Enable(True)
            self.Bind(wx.EVT_MENU,self.importfile, self.bumem_importfiel)

    def submitdetail(self,event):
        # Ӧ������������x��y��ȷ��������һ��x*y�����ݿ�
        # if self.paneldetail.griddetail.GetCellValue(3,3) is None:           #GetValue��������unicode
        #     print "none"
        # elif self.paneldetail.griddetail.GetCellValue(3,3) == "":
        #     print "no"
        # else:
        #     print "nono"                                                     #����ʵ�鷢���ǿգ�������None
        rowflag,columnflag = 0,0
        while self.paneldetail.griddetail.GetCellValue(rowflag,0) != "":
            rowflag+=1
        while self.paneldetail.griddetail.GetCellValue(0,columnflag) != "":
            columnflag+=1
        print rowflag,columnflag            #ʵ����������

        #����Ϊexcel
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
        #��sheetҳ��д������
        sheet1.write(0,0,"����".decode("gbk"))
        sheet1.write(0,1,self.bridgename)
        sheet1.write(1,0,"������ͣ�".decode("gbk"))
        sheet1.write(1,1,self.detecttype)
        sheet1.write(2,0,"���ʱ��".decode("gbk"))
        sheet1.write(2,1,self.detecttime)
        sheet1.write(3,0,'�Ƿ�Ԥ�㣺'.decode("gbk"))
        sheet1.write(3,1,self.whethermoney)
        sheet1.write(4,0,"�걨���ã�".decode("gbk"))
        sheet1.write(4,1,self.askmoney)
        sheet1.write(5,0,"�걨����".decode("gbk"))
        sheet1.write(5,1,self.reason4askmoney)
        for i in range(rowflag):
            for j in range(columnflag):
                sheet1.write(i+8,j,self.paneldetail.griddetail.GetCellValue(i,j))
        # �����excel�ļ�,��ͬ���ļ�ʱֱ�Ӹ���
        workbook.save(r'templates\%s.xls'%(self.bridgename+self.detecttime))
        print '����excel�ļ����'

    def importfile(self,event):
        #������ļ����ڣ�����excel�ļ�·���ӿ�
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.absolutefileroute = self.dirname+'\\'+self.filename           #���ش��ļ��ľ���·��
        dlg.Destroy()

        #�����ǵ���excel��grid��
            #��һ��workbook
        workbook = xlrd.open_workbook(self.absolutefileroute)
        # workbook = xlrd.open_workbook(r'templates\test1.xls')
            #ץȡ����sheetҳ������
        worksheets = workbook.sheet_names()
        # print('worksheets is %s' %worksheets)
            #��λ��sheet1
        worksheet1 = workbook.sheet_by_name(u'sheet1')
            #����sheet1��������row
        num_rows = worksheet1.nrows
        for curr_row in range(num_rows):
            row = worksheet1.row_values(curr_row)
            # print('row%s is %s' %(curr_row,row))
            #����sheet1��������col
        num_cols = worksheet1.ncols
        for curr_col in range(num_cols):
            col = worksheet1.col_values(curr_col)
            # print('col%s is %s' %(curr_col,col))
            #����sheet1�����е�Ԫ��cell
        for rown in range(num_rows):
            for coln in range(num_cols):
                cell = worksheet1.cell_value(rown,coln)
                self.paneldetail.griddetail.SetCellValue(rown,coln,cell)



app = wx.App()
frame1 = frame_login()
frame1.Show()
app.MainLoop()