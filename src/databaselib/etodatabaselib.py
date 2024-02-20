import pymysql
import cryptography
from databaselib.helper import getDictionaryRow, getFirstDictionaryRow

class Database():

    def __init__(self, host:str, user:str, password:str, db:str):

        self.host = host
        self.user = user
        self.password = password
        self.db = db

database:Database = None

def connect():
    # Here you insert the credentials for your database
    return pymysql.connect(
            host=f'{database.host}',
            user=f'{database.user}',
            password=f'{database.password}',
            db=f'{database.db}',
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor
    )

conn = connect()

def reconnect():
    global conn
    if not conn.open:
        conn = connect()

def close_connection():
    if conn.open:
        conn.close()

def createTable(title:str, args:dict, useSafeCreate:bool = None):
    reconnect()
    try:
        with conn.cursor() as cursor:
            # Create a new record
            
            first_row:tuple = getFirstDictionaryRow(args)
            
            createModeSqlQuerry = "IF NOT EXISTS" if useSafeCreate else ""

            sql = f"CREATE TABLE {createModeSqlQuerry} {title} ( {first_row[0]} {first_row[1]}"
            #print(sql) 
            #cursor.execute(sql)
            
            for i in range(args.__len__()):
                row = getDictionaryRow(args, i + 1)
                if row == getFirstDictionaryRow(args):
                    continue    
                sql += ", "
                sql += f"{row[0]} {row[1]}"
            sql += " )"
            #print(sql)
            cursor.execute(sql)

        # Commit changes
        conn.commit()

        #print("Record inserted successfully")
    except pymysql.err.OperationalError:
        close_connection()
        #print('Editing the column instead')
        editColumn(title, args)
    finally:
        close_connection()

def addColumn(table:str, args:dict):
    reconnect()
    try:
        with conn.cursor() as cursor:
            # Create a new record
            sql = f"ALTER TABLE {table} "
            
            for i in range(args.__len__()):
                row = getDictionaryRow(args, i + 1)
                sql += f"ADD {row[0]} {row[1]}"
                if not row == getDictionaryRow(args, args.__len__()):
                    sql += ", "
            #print(sql)
            cursor.execute(sql)
            
            
        # Commit changes
        conn.commit()

        #print("Record inserted successfully")
    except pymysql.err.OperationalError:
        close_connection()
        #print('rawr')
        editColumn(table, args)
    finally:
        close_connection()
    
def editColumn(table:str, args:dict):
    reconnect()
    try:
        with conn.cursor() as cursor:
            # Create a new record
            sql = f"ALTER TABLE {table} "
            
            row = getFirstDictionaryRow(args)
            sql += f"MODIFY {row[0]} {row[1]}"
            #print(sql)
            cursor.execute(sql) 
    
        # Commit changes
        conn.commit()

        #print("Record inserted successfully")
    finally:
        close_connection()

def get_rows(table:str, columns:list, condition:str = None):
    reconnect()
    return_rows = None
    try:
        with conn.cursor() as cursor:

            sql = f"SELECT "
            ###print(sql)

            for column in columns:
                sql += f"{column}"
                if not column == columns[columns.__len__() - 1]:
                    sql += f", "
            
            conditionStr = f"WHERE {condition}" if condition != None else ""

            sql += f" from {table} {conditionStr}"
            ##print(sql)

            cursor.execute(sql)

            rows = cursor.fetchall()
            return_rows = rows
            ###print(rows)

            ###print("*" * 50)

            """ for row in rows:
                ##print(row) """
        
            
    finally:
        close_connection()
        ###print(f"meow {return_rows}")
        if return_rows == ():
            return_rows = None
        return return_rows

# BE AWARE THAT USING THE DONT_REPEAT TUPLE FOR SMART INSERTS WILL DECREASE THE PERFORMANCE SINCE FOR EACH ELEMENT IN THE DONT_REPEAT TUPLE IT WILL EXECUTE 1 SELECT QUERY

def insert_rows(table: str, args:dict, dont_repeat:list = None):

    reconnect()
    try:
        with conn.cursor() as cursor:

            if not dont_repeat == None: 
            
                conditionList = ""

                for item in dont_repeat:
                    if item in args:
                        itemValue = args.get(item)
                        if type(itemValue) == str:
                            conditionList += f"{item} = '{args.get(item)}'"
                        else:
                            conditionList += f"{item} = {args.get(item)}"
                        if not item == dont_repeat[-1]:
                            conditionList += " OR "
                ##print(f"{conditionList}")

                test = get_rows(table, ["*"], conditionList)
                ##print(f's\n{test}')
                reconnect()
                cursor = conn.cursor()
                ##print(test)
            
                if not test == None:
                    readable_condition_list = ""
                    for condition in dont_repeat:
                        readable_condition_list += f"{condition} or "
                    raise ValueError(f'repeated {readable_condition_list}')

                """ for item in dont_repeat:
                    if item in args:
                        args.__delitem__(item) """

            sql = f"INSERT INTO {table} ( "
            ##print(sql)

            for i in range(args.__len__()):
                column = getDictionaryRow(args, i + 1)
                columnName = column[0]
                sql += f"{columnName}"
                if not column == getDictionaryRow(args, args.__len__()):
                    sql += f", "
            sql += " ) VALUES ( "

            for i in range(args.__len__()):
                column = getDictionaryRow(args, i + 1)
                columnValue = column[1]
                if type(columnValue) == str:
                    sql += f"'{columnValue}'"
                else:
                    sql += f"{columnValue}"
                if not column == getDictionaryRow(args, args.__len__()):
                    sql += f", "
            sql += " )"
            
            #conditionStr = f"WHERE {condition}" if condition != None else ""

            #sql += f" {conditionStr}"
            ##print(sql)

            cursor.execute(sql)

        conn.commit()

        #print('Rows inserted!')
    except ValueError as e:
        print(e)
    finally:
        close_connection()

def edit_rows(table: str, args:dict, condition:str, dont_repeat:list = None) -> bool:
    reconnect()
    try:
        with conn.cursor() as cursor:

            if not dont_repeat == None: 
            
                conditionList = ""

                for item in dont_repeat:
                    if item in args:
                        itemValue = args.get(item)
                        if type(itemValue) == str:
                            conditionList += f"{item} = '{args.get(item)}'"
                        else:
                            conditionList += f"{item} = {args.get(item)}"
                        if not item == dont_repeat[-1]:
                            conditionList += " OR "
                        

                test = get_rows(table, ["*"], conditionList)
                reconnect()
                cursor = conn.cursor()
                #print(test)
            
                if not test == None:
                    readable_condition_list = ""
                    for condition in dont_repeat:
                        readable_condition_list += f"{condition} or "
                    raise ValueError(f'repeated {readable_condition_list}')

                """ for item in dont_repeat:
                    if item in args:
                        args.__delitem__(item) """

            sql = f"UPDATE {table}\nSET "
            #print(sql)
                

            for i in range(args.__len__()):
                column = getDictionaryRow(args, i + 1)
                columnName = column[0]
                columnValue = column[1]
                sql += f"{columnName} = "
                if type(columnValue) == str:
                    sql += f"'{columnValue}'"
                else:
                    sql += f"{columnValue}"
                if not column == getDictionaryRow(args, args.__len__()):
                    sql += f", "
            
            conditionStr = f"WHERE {condition}" if condition != None else ""

            sql += f"\n{conditionStr}"

            #print(sql)

            cursor.execute(sql)

        conn.commit()

        #print('Rows edited!')
    except ValueError as e:
        print(e)
        return False
    finally:
        close_connection()
        return True