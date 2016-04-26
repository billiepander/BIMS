#coding:gbk
import wx, xlwt, xlrd, os, shutil, threading
from selenium import webdriver
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
font = FontProperties(fname=r"c:\windows\Fonts\simsun.ttc",size=11)
import MySqlUnit
from PanelPieSearch import panel_WebSituation
from PanelRatifyWebMoney import panel_RatifyWebMoney
from PanelMoneyTable import panel_MoneyTable
from PanelLineSearch import panel_ItemSituation
from PanelWriteIn import panel_writein, panel_detail
from PanelSearch import panel_search
from PanelShowSearchResult import panel_searchResultShow
from PanelGIS import Panel_gis
from SaveDocAndPDF import savedocpdf

#���������
class frame_depart(wx.Frame):
    def __init__(self,id):
        wx.Frame.__init__(self,None, title = "������Ϣ����ϵͳ")
        self.id = id
        t = threading.Thread(target=self.yubeidui)
        t.start()
        #������Ϣ�����������������棬���������������±������ܹ������ڴ˳�ʼ�����������Ӧ����һ������������ռ�ڴ�Сһ��
        self.routestring,self.mainbroken,self.askmoney,self.reason4askmoney,self.bridgename,self.detecttime,self.detecttype,self.parentWeb,self.bridgerate = ["","","","","","","","",""]
        self.search_bridgename,self.search_detecttype,self.search_detectime,self.result = ["","","",""]

        self.menubarOutLook()   #���������˵����ֵ������ʾ

        self.preMainSizer()     #����frame��sizer����ʼ������panel

        self.bindItem()     #��ÿ���˵�����¼�

    def menubarOutLook(self):
        self.CreateStatusBar()  # A Statusbar in the bottom of the window
        # �����Ĳ˵���
        filemenu= wx.Menu()
        upermenu = wx.Menu()
        helpmenu = wx.Menu()

        # ��˵������about��exit����м��Ժ��߷ָ�
        self.bumem_importfiel = filemenu.Append(wx.ID_ADD,"����excel�ļ�","��¼���µľ�����Ϣ¼��ʱ���ڵ���excel�ļ�")
        self.bumem_importfiel.Enable(False)
        self.bumem_importimage = filemenu.Append(wx.ID_FILE,"����ͼƬ","��¼���µľ�����Ϣ¼��ʱ���ڵ���ͼ���ļ�")
        self.bumem_importimage.Enable(False)
        self.bumen_writein = filemenu.Append(wx.ID_ABOUT, "¼��"," ����¼�� ")
        self.bumem_search = filemenu.Append(wx.ID_HELP_SEARCH, "��Ŀ����"," ��ѯ��Ŀ��������Ϣ ")
        self.bumem_gis = filemenu.Append(wx.ID_PREVIEW_GOTO, "GIS�鿴","��ͼ�鿴������Ϣ")
        self.uper_SearchItemHis = upermenu.Append(wx.ID_EDIT, "����������ʷ��¼", "�鿴�����������ʱ��������仯")
        self.uper_givemoney = upermenu.Append(wx.ID_HELP, "����Ԥ���鿴����ʾ", "����Ԥ���鿴����ʾ")
        self.uper_ratifyWebMoney = upermenu.Append(wx.ID_APPLY,"����Ԥ��鿴����ʾ","����Ԥ��鿴����ʾ")
        self.uper_webinfosearch = upermenu.Append(wx.ID_HARDDISK,"������Ŀ����","����������Ϣ��ѯ")
        self.doctment = helpmenu.Append(wx.ID_ANY,"�����ĵ�","�鿴��Ʒ˵����")
        self.callmaker = helpmenu.Append(wx.ID_FILE1,"��ϵ����","�鿴���������ϵ��Ϣ")

        # �����˵������ҽ�ǰ��Ĳ˵��������ȥ
        menuBar = wx.MenuBar()               #�����˵���
        menuBar.Append(filemenu,"����")      #���˵���"filemenu"����˵�������ȡ��Ϊ������
        menuBar.Append(upermenu,"�߼�")
        menuBar.Append(helpmenu,"����")
        self.SetMenuBar(menuBar)             #���˵�������Frame


    def preMainSizer(self):
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



    def bindItem(self):
        #�󶨲˵��¼�
        self.Bind(wx.EVT_MENU,self.writein, self.bumen_writein)
        self.Bind(wx.EVT_MENU,self.search, self.bumem_search)
        self.Bind(wx.EVT_MENU,self.gis, self.bumem_gis)
        self.Bind(wx.EVT_MENU,self.searchitemhis, self.uper_SearchItemHis)
        self.Bind(wx.EVT_MENU,self.ratifyitemmoney, self.uper_givemoney)
        self.Bind(wx.EVT_MENU,self.ratifyWebMoney, self.uper_ratifyWebMoney)
        self.Bind(wx.EVT_MENU,self.pieSearch, self.uper_webinfosearch)
        #����ҳ�������Լ���ť���¼���
        self.panelwritein.choice_2.Bind( wx.EVT_CHOICE,self.choice4money )
        self.panelwritein.bt_7.Bind( wx.EVT_BUTTON,self.detailinfo )
        self.paneldetail.subbtn.Bind(wx.EVT_BUTTON,self.submitdetail)
        #��Ŀ����ҳ���¼���
        self.panelsearch.bt.Bind(wx.EVT_BUTTON,self.submitsearch)

    #�˴����Ż�������������ͻ��ƺ�������ͼ������templates
    def yubeidui(self):
        searchWebName = "select FatherWeb from bridgeinfo GROUP by FatherWeb"
        WebNames = MySqlUnit.exe_search(searchWebName)
        for i in WebNames:
            for j in i:
                search = "select COUNT(QualityLevel), QualityLevel,FatherWeb from bridgeinfo WHERE FatherWeb='%s' GROUP BY QualityLevel"%j
                result = MySqlUnit.exe_search(search)
                self.sumnumber = 0
                self.sumnumber = reduce(lambda x,y:x+y,[z[0] for z in result])
                # make a square figure and axes
                plt.figure(1, figsize=(4.7,4.7))
                ax = plt.axes([0.1, 0.1, 0.8, 0.8])
                # labels = ['A', 'B', 'C', 'D']
                # fracs = [result[0][0], result[1][0], result[2][0], result[3][0]]
                # explode=(0, 0, 0, 0.05)       #ÿ���ļ������Ӧ��labels������Hogs��ļ�����0.05
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

                plt.title(result[0][2]+u'����״��\n',fontsize=16, color="red",fontproperties=font)
                plt.xlabel(u'����%d������'%self.sumnumber,fontproperties=font)
                plt.savefig(".\\templates\\%d.png"%abs(hash(j)))
                plt.close()

    def hideAllPanel(self):
        #����������Щʵ������hideʱû�еģ������б�ѭ�����ػ���ֱ�ʵ�������ڵĴ��󣬴����
        # allpanels = [self.panelshowsearchresult,self.panelMoneyTable, self.paneldetail,self.panelRatifiWebMoney,self.panelwritein,self.panelsearch,self.panelShowWebPie,self.panelItemSearch,self.panelgis]
        #
        # for i in range(len(allpanels)):
        #     try:
        #         allpanels[i].Hide()
        #     except:
        #         pass

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
        try:
            self.panelgis.Hide()
        except:
            pass


    def writein(self , event):
        self.hideAllPanel()
        self.panelwritein.Show()
        self.Layout()

    def choice4money(self,event):
        self.whethermoney = self.panelwritein.choice_2.GetStringSelection()
        if self.whethermoney == u"��":        #��������(�ʼ�u):Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
            self.panelwritein.input_5.SetValue("")
            self.panelwritein.input_6.SetValue("")
            self.panelwritein.input_5.Enable( False )
            self.panelwritein.input_6.Enable( False )

        elif self.whethermoney == u"��":      #��û����������˷���ٵ���������������Ȼ��Ч
            self.panelwritein.input_5.Enable( True )
            self.panelwritein.input_6.Enable( True )

    def detailinfo( self,event ):
        self.bridgename = self.panelwritein.input_1.GetValue()
        self.detecttype = self.panelwritein.choice_1.GetStringSelection()
        self.detecttime = self.panelwritein.input_3.GetValue()
        self.parentWeb = self.panelwritein.input_3_5.GetValue()
        self.bridgerate = self.panelwritein.input_3_rate.GetValue()
        self.mainbroken = self.panelwritein.input_3_mainbroken.GetValue()
        self.askmoney = self.panelwritein.input_6.GetValue()
        self.reason4askmoney = self.panelwritein.input_5.GetValue()

        if self.bridgename=="" or self.detecttime=="" or self.detecttype == u"" or self.parentWeb=="":
            self.dialogue_info = wx.Dialog(self,-1,"��ʾ��",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n��ȫ������\n��������",style = wx.ALIGN_CENTER)
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
        # print rowflag,columnflag            #ʵ����������

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
        sheet1.write(3,0,"��Ŀ����".decode("gbk"))
        sheet1.write(3,1,self.bridgerate)
        sheet1.write(4,0,"��Ҫ����".decode("gbk"))
        sheet1.write(4,1,self.mainbroken)
        sheet1.write(5,0,'�Ƿ�Ԥ�㣺'.decode("gbk"))
        sheet1.write(5,1,self.whethermoney)
        sheet1.write(6,0,"�걨���ã�".decode("gbk"))
        sheet1.write(6,1,self.askmoney)
        sheet1.write(7,0,"�걨����".decode("gbk"))
        sheet1.write(7,1,self.reason4askmoney)
        for i in range(rowflag):
            for j in range(columnflag):
                sheet1.write(i+10,j,self.paneldetail.griddetail.GetCellValue(i,j))
        # �����excel�ļ�,��ͬ���ļ�ʱֱ�Ӹ���
        workbook.save(r'templates\%s\%s.xls'%(abs(hash(self.routestring)),self.routestring))

        #�������ݿ�
        sql = "INSERT INTO bridgeinfo VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s' )" % (self.bridgename, self.detecttype, self.detecttime, self.parentWeb, self.bridgerate,self.mainbroken,self.whethermoney,self.askmoney,self.reason4askmoney,"waiting",str(abs(hash(self.routestring))))
        MySqlUnit.exe_update(sql)


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

    def importimage(self,event):
        #������ļ����ڣ�����excel�ļ�·���ӿ�
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.absoluteimageroute = self.dirname+'\\'+self.filename           #���ش��ļ��ľ���·��
        dlg.Destroy()

        shutil.copyfile(self.absoluteimageroute,r"templates\%s\%s"%(abs(hash(self.routestring)),self.filename))

    def gis(self,event):
        self.hideAllPanel()
        self.panelgis = Panel_gis(self)
        self.sizer.Add(self.panelgis, 1 , wx.EXPAND)
        self.panelgis.Show()
        self.Layout()

    def search(self,event):
        self.hideAllPanel()
        self.panelsearch.Show()
        self.Layout()

    def submitsearch(self,event):
        self.search_bridgename = self.panelsearch.input_1.GetValue()
        self.search_detecttype = self.panelsearch.choice_1.GetStringSelection()
        self.search_detectime = self.panelsearch.input_3.GetValue()
        if self.search_bridgename == "" or self.search_detecttype == "":
            self.dialogue_info = wx.Dialog(self,-1,"��ʾ��",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n�����ͼ������\n��������",style = wx.ALIGN_CENTER)
            self.dialogue_info.ShowModal()
        if self.search_detectime != "":
            # self.dicthelp = {"�ճ����":"normal","���ڼ��":"regular","������":"special"}
            search = "select * from bridgeinfo WHERE BridgeName = '%s' AND DetectType = '%s' AND detecttime LIKE '%s%%'" % (self.search_bridgename,self.search_detecttype,self.search_detectime)
        else:
            search = "select * from bridgeinfo WHERE BridgeName = '%s' AND DetectType = '%s'"%(self.search_bridgename,self.detecttype)
        self.result = MySqlUnit.exe_search(search)
        if not self.result:
            self.dialogue_info = wx.Dialog(self,-1,"��ʾ��",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n��û���������\n��������",style = wx.ALIGN_CENTER)
            self.dialogue_info.ShowModal()
        else:
            self.panelshowsearchresult = panel_searchResultShow(self,len(self.result),bridgename= self.search_bridgename)
            self.panelshowsearchresult.Hide()
            self.sizer.Add(self.panelshowsearchresult, 1 , wx.EXPAND)
            self.panelsearch.Hide()
            self.panelshowsearchresult.Show()
            self.Layout()


            self.transferTo = self.panelshowsearchresult.which2see.GetValue()
            self.dbpara = ['����','�������','���ʱ��','��������','��Ŀ����','��Ҫ����','�Ƿ��걨ά�޷�','�걨����','�걨����','�걨����']
            try:
                int(self.transferTo)
                self.rank = int(self.transferTo) - 1
            except:
                self.rank = 0

            self.panelshowsearchresult.SetLabel( "���ǵ�%d������"%(self.rank+1))

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
            self.Bind(wx.EVT_BUTTON,lambda evt,item=self.search_bridgename:self.SeeMap(evt,item),self.panelshowsearchresult.seebtn)
            self.Bind(wx.EVT_BUTTON,lambda evt,ToFile=(self.search_detectime+self.search_bridgename+self.search_detecttype):self.SavePrint(evt,ToFile),self.panelshowsearchresult.wordPDF)
            # self.choice.Bind(wx.EVT_CHOICE, lambda evt,mark=i,choice=self.choice:self.changewhichone(evt,mark,choice))

    def OnEnter(self,event):
        self.transferTo = self.panelshowsearchresult.which2see.GetValue()
        self.dbpara = ['����','�������','���ʱ��','��������','��Ŀ����','��Ҫ����','�Ƿ��걨ά�޷�','�걨����','�걨����','�걨����']
        try:
            int(self.transferTo)
            self.rank = int(self.transferTo) - 1
        except:
            self.rank = 0

        self.panelshowsearchresult.rankinfo.SetLabelText("���ǵ�%d������"%(self.rank+1))

        for i in range(10):
            if not self.result[self.rank][i]:
                self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
                self.panelshowsearchresult.griddetail.SetCellValue(i,1,"")
            else:
                self.panelshowsearchresult.griddetail.SetCellValue(i,0,self.dbpara[i])
                self.panelshowsearchresult.griddetail.SetCellValue(i,1,self.result[self.rank][i])

    def SeeDetailSearchResult(self,event):
        self.detailNum = int(self.panelshowsearchresult.which2see.GetValue())
        os.startfile( os.getcwd()+"\\templates\\"+ self.result[self.detailNum-1][10])

    def ratifyitemmoney(self,event):
        self.hideAllPanel()
        search = "select * from bridgeinfo WHERE WhetherDeclare = '%s' ORDER BY DetectTime"%u"��"
        self.result_money = MySqlUnit.exe_search(search)[:8]
        self.panelMoneyTable = panel_MoneyTable(self,self.result_money)
        if self.id == 'bumen':
            for i in range(8):
                facebtn = self.panelMoneyTable.FindWindowByName("��%d���걨��Ϣ"%i)
                facebtn.Enable(False)
        self.sizer.Add(self.panelMoneyTable, 1 , wx.EXPAND)
        self.panelMoneyTable.Show()
        self.Layout()

    def SeeMap(self,event,item):
        driver = webdriver.Chrome()
        driver.get(r'http://map.baidu.com/')
        # <input id="sole-input" class="searchbox-content-common" type="text" name="word" autocomplete="off" maxlength="256" placeholder="�ѵص㡢�鹫������·��" value="">
        sousuo = driver.find_element_by_id('sole-input')
        sousuo.send_keys(item)
        # <button id="search-button" data-title="����" data-tooltip="1"></button>
        clicli = driver.find_element_by_id('search-button')
        clicli.click()

    def SavePrint(self,event,ToFile):
        self.detailNum = int(self.panelshowsearchresult.which2see.GetValue())
        # os.startfile( os.getcwd()+"\\templates\\"+ self.result[self.detailNum-1][10])
        oriroute = os.getcwd()+"\\templates\\"+ self.result[self.detailNum-1][10]
        toroute = r'C:\Users\Administrator\Desktop\%s'%ToFile
        shutil.copytree(oriroute, toroute)
        savedocpdf(oriroute,toroute)


    def ratifyWebMoney(self,event):
        self.hideAllPanel()
        self.panelRatifiWebMoney = panel_RatifyWebMoney(self)
        if self.id == 'bumen' or 'shiji':
            for i in range(8):
                try:
                    facebtn = self.panelRatifiWebMoney.FindWindowByName("��%d����ť"%i)
                    faceinpt = self.panelRatifiWebMoney.FindWindowByName("��%d������"%i)
                    facebtn.Enable(False)
                    faceinpt.Enable(False)
                except:
                    pass
        self.sizer.Add(self.panelRatifiWebMoney, 1 , wx.EXPAND)
        self.panelRatifiWebMoney.Show()
        self.Layout()

    def pieSearch(self,event):
        self.hideAllPanel()
        self.panelShowWebPie  = panel_WebSituation(self)
        self.sizer.Add(self.panelShowWebPie, 1 , wx.EXPAND)
        self.panelShowWebPie.Show()
        self.Layout()

    def searchitemhis(self,event):
        self.hideAllPanel()
        self.panelItemSearch = panel_ItemSituation(self)
        self.sizer.Add(self.panelItemSearch, 1 , wx.EXPAND)
        self.panelItemSearch.Show()
        self.Layout()
