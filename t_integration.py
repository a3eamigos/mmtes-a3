import unittest
import sqlite3
from database import adicionar_usuario, registrar_denuncia, listar_denuncias

class TestDatabaseIntegration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Configura um banco de dados de teste em memória
        cls.con = sqlite3.connect("DBRP.sqlite")  # Usando o banco original
        cls.cursor = cls.con.cursor()

        # Criação das tabelas para o teste de integração
        cls.cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            user_cpf INTEGER PRIMARY KEY, 
            user_name VARCHAR(100),  
            user_email VARCHAR(100), 
            user_password VARCHAR(100)
        )
        ''')
        cls.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Incident (
            incident_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            incident_user_cpf INTEGER, 
            incident_address TEXT,
            incident_bairro TEXT,
            incident_denuncia TEXT,
            incident_foto TEXT,
            incident_data_hora TIMESTAMP,
            incident_resolvido BOOLEAN,
            FOREIGN KEY (incident_user_cpf) REFERENCES User(user_cpf) 
        )
        ''')

    @classmethod
    def tearDownClass(cls):
        # Fecha a conexão ao banco de dados de teste
        cls.con.close()

    def setUp(self):
        # Limpa as tabelas antes de cada teste
        self.cursor.execute("DELETE FROM User")
        self.cursor.execute("DELETE FROM Incident")
        self.con.commit()

    def test_user_creation_and_report_flow(self):
        # Testa o fluxo completo: adicionar usuário, registrar denúncia e listar denúncias
        
        # Adiciona um usuário
        nome = "João Silva"
        cpf = 12345678901
        email = "joao@example.com"
        senha = "senha123"
        
        # Verifica se o usuário já existe antes de inserir
        if not self.user_exists(cpf):
            adicionar_usuario(nome, cpf, email, senha)

        # Registra uma denúncia para o usuário
        localizacao = "Rua das Flores, 123"
        bairro = "Centro"
        denuncia_texto = "Buraco na rua"
        foto_path = None  # Sem foto no teste
        registrar_denuncia(cpf, localizacao, bairro, denuncia_texto, foto_path)

        # Lista as denúncias do usuário
        denuncias = listar_denuncias(cpf)
        
        # Verifica se a denúncia foi registrada corretamente
        self.assertEqual(len(denuncias), 1)
        self.assertEqual(denuncias[0][1], localizacao)
        self.assertEqual(denuncias[0][2], bairro)
        self.assertEqual(denuncias[0][3], denuncia_texto)
        self.assertFalse(denuncias[0][4])  # Verifica que a denúncia ainda não foi resolvida

    def user_exists(self, cpf):
        # Verifica se o usuário já existe no banco de dados
        self.cursor.execute("SELECT 1 FROM User WHERE user_cpf = ?", (cpf,))
        return self.cursor.fetchone() is not None

if __name__ == "__main__":
    unittest.main()
