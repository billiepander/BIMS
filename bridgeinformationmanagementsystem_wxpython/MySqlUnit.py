#coding:gbk
"""
    ���ݿ�search��update��װ����
"""
import MySQLdb
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
            result = func(conn,cursor,sql)
            cursor.close()
            conn.close()
            return result
        return infunc
    return ifunc

#��ѯ����
@conclos(host='127.0.0.1',port = 3306,user = 'root',passwd = 'punkisdead',db = 'bims',charset = 'utf8',)
def exe_search(conn,cursor,sql):
    cursor.execute(sql)
    outcatch = cursor.fetchall()
    conn.commit()
    return outcatch

#�������ɾ������
@conclos(host='127.0.0.1',port = 3306,user = 'root',passwd = 'punkisdead',db = 'bims',charset = 'utf8',)
def exe_update(conn,cursor,sql):
    try:
       cursor.execute(sql)
       conn.commit()
    except:
       conn.rollback()



















