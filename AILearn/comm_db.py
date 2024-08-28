import sqlite3


class communication_db():
    def __init__(self):
        self.connection = sqlite3.connect('world_data.db')
    
    def update_data(self,table,head_title,insert_data,country_full_name):
        print("table:", table)
        print("column:", head_title)
        print("Insert:",insert_data)
        print("country_full_name:",country_full_name)
        cursor = self.connection.cursor()
      
        db = """UPDATE {} SET '{}' = '{}' WHERE Country= '{}' """.format(table,head_title,insert_data,country_full_name)
    
        cursor.execute(db)
        self.connection.commit()
        cursor.close()

        

    def read_table(self,table):
        cursor = self.connection.cursor()

        bd = """SELECT * FROM  {}""".format(table)
        cursor.execute(bd)
        title = [cn[0] for cn in cursor.description]
        register = cursor.fetchall()
        num_rows=len(register)
        num_columns =len(register[0])
        self.connection.commit()
        cursor.close()
        return (register,title,num_rows,num_columns)
    




    def search_country(self,table,country_name):
        cursor = self.connection.cursor()

        bd = "SELECT * FROM {} WHERE Country LIKE {} ".format(table,country_name)

        cursor.execute(bd)
        title = [cn[0] for cn in cursor.description]
        register = cursor.fetchall()
        num_rows=len(register)
        num_columns =len(register[0])
        self.connection.commit()
        cursor.close()
        return (register,title,num_rows,num_columns)
        

    def delete_data(self, table,country_name):
        cursor = self.connection.cursor() 
        bd = """DELETE FROM {} WHERE Country= '{}' """.format(table,country_name)
        cursor.execute(bd)
        self.connection.commit()
        cursor.close()

    def select_xy(self,Item):
        cursor = self.connection.cursor()
        bd = "SELECT * FROM ecuador WHERE IndicatorName = {} ".format(Item)
        cursor.execute(bd)
        title = [cn[0] for cn in cursor.description]
        register = cursor.fetchall()
        num_rows=len(register)
        num_columns =len(register[0])
        self.connection.commit()
        cursor.close()
        return (register,title,num_rows,num_columns) 










