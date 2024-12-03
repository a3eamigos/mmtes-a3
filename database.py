# database.py
import sqlite3
from pathlib import Path
from datetime import datetime

# Caminho para o diretório do arquivo atual
ROOT_PATH = Path(__file__).parent
con = sqlite3.connect(ROOT_PATH / 'DBRP.sqlite')
cursor = con.cursor()

# Criação das tabelas, se ainda não existirem
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    user_cpf INTEGER PRIMARY KEY, 
    user_name VARCHAR(100),  
    user_email VARCHAR(100), 
    user_password VARCHAR(100)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Incident (
    incident_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    incident_user_cpf INTEGER, 
    incident_address TEXT,
    incident_bairro TEXT,
    incident_denuncia TEXT,
    incident_coords_lat TEXT,
    incident_coords_long TEXT,
    incident_foto TEXT,
    incident_data_hora TIMESTAMP,
    incident_resolvido BOOLEAN,
    FOREIGN KEY (incident_user_cpf) REFERENCES User(user_cpf) 
)
''')

# Funções CRUD
def adicionar_usuario(nome, cpf, email, senha):
    data_user = (nome, cpf, email, senha)
    try:
        cursor.execute("INSERT INTO User (user_name, user_cpf, user_email, user_password) VALUES (?, ?, ?, ?);", data_user)
        con.commit()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        con.rollback()

def verificar_usuario_existente(cpf, email):
    cursor.execute("SELECT * FROM User WHERE user_cpf = ? OR user_email = ?", (cpf, email))
    return cursor.fetchone() is not None

def check_login(email, senha):
    cursor.execute("SELECT * FROM User WHERE user_email = ? AND user_password = ?", (email, senha))
    return cursor.fetchone()

def registrar_denuncia(user_cpf, localizacao, bairro, denuncia_texto, foto_path=None):
    data_denuncia = (user_cpf, localizacao, bairro, denuncia_texto, foto_path, datetime.now(), False)
    cursor.execute('''
        INSERT INTO Incident (incident_user_cpf, incident_address, incident_bairro, incident_denuncia, incident_foto, incident_data_hora, incident_resolvido) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data_denuncia)
    con.commit()

def listar_denuncias(user_id):
    cursor.execute('''SELECT incident_data_hora, incident_address, incident_bairro, incident_denuncia, incident_resolvido FROM Incident WHERE incident_user_cpf = ?''', (user_id,))
    return cursor.fetchall()

def listar_denuncias_por_bairro(user_id, bairro):
    cursor.execute('''
        SELECT incident_data_hora, incident_address, incident_bairro, incident_denuncia, incident_resolvido 
        FROM Incident 
        WHERE incident_user_cpf = ? AND incident_bairro = ?
    ''', (user_id, bairro))
    return cursor.fetchall()

def listar_todas_denuncias():
    cursor.execute("SELECT incident_id, incident_data_hora, incident_address, incident_bairro, incident_denuncia, incident_resolvido FROM Incident")
    return cursor.fetchall()

def atualizar_status_denuncia(incident_id, novo_status):
    cursor.execute("UPDATE Incident SET incident_resolvido = ? WHERE incident_id = ?", (novo_status, incident_id))
    con.commit()

# Fecha a conexão ao encerrar
def fechar_conexao():
    con.close()
