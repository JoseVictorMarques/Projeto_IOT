import database.database_commands as dbc
import sqlite3

input_ = {'endereco_diretorio':'imagens_input', 'id_inspecao':1}
dbc.cadastrar_imagens_diretorio(input_['id_inspecao'], input_['endereco_diretorio'])
print('Imagens da inspecao {}: '.format(input_['id_inspecao']), dbc.retornar_imagens(input_['id_inspecao']))
