#coding:gbk
import wx,math,sys
import pandas as pd

class panel_showcal(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.printtext = wx.TextCtrl(self,-1,size=(1500,900), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

class frame_cal(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title = "ǿ�ȼ�����")
        self.showcal = panel_showcal(self)
        sys.stdout = self.showcal.printtext

class panel_cal(wx.Panel):
    magic = 0
    stable = {6:(28.3,7),16:(201.1,18.4),32:(804.2,35.8)}
    ctable = { u'C30':{u'fcd':13.8,u'ftk':1.39,u'Ec':3.00},u'C35':{u'fcd':16.1,u'ftk':1.52,u'Ec':3.15},u'C40':{u'fcd':18.4,u'ftk':1.65,u'Ec':3.25} }
    c12table = [(0.1,0.312),(0.2,0.291),(0.3,0.27),(0.4,0.25),(0.5,0.229),(0.6,0.209),(0.7,0.189),(0.8,0.171),(0.9,0.155),(1,0.141)]
    data=[[200,200,200,200,200],[237,216,194,180,173],[269,229,188,163,151],[321,249,178,136,116],[362,263,168,115,92],[396,273,158,99,73],[425,281,150,85,59],[481,291,130,61,36],[523,295,114,45,23],[583,296,87,26,10],[625,291,66,15,4],[682,277,35,4,1],[750,250,0,0,0],[828,201,-34,6,-1]]
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.setoutlook()
        self.checkbox_sidewalk.Bind(wx.EVT_CHECKBOX,self.whethersideway)
        self.bt.Bind(wx.EVT_BUTTON,self.calgo)
        self.sareahigh = {}
        self.parent = 0.0
        self.children = 0.0

        self.showframe = frame_cal()
        self.showframe.Hide()


    def setoutlook(self):
        self.label_design = wx.StaticText( self, -1, '��������������',pos = (300,50))
        self.label_con = wx.StaticText( self, -1, '��������',pos = (350,100))
        self.input_con = wx.TextCtrl(self, -1,pos = (450,100))
        self.label_t = wx.StaticText( self, -1, 'T�ν������:',pos = (350,150))
        self.label_bf = wx.StaticText( self, -1, "bf'��",pos = (370,200))
        self.input_bf = wx.TextCtrl(self, -1,pos = (450,200))
        self.label_hf = wx.StaticText(self,-1,"hf'��", pos=(370,250))
        self.input_hf = wx.TextCtrl(self, -1, pos = (450,250))
        self.label_h = wx.StaticText(self,-1,"h��", pos=(380,300))
        self.input_h = wx.TextCtrl(self, -1, pos = (450,300))
        self.label_b = wx.StaticText(self,-1,"b��", pos=(380,350))
        self.input_b = wx.TextCtrl(self, -1, pos = (450,350))

        self.label_steel = wx.StaticText(self,-1,"��������", pos=(350,400))

        self.input_s1 = wx.TextCtrl(self,-1,pos = (380,450),size = (100,25))
        self.label_s1 = wx.StaticText(self,-1,"��", pos=(495,450))
        self.input_s11 = wx.TextCtrl(self,-1,pos = (520,450),size = (100,25))

        self.input_s2 = wx.TextCtrl(self,-1,pos = (380,500),size = (100,25))
        self.label_s2 = wx.StaticText(self,-1,"��", pos=(495,500))
        self.input_s21 = wx.TextCtrl(self,-1,pos = (520,500),size = (100,25))

        #ʵ�ʺ��أ�
        self.label_actual = wx.StaticText( self, -1, 'T���½����۰������',pos = (700,50))

        self.label_surface = wx.StaticText( self, -1, '������װ��',pos = (750,100))
        self.input_aldepth = wx.TextCtrl(self,-1,pos = (780,150),size = (50,25))
        self.label_surfal = wx.StaticText(self,-1,"m���������", pos=(840,155))
        self.label_sw1 = wx.StaticText(self,-1,"; �ضȣ�", pos=(915,155))
        self.input_alweight = wx.TextCtrl(self,-1,pos = (965,150),size = (50,25))
        self.label_ss1 = wx.StaticText(self,-1,"KN/m^3", pos=(1028,155))

        self.input_condepth = wx.TextCtrl(self,-1,pos = (780,200),size = (50,25))
        self.label_surfcon = wx.StaticText(self,-1,"m���������", pos=(840,205))
        self.label_sw2 = wx.StaticText(self,-1,"; �ضȣ�", pos=(915,205))
        self.input_conweight = wx.TextCtrl(self,-1,pos = (965,200),size = (50,25))
        self.label_ss2 = wx.StaticText(self,-1,"KN/m^3", pos=(1028,205))

        self.label_t = wx.StaticText(self,-1,"T���������ضȣ�", pos=(750,255))
        self.input_tweight = wx.TextCtrl(self,-1,pos = (880,250))
        self.label_ss3 = wx.StaticText(self,-1,"KN/m^3", pos=(1028,255))

        self.label_l = wx.StaticText(self,-1,"T������羶 l ��", pos=(750,305))
        self.input_l = wx.TextCtrl(self,-1,pos = (880,300))
        self.label_ss4 = wx.StaticText(self,-1,"m", pos=(1028,305))

        self.label_lo = wx.StaticText(self,-1,"��ļ���羶 lo ��", pos=(750,355))
        self.input_lo = wx.TextCtrl(self,-1,pos = (880,350))
        self.label_ss5 = wx.StaticText(self,-1,"m", pos=(1028,355))

        self.checkbox_diaphragm = wx.CheckBox(self,-1,"�Ƿ��к����",pos=(751,400))
        self.checkbox_sidewalk = wx.CheckBox(self,-1,"�Ƿ������е�������",pos=(950,400))

        self.label_num = wx.StaticText(self,-1,"��", pos=(750,455))
        self.input_num = wx.TextCtrl(self,-1,pos = (770,450),size=(50,25))
        self.label_ss6 = wx.StaticText(self,-1,"����������", pos=(830,455))

        self.label_width = wx.StaticText(self,-1,"�����", pos=(750,505))
        self.input_widthmain = wx.TextCtrl(self,-1,pos = (800,500),size=(50,25))
        self.label_ss7 = wx.StaticText(self,-1,"+ 2 x", pos=(860,505))
        self.input_widthsideway = wx.TextCtrl(self,-1,pos = (900,500),size=(50,25))

        self.bt = wx.Button( self , -1,label = "��ʼ����" ,pos = (920,620))


    def whethersideway(self,event):
        self.wahaha = self.checkbox_sidewalk.GetValue()
        if self.wahaha:
            self.input_widthsideway.Enable(True)
        else:
            self.input_widthsideway.Enable(False)

    def calgo(self,event):
        self.concrete = self.input_con.GetValue()
        self.bf = float(self.input_bf.GetValue())
        self.hf = float(self.input_hf.GetValue())
        self.h = float(self.input_h.GetValue())
        self.b = float(self.input_b.GetValue())
        self.steel = []
        self.steel.append((float(self.input_s11.GetValue().encode()),float(self.input_s1.GetValue().encode())))
        self.steel.append((float(self.input_s21.GetValue().encode()),float(self.input_s2.GetValue().encode())))

        self.aldepth = float(self.input_aldepth.GetValue())
        self.alweight = float(self.input_alweight.GetValue())
        self.condepth = float(self.input_condepth.GetValue())
        self.conweight = float(self.input_conweight.GetValue())
        self.tweight = float(self.input_tweight.GetValue())
        self.l = float(self.input_l.GetValue())
        self.lo = float(self.input_lo.GetValue())
        self.diaphragm = self.checkbox_diaphragm.GetValue()
        self.sidewalk = self.checkbox_sidewalk.GetValue()
        self.num = float(self.input_num.GetValue())
        self.widthmain = float(self.input_widthmain.GetValue())
        self.widthsideway = float(self.input_widthsideway.GetValue())

        #------------------------------------�������������濹�������Mu����
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~����½Ӽ�֧T��ǿ������~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "\n================================���������濹�������Mu����===================================="
        for i in self.steel:
            self.sareahigh[i[0]] = ( i[1]*self.stable[i[0]][0] , i[1]*self.stable[i[0]][1]/4)

        for i,j in self.sareahigh.items():
            self.parent += j[0]

        for i,j in self.sareahigh.items():
            self.children += j[0]*( 35+j[1] )
        self.children += self.sareahigh[ self.steel[0][0] ][1] * self.stable[ self.steel[1][0] ][0]*2

        self.aas = self.children / self.parent
        print 'as:',self.aas,'mm'
        self.ho = self.h - self.aas

        self.uperM = self.ctable[self.concrete][u'fcd']*self.bf*self.hf
        self.bottomM = self.parent*280

        self.x = self.bottomM / self.uperM * self.hf
        print u"��ѹ���߶ȣ�",self.x,'mm'

        if self.x < self.hf:
            print u'���ڵ�һ�����'

        self.Mu = (self.ho - self.x/2) * self.ctable[self.concrete][u'fcd'] * self.bf * self.x

        print u'�����濹�������Mu��',self.Mu/1000000,'KN.m'

        #---------------------------------------�����-----------------------------------------
        print "=================================�����========================================="
        self.sumg = (self.aldepth*self.alweight + self.condepth*self.conweight + self.tweight*self.hf/1000)
        self.Mag = self.sumg * self.lo * self.lo
        self.Qag = self.sumg * self.lo
        print u"����Mag:",self.Mag,'KN.m'

        self.a1 = 0.2 + 2*( self.condepth + self.aldepth )
        self.b1 = 0.6 + 2*( self.condepth + self.aldepth )
        self.a = self.a1 + 2*self.lo + 1.4
        self.Map = 1.3 * 70 * (self.lo - self.b1/4) / self.a
        self.Qap = 1.3 * 70 / self.a
        print u"����Map��",self.Map,'KN.m'

        self.Ma = self.Mag + self.Map
        self.Qa = self.Qag + self.Qap
        print u"����ۺ����������",self.Ma,'KN.m'

        #----------------------------------�����������ز���---------------------------------
        print "\n==========================������������====================================="
        print "1)�����ؼ���"
        if not self.checkbox_sidewalk:
            self.widthsideway = 0

        self.g1 = self.tweight * ( self.b * self.h / 1000000 + self.hf * ( self.bf - self.b ) / 1000000 )
        print "\t����������ؼ��ȣ�",self.g1,'KN/m'
        if self.diaphragm:
            self.g2 = 0.07
        else:
            self.g2 = 0
        print "\t��������ؼ��ȣ�",self.g2,'KN/m'
        self.g3 = ( self.aldepth*self.alweight + self.condepth*self.conweight ) * self.widthmain / ( self.num*self.num*10 )
        print "\t������װ���ؼ��ȣ�",self.g3,'KN/m'
        if self.sidewalk:
            self.g4 = 2.0
        else:
            self.g4 = 0.0
        print "\t���������е���",self.g4,'KN/m'
        self.gall = self.g1 + self.g2 + self.g3 + self.g4
        print "\tȫ�����ؼ��ȣ�",self.gall,'KN/m'
        self.Mmiddle = self.gall*self.l*self.l/8
        print "\t���ϣ��������ؿ�����أ�",self.Mmiddle,'KN.m'

        print "2)�����ؼ���\n\t1]:����ֲ�ϵ�����㣨����½Ӱ巨��"
        self.e = ( self.b*self.h*self.h/2 + (self.bf-self.b)*self.hf*self.hf/2 ) / (self.b*self.h*10 + (self.bf-self.b)*self.hf*10)
        print "\t\t�������ĵ��������룺",self.e,'cm'
        self.I = (self.b*self.h**3/12 + (self.b*self.h)*(self.h/2-self.e)**2 + (self.bf-self.b)*self.hf**3/12 + (self.bf-self.b)*self.hf*(self.e-self.hf/2)**2)/10000
        print "\t\t����߾ࣺ",self.I,'cm^4'
        self.column = self.hf / self.bf
        self.c1 = self.aboutc(self.column)
        self.row = self.b / (self.h-self.hf)
        self.c2 = self.aboutc(self.row)
        self.It = (self.c1*self.bf*self.hf**3 + self.c2*(self.h-self.hf)*self.b**3)/10000
        print "\t\t��Ť�߾ࣺ",self.It,'cm^4'
        self.r = 5.8*self.I*(self.bf/(self.l*1000))**2/self.It
        self.B = 390*self.I*(self.hf/((self.bf-self.b)/2))**3 /((self.l*100)**4)
        self.effect = self.B/(1+self.r)
        if self.effect < 0.05:
            print "\t\tӰ��ϵ����",self.effect,"̫С������"

        flag = 0.0
        frame_1 = pd.DataFrame(self.data,columns=[u'��11',u'��12',u'��13',u'��14',u'��15'],index=[0.00,0.01,0.02,0.04,0.06,0.08,0.10,0.15,0.20,0.30,0.40,0.60,1.00,2.00])

        for i in range(len(frame_1.index)):
            if self.r > frame_1.index[i]:
                flag = i

        # print flag
        bottom,upper = {},{}
        bottom[frame_1.index[flag]] = frame_1.ix[frame_1.index[flag]].values
        upper[frame_1.index[flag+1]] = frame_1.ix[frame_1.index[flag+1]].values
        self.refct = self.change(bottom,upper,self.r)
        self.refct = map(lambda x:x/1000,self.refct)
        print "\t\t����ֲ�Ӱ��ϵ����",self.refct
        self.loo = 2*self.lo + self.b/1000
        self.xrange = self.loo*2.5 - self.widthsideway - 0.5
        self.a = (self.refct[1]-self.refct[0])/self.loo
        self.b = self.refct[0]-self.loo*self.a/2
        self.cars = 1
        while self.xrange > 0:
            if self.cars % 2 ==1:
                self.xrange -= 1.8
            else:
                self.xrange -= 1.3
            self.cars += 1
        self.cars -= 1
        print "\t\t�ܷ���%s��1/2��"%self.cars
        self.carrowdistribute,self.peoplerowdistribute = 0.0,0.0

        for i in range(self.cars):
            if i==0:
                self.carrowdistribute += self.func(self.a,self.b,self.widthsideway+0.5)
            elif i==1:
                self.carrowdistribute += self.func(self.a,self.b,self.widthsideway+0.5+1.8)
            elif i==2:
                self.carrowdistribute += self.func(self.a,self.b,self.widthsideway+0.5+1.8+1.3)
        print "\t\t��������ֲ�ϵ����",self.carrowdistribute/2
        print "\t\t��Ⱥ���طֲ�ϵ����",self.func(self.a,self.b,self.widthsideway/2),"\n\t2]:���ؼ���"

        self.f1 = (( 9.81*self.ctable[self.concrete][u'Ec']*100*self.I/(self.conweight*1000) )**0.5)*3.1416/(2*self.l**2)
        # self.f1 = (( 9.81*self.ctable[self.concrete][u'Ec']*100*self.I/(self.conweight*1000) )**0.5)*3.1416/(2*self.l**2)
        print '\t\t��֧������Ƶf1:',self.f1,'Hz'
        if self.f1 >= 1.5 and self.f1<=14:
            print '\t\t���ڻ�Ƶ��1.5��15�䣬�ɡ��Ź桷����=0.1767lnf - 0.0157 '
            self.shock = 1 + 0.1767*math.log(self.f1) - 0.0157

        self.Pk = 180*(1+(self.l-5)/(45))
        self.w = self.l**2/8

        self.Mcarmidlle = self.shock * self.carrowdistribute * (10.5*self.w+self.Pk*self.l/4)
        print "\t\t��·һ�����ؿ�����أ�",self.Mcarmidlle,'KN.m'
        self.Mpeoplemiddle = self.peoplerowdistribute * (3.0*self.widthsideway)*self.w
        print "\t\t��Ⱥ���ؿ�����أ�",self.Mpeoplemiddle,'KN.m'

        print "\n===============================�Ƚ�====================================================="
        print "��������ؿ�����غͣ�",self.Mcarmidlle+self.Mpeoplemiddle+self.Mmiddle,'KN.m'
        print "���������ؿ���:",self.Mu/1000000,'KN.m'
        if (self.Mcarmidlle+self.Mpeoplemiddle+self.Mmiddle)<(self.Mu/1000000):
            print "�����㣬�ܹ�����Ҫ��"
        else:
            print "�����㣬���ϸ�"

        self.showframe.Show()
        self.showframe.Maximize()

    def change(self,bo,up,real):
        result = []
        for i in range(len(bo.items()[0][1])):
            result.append(up.items()[0][1][i]- (up.items()[0][1][i] - bo.items()[0][1][i]) * (up.keys()[0] - real) / ( up.keys()[0] - bo.keys()[0] ))
        return result

    def aboutc(self,column):
        if column<0.1:
            self.c = 1.0/3
        else:
            for i in range(len(self.c12table)):
                if column > self.c12table[i][0] and column < self.c12table[i+1][0]:
                    self.c = self.c12table[i][1] - (self.c12table[i][1]-self.c12table[i+1][1])*(self.column-self.c12table[i][0])/0.1
        return self.c

    def func(self,a,b,x):
        return a*x+b

# app = wx.App()
# frame = wx.Frame(None,-1)
# panel = panel_cal(frame)
# frame.Show()
# frame.Maximize()
# app.MainLoop()