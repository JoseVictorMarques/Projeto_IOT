import sqlite3
import datetime as dt
import re
import shutil
import os
from .reconhecimento import reconhecimento as rec

DATABASE_PATH = 'database/local_database.db' #localmente
#Database functions:
def connect_to_user_database():
     con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
     con.close()

def create_user_database():
     con = sqlite3.connect(DATABASE_PATH)
     con.close()

def create_tables():
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    with open('database/database_schema.sql') as f:
        script = f.read()
        cur = con.cursor()
        cur.executescript(script)
    con.close()


#Criar cliente:
def create_cliente(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO cliente(nome, telefone, nascimento, password) VALUES (?, ?, ?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()


def get_cliente():
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    cur = con.cursor()
    cur.execute('''
    SELECT * FROM cliente 
    ''')
    result = cur.fetchall()
    con.close()
    return result

def edit_cliente(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        UPDATE cliente SET name = ?, nascimento = ?
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()


#Create localizacao:
def create_pais(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO pais(nome) VALUES (?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

def create_regiao(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO regiao(id_pais, nome) VALUES (?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()



def create_cidade(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO cidade(id_regiao, nome) VALUES (?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

#Create construcao:
def create_construcao(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO construcao(id_cidade, id_cliente, nome, altura_maxima, altura_minima, bairro, cep) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

#Create inspecao:
def create_inspecao(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO inspecao(id_construcao, data_inicio) VALUES (?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

def finish_inspecao(id_inspecao):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        date = datetime.now().isoformat(' ')
        cur = con.cursor()
        cur.execute('''
        UPDATE inspecao SET data_fim = ? WHERE id_inspecao = ? 
        ''', (date, id_inspecao))
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

#Adicionar fotos a uma inspecao:
def cadastrar_imagem(id_inspecao, original_picture_path, default_path='database/imagens_inspecao'):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO imagens_inspecao(id_inspecao, nome, endereco) VALUES (?, ?, ?)
        ''', (id_inspecao, 'default_name', ''))
        con.commit()
        cur.execute('''
        SELECT last_insert_rowid();
        ''')
        id_imagens_inspecao = cur.fetchall()[0][0]
        picture_name = 'imagem_{}_inspecao_{}.png'.format(id_imagens_inspecao, id_inspecao)
        picture_path = default_path + '/' + picture_name
        cur.execute('''
        UPDATE imagens_inspecao SET nome = ?, endereco = ? WHERE id_imagens_inspecao = ? 
        ''', (picture_name, picture_path, id_imagens_inspecao))
        con.commit()
        try:
            #Mover a imagem para o novo diretorio:
            os.rename(original_picture_path, picture_path)
        except:
            print("Operation failed.")
            con.rollback()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()



def cadastrar_imagens_diretorio(id_inspecao, folder_path, default_path='database/imagens_inspecao'):
    lista_enderecos = os.listdir(path=folder_path)
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    for filename in lista_enderecos:
        original_picture_path = folder_path + '/' + filename
        try:
            cur = con.cursor()
            cur.execute('''
            INSERT INTO imagens_inspecao(id_inspecao, nome, endereco) VALUES (?, ?, ?)
            ''', (id_inspecao, 'default_name', ''))
            con.commit()
            cur.execute('''
            SELECT last_insert_rowid();
            ''')
            id_imagens_inspecao = cur.fetchall()[0][0]
            picture_name = 'imagem_{}_inspecao_{}.png'.format(id_imagens_inspecao, id_inspecao)
            picture_path = default_path + '/' + picture_name
            cur.execute('''
            UPDATE imagens_inspecao SET nome = ?, endereco = ? WHERE id_imagens_inspecao = ? 
            ''', (picture_name, picture_path, id_imagens_inspecao))
            con.commit()
            try:
                #Mover a imagem para o novo diretorio:
                os.rename(original_picture_path, picture_path)
            except:
                print("Operation failed.")
                con.rollback()
        except:
            print("Operation failed.")
            con.rollback()
    con.close()
    avaliar_imagens(id_inspecao)

def avaliar_imagens(id_inspecao):
    imagens_lista = retornar_imagens(id_inspecao)
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    for picture_path, label in imagens_lista:
        if label is None:
            #Avaliar imagem
            new_label = rec.classify_image(picture_path)['status']
            print("Avaliando imagem")
            try:
                cur = con.cursor()
                cur.execute('''
                UPDATE imagens_inspecao SET label = ? WHERE endereco = ?, id_inspecao = ? 
                ''', (new_label, picture_path, id_inspecao))
                con.commit()
            except:
                print("Operation failed.")
                con.rollback()
        else:
            continue
    con.close()


def retornar_imagens(id_inspecao):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    cur = con.cursor()
    cur.execute('''
    SELECT endereco, label FROM imagens_inspecao WHERE id_inspecao = ? 
    ''', (id_inspecao,))
    result = cur.fetchall()
    con.close()
    return result


def classificar_imagens_inspecao(id_imagens_inspecao, label):
    #label --> 'QUEBRADO' ou 'NAO-QUEBRADO'
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        UPDATE imagens_inspecao SET label = ? WHERE id_imagens_inspecao = ? 
        ''', (label, id_imagens_inspecao))
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

#Cadastrar drone:
def create_marca(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO marca(nome) VALUES (?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()


def create_modelo(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO modelo (id_marca, nome, altura_maxima, autonomia_voo, distancia_controle) VALUES (?, ?, ?, ?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()



def create_drone(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO drone(id_modelo, nome, data_aquisicao, custo_compra) VALUES (?, ?, ?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()


#Adicionar foto para treinamento:
def create_imagens_treinamento(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO imagens_treinamento(nome, endereco, label) VALUES (?, ?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

#Cadastrar usuario:

######################################################################################################################################################


#Modify Tasks:
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_tasks():
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('''
    SELECT task_id, creation_date, difficulty, description, name, importance, total_hours, deadline, daily_hours FROM task WHERE is_finished = 0
    ''')
    result = cur.fetchall()
    con.close()
    return result


def add_book(task_value, book_value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO task (name, description, deadline, 
        importance, daily_hours, frequency) VALUES (?, ?, ?, ?, ?, ?)
        ''', task_value)
        con.commit()
        cur.execute('''
        SELECT last_insert_rowid();
        ''')
        task_id = cur.fetchall()
        cur.execute('''
        INSERT INTO task_book (task_id, book_name, publisher, total_pages, edition, volume, author) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', task_id[0] + book_value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()


