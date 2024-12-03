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
    user_name VARCHAR(100) NOT NULL,  
    user_email VARCHAR(100) NOT NULL, 
    user_password VARCHAR(100) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Incident (
    incident_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    incident_user_cpf INTEGER, 
    incident_address TEXT NOT NULL,
    incident_bairro TEXT NOT NULL,
    incident_denuncia TEXT NOT NULL,
    incident_foto TEXT,
    incident_data_hora TIMESTAMP,
    incident_resolvido BOOLEAN,
    FOREIGN KEY (incident_user_cpf) REFERENCES User(user_cpf) 
)
''')

# Funções CRUD
def adicionar_usuario(nome, cpf, email, senha):
    # Verificar se todos os campos foram preenchidos
    if not all([nome, cpf, email, senha]):
        raise ValueError("Todos os campos são obrigatórios. Nenhum valor pode ser nulo ou vazio.")

    data_user = (nome, cpf, email, senha)
    try:
        cursor.execute("INSERT INTO User (user_name, user_cpf, user_email, user_password) VALUES (?, ?, ?, ?);", data_user)
        con.commit()
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}")
        con.rollback()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        con.rollback()


def verificar_usuario_existente(cpf, email):
    cursor.execute("SELECT * FROM User WHERE user_cpf = ? AND user_email = ?", (cpf, email))
    return cursor.fetchone() is not None

def check_login(email, senha):
    cursor.execute("SELECT * FROM User WHERE user_email = ? AND user_password = ?", (email, senha))
    return cursor.fetchone()

def registrar_denuncia(user_cpf, localizacao, bairro, denuncia_texto, foto_path=None):
    if not all([localizacao, bairro, denuncia_texto]):
        raise ValueError("Todos os campos são obrigatórios. Nenhum valor pode ser nulo ou vazio.")
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

def obter_todos_enderecos():
    cursor.execute("SELECT incident_address FROM Incident WHERE incident_resolvido = 0")
    return [row[0] for row in cursor.fetchall()]

# Fecha a conexão ao encerrar
def fechar_conexao():
    con.close()