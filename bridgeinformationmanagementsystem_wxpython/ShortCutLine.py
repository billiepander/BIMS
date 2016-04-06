#coding:gbk
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np
font = FontProperties(fname=r"c:\windows\Fonts\simsun.ttc",size=11)
import MySqlUnit

def genLinePic():
    search_name = "select BridgeName from bridgeinfo GROUP BY BridgeName"
    names = MySqlUnit.exe_search(search_name)
    for i in names:
        for j in i:
            search = "select BridgeName,QualityLevel,DetectTime from bridgeinfo WHERE BridgeName='%s' ORDER BY DetectTime"%j
            result = MySqlUnit.exe_search(search)

            changeBridge={u'A':4,u"B":3,u'C':2,u'D':1}
            x = []
            y = []
            for i in range(len(result)):
                y.append(changeBridge[result[i][1]])
                x.append(i)

            print x,y
            if len(x)>2:
                plt.figure(1, figsize=(len(x)*1.5,4.7))
            else:
                plt.figure(1, figsize=(4.7,4.7))
            plt.plot(x,y,"k-",label="range",color="red")
            plt.scatter(x,y,color="red")
            plt.grid()      #打开网格
            plt.title(result[0][0],size=16,fontproperties=font)
            plt.axis([0,len(x)+1,0,6])
            plt.xticks( np.arange(len(x)), [z[2] for z in result ] )
            plt.yticks( np.arange(5), ('0','D', 'C', 'B', 'A') )
            print abs(hash(j))
            plt.savefig(".//templates//%s.png"%abs(hash(j)))
            plt.close()
