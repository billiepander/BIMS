#coding:gbk
from MySqlUnit import *

sql_search = "select * from bridgeinfo"
result_search = exe_search(sql_search)
print result_search

sql_update = "UPDATE bridgeinfo SET DeclareProgress = '%s' WHERE BridgeName = '%s'" %(u"��׼",u"��ֱ�Ŵ���")
exe_update(sql_update)

sql_insert = "INSERT INTO bridgeinfo VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s' )"%(u'���ȴ���', u'������', u'2099', u'�ڻ�', 'B',u'OK',u'��','900',u'û����',u'��׼','121212')
exe_update(sql_insert)