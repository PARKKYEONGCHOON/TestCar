
import pymysql


class Mysql:
    
    def __init__(self):
        
        self.host = 'localhost'
        self.port = 3306
        self.database = 'test_db'
        self.username = 'root'
        self.password = '940302'
        self.conn = None
        self.cursor = None
    
    def MySQL_Connect(self):
        
        #DB Connection 생성
        self.conn = pymysql.connect(user=self.username, passwd=self.password, host=self.host, db=self.database, charset='utf8')
        self.cursor = self.conn.cursor()

        if self.conn.open:
            print("db open complete")    
        
    
    def MySQL_DisConnect(self):
        
        self.conn.close()
    
    def MySQL_SelectAll(self,table):
        
        sql = "SELECT * FROM " + table
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)
        
    def MySQL_INSERT(self,table,col,data):
        
        #sql = """insert into detectdata(DATE,RESULT) values ('2022-03-15', 'OK')"""
        sql = "INSERT INTO "+ table + " ("+ col + ") " + "VALUES (%s)"
        self.cursor.execute(sql,data)
        self.conn.commit()
        
    def MySQL_INSERT2(self,table,col1,col2,data1,data2):
        
        #sql = """insert into detectdata(DATE,RESULT) values ('2022-03-15', 'OK')"""
        sql = "INSERT INTO "+ table + " ("+ col1 + "," + col2 +") " + "VALUES (%s,%s)"
        
        data = (data1,data2)
        self.cursor.execute(sql,data)  
        self.conn.commit()
    
    def MySQL_DELETE(self,table,con):
        
        sql = "DELETE FROM "+ table + " WHERE " + con
        self.cursor.execute(sql)
        self.conn.commit()
    
    def MySQL_UPDATE(self,table,col,data,condition):
        
        #sql = "UPDATE detectdata SET RESULT = %s WHERE NO = 2"
        sql = "UPDATE "+ table + " SET " + col + "= %s WHERE " + condition
        self.cursor.execute(sql,data)
        self.conn.commit()

#if __name__ == "__main__":
    #sql = Mysql()
    
    #sql.MySQL_Connect()
    
    #t = 'detectdata'
    #c = 'RESULT'
    #d = "OK"
    #con = "NO = 5"
    
    #sql.MySQL_SelectAll(t)
    
    #sql.MySQL_DELETE(t,con)
    #sql.MySQL_UPDATE(t,c,d,con)
    #sql.MySQL_INSERT(t,c,d)
    
    