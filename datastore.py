import sqlite3

class file_db:
    def __init__(self, db_name):
        self.db_name = db_name
        
    def execute_query_w(self , query , params=None):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query , params)
            conn.commit()
            conn.close
            return True
        except:
            #log
            return False
    

    def execute_query_r(self , query , params = None):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall()
            cursor.close()
            return data
        except:
            #log
            return None
    
        