import pymysql

def conexion():
    return pymysql.connect(host='localhost',
                            user='root',
                            password='1',
                            db='database')