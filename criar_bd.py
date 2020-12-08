import database.database_commands as dbc
import sqlite3

try: #Database user_database.bd already exists.
    dbc.connect_to_user_database()
    print('Banco de dados ja existente.')
except sqlite3.OperationalError: #Database user_database.bd does not exist. It will be created.
    dbc.create_user_database()
    dbc.create_tables()
    print('Banco de dados criado.')
