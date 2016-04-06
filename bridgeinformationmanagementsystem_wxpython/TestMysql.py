#coding:gbk
from MySqlUnit import *

sql_search = "select * from bridgeinfo"
result_search = exe_search(sql_search)
print result_search

sql_update = "UPDATE bridgeinfo SET DeclareProgress = '%s' WHERE BridgeName = '%s'" %(u"批准",u"西直门大桥")
exe_update(sql_update)

sql_insert = "INSERT INTO bridgeinfo VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s' )"%(u'鬼魅大桥', u'特殊检查', u'2099', u'糙环', 'B',u'OK',u'否','900',u'没问题',u'批准','121212')
exe_update(sql_insert)