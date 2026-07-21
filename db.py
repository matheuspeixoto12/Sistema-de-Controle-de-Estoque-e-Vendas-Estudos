import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='graal'
        )
        return con
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None
