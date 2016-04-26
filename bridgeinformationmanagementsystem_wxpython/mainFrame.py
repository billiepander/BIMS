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

#软件主界面
class frame_depart(wx.Frame):
    def __init__(self,id):
        wx.Frame.__init__(self,None, title = "桥梁信息管理系统")
        self.id = id
        t = threading.Thread(target=self.yubeidui)
        t.start()
        #桥梁信息输入那里有两个界面，有两个函数，导致变量不能共享，故在此初始化。待解决，应该用一个函数，这样占内存小一点
        self.routestring,self.mainbroken,self.askmoney,self.reason4askmoney,self.bridgename,self.detecttime,self.detecttype,self.parentWeb,self.bridgerate = ["","","","","","","","",""]
        self.search_bridgename,self.search_detecttype,self.search_detectime,self.result = ["","","",""]

        self.menubarOutLook()   #完成主界面菜单部分的外观显示

        self.preMainSizer()     #给主frame绑定sizer并初始化几个panel

        self.bindItem()     #给每个菜单项都绑定事件

    def menubarOutLook(self):
        self.CreateStatusBar()  # A Statusbar in the bottom of the window
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
        self.bumem_gis = filemenu.Append(wx.ID_PREVIEW_GOTO, "GIS查看","地图查看桥梁信息")
        self.uper_SearchItemHis = upermenu.Append(wx.ID_EDIT, "单项桥梁历史纪录", "查看单项桥梁随各时间的质量变化")
        self.uper_givemoney = upermenu.Append(wx.ID_HELP, "单项预算表查看与批示", "单项预算表查看与批示")
        self.uper_ratifyWebMoney = upermenu.Append(wx.ID_APPLY,"网级预算查看与批示","网级预算查看与批示")
        self.uper_webinfosearch = upermenu.Append(wx.ID_HARDDISK,"网级项目检索","网级桥梁信息查询")
        self.doctment = helpmenu.Append(wx.ID_ANY,"帮助文档","查看产品说明书")
        self.callmaker = helpmenu.Append(wx.ID_FILE1,"联系作者","查看软件作者联系信息")

        # 创建菜单栏并且将前面的菜单项捆绑进去
        menuBar = wx.MenuBar()               #创建菜单栏
        menuBar.Append(filemenu,"操作")      #将菜单项"filemenu"放入菜单栏并且取名为。。。
        menuBar.Append(upermenu,"高级")
        menuBar.Append(helpmenu,"帮助")
        self.SetMenuBar(menuBar)             #将菜单栏放入Frame


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
        #绑定菜单事件
        self.Bind(wx.EVT_MENU,self.writein, self.bumen_writein)
        self.Bind(wx.EVT_MENU,self.search, self.bumem_search)
        self.Bind(wx.EVT_MENU,self.gis, self.bumem_gis)
        self.Bind(wx.EVT_MENU,self.searchitemhis, self.uper_SearchItemHis)
        self.Bind(wx.EVT_MENU,self.ratifyitemmoney, self.uper_givemoney)
        self.Bind(wx.EVT_MENU,self.ratifyWebMoney, self.uper_ratifyWebMoney)
        self.Bind(wx.EVT_MENU,self.pieSearch, self.uper_webinfosearch)
        #输入页下拉框以及按钮的事件绑定
        self.panelwritein.choice_2.Bind( wx.EVT_CHOICE,self.choice4money )
        self.panelwritein.bt_7.Bind( wx.EVT_BUTTON,self.detailinfo )
        self.paneldetail.subbtn.Bind(wx.EVT_BUTTON,self.submitdetail)
        #项目搜索页的事件绑定
        self.panelsearch.bt.Bind(wx.EVT_BUTTON,self.submitsearch)

    #此处待优化，在启动软件就绘制好网级饼图放入了templates
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
        #由于其中有些实例是在hide时没有的，若用列表循环隐藏会出现报实例不存在的错误，待解决
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
        if self.whethermoney == u"否":        #出错提醒(故加u):Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
            self.panelwritein.input_5.SetValue("")
            self.panelwritein.input_6.SetValue("")
            self.panelwritein.input_5.Enable( False )
            self.panelwritein.input_6.Enable( False )

        elif self.whethermoney == u"是":      #若没有这个则点击了否后再点击是两个输入框任然无效
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
        # print rowflag,columnflag            #实际输入区域

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
        sql = "INSERT INTO bridgeinfo VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s' )" % (self.bridgename, self.detecttype, self.detecttime, self.parentWeb, self.bridgerate,self.mainbroken,self.whethermoney,self.askmoney,self.reason4askmoney,"waiting",str(abs(hash(self.routestring))))
        MySqlUnit.exe_update(sql)


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
            self.dialogue_info = wx.Dialog(self,-1,"提示框",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n桥名和检测类型\n不能留空",style = wx.ALIGN_CENTER)
            self.dialogue_info.ShowModal()
        if self.search_detectime != "":
            # self.dicthelp = {"日常检查":"normal","定期检测":"regular","特殊检测":"special"}
            search = "select * from bridgeinfo WHERE BridgeName = '%s' AND DetectType = '%s' AND detecttime LIKE '%s%%'" % (self.search_bridgename,self.search_detecttype,self.search_detectime)
        else:
            search = "select * from bridgeinfo WHERE BridgeName = '%s' AND DetectType = '%s'"%(self.search_bridgename,self.detecttype)
        self.result = MySqlUnit.exe_search(search)
        if not self.result:
            self.dialogue_info = wx.Dialog(self,-1,"提示框",size = (300,150),pos=(600,300))
            self.errorlabel_info = wx.StaticText(self.dialogue_info,-1,"\n\n并没有相关数据\n请检查输入",style = wx.ALIGN_CENTER)
            self.dialogue_info.ShowModal()
        else:
            self.panelshowsearchresult = panel_searchResultShow(self,len(self.result),bridgename= self.search_bridgename)
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

            self.panelshowsearchresult.SetLabel( "这是第%d条数据"%(self.rank+1))

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
        self.dbpara = ['桥名','检测类型','检测时间','所属网络','项目评级','主要问题','是否申报维修费','申报费用','申报陈述','申报进度']
        try:
            int(self.transferTo)
            self.rank = int(self.transferTo) - 1
        except:
            self.rank = 0

        self.panelshowsearchresult.rankinfo.SetLabelText("这是第%d条数据"%(self.rank+1))

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
        search = "select * from bridgeinfo WHERE WhetherDeclare = '%s' ORDER BY DetectTime"%u"是"
        self.result_money = MySqlUnit.exe_search(search)[:8]
        self.panelMoneyTable = panel_MoneyTable(self,self.result_money)
        if self.id == 'bumen':
            for i in range(8):
                facebtn = self.panelMoneyTable.FindWindowByName("第%d条申报信息"%i)
                facebtn.Enable(False)
        self.sizer.Add(self.panelMoneyTable, 1 , wx.EXPAND)
        self.panelMoneyTable.Show()
        self.Layout()

    def SeeMap(self,event,item):
        driver = webdriver.Chrome()
        driver.get(r'http://map.baidu.com/')
        # <input id="sole-input" class="searchbox-content-common" type="text" name="word" autocomplete="off" maxlength="256" placeholder="搜地点、查公交、找路线" value="">
        sousuo = driver.find_element_by_id('sole-input')
        sousuo.send_keys(item)
        # <button id="search-button" data-title="搜索" data-tooltip="1"></button>
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
                    facebtn = self.panelRatifiWebMoney.FindWindowByName("第%d个按钮"%i)
                    faceinpt = self.panelRatifiWebMoney.FindWindowByName("第%d个网络"%i)
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
