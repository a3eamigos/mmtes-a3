# test_database.py
import unittest
from unittest.mock import patch, MagicMock
from database import adicionar_usuario, check_login, registrar_denuncia, listar_denuncias, verificar_usuario_existente

class TestDatabaseFunctions(unittest.TestCase):

    @patch("database.cursor")
    @patch("database.con")
    def test_adicionar_usuario(self, mock_con, mock_cursor):
        # Simula um cenário onde a função insere o usuário corretamente
        nome = "João Silva"
        cpf = 12345678901
        email = "joao@example.com"
        senha = "senha123"

        adicionar_usuario(nome, cpf, email, senha)
        
        # Verifica se o método de execução e o commit foram chamados
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO User (user_name, user_cpf, user_email, user_password) VALUES (?, ?, ?, ?);",
            (nome, cpf, email, senha)
        )
        mock_con.commit.assert_called_once()

    @patch("database.cursor")
    def test_verificar_usuario_existente(self, mock_cursor):
        # Dados de exemplo
        cpf = 12345678901
        email = "joao@example.com"

        # Simula o cenário onde o usuário já existe
        mock_cursor.fetchone.return_value = (cpf, "João Silva", email, "senha123")
        self.assertTrue(verificar_usuario_existente(cpf, email))
        
        # Verifica se a consulta foi chamada corretamente
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_cpf = ? OR user_email = ?", 
            (cpf, email)
        )

        # Reseta o mock e simula o cenário onde o usuário não existe
        mock_cursor.reset_mock()
        mock_cursor.fetchone.return_value = None
        self.assertFalse(verificar_usuario_existente(cpf, email))
        
        # Verifica novamente se a consulta foi chamada corretamente
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_cpf = ? OR user_email = ?", 
            (cpf, email)
        )

    @patch("database.cursor")
    def test_check_login(self, mock_cursor):
        # Configura o retorno esperado para o cursor.fetchone()
        email = "joao@example.com"
        senha = "senha123"
        mock_cursor.fetchone.return_value = (12345678901, "João Silva", email, senha)

        # Executa a função a ser testada
        result = check_login(email, senha)

        # Verifica se o cursor foi chamado com o SQL correto e se o retorno está conforme esperado
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_email = ? AND user_password = ?", 
            (email, senha)
        )
        self.assertEqual(result, (12345678901, "João Silva", email, senha))

    @patch("database.cursor")
    @patch("database.con")
    def test_registrar_denuncia(self, mock_con, mock_cursor):
        # Dados da denúncia
        user_cpf = 12345678901
        localizacao = "Rua das Flores, 123"
        denuncia_texto = "Buraco na rua"
        foto_path = "C:/Users/Windows/OneDrive/Imagens/Capturas de tela/Captura de tela 2024-05-12 093040.png"

        # Executa a função a ser testada
        registrar_denuncia(user_cpf, localizacao, denuncia_texto, foto_path)

        # Verifica se o cursor foi chamado para executar o SQL
        mock_cursor.execute.assert_called()

        # Recupera todos os argumentos passados para o método 'execute'
        args, _ = mock_cursor.execute.call_args

        # Valida o SQL, ignorando formatação, e verifica os parâmetros
        self.assertIn("INSERT INTO Incident", args[0])
        self.assertEqual(args[1], (user_cpf, localizacao, denuncia_texto, foto_path, unittest.mock.ANY, False))

        # Verifica se o commit foi realizado
        mock_con.commit.assert_called_once()



    @patch("database.cursor")
    def test_listar_denuncias(self, mock_cursor):
        # Simula o retorno esperado para o cursor.fetchall()
        user_cpf = 12345678901
        mock_cursor.fetchall.return_value = [
            ("2024-01-01 12:00:00", "Rua das Flores, 123", "Buraco na rua", False),
            ("2024-01-02 13:30:00", "Av. Central, 456", "Lâmpada queimada", True)
        ]

        # Executa a função a ser testada
        result = listar_denuncias(user_cpf)

        # Verifica se a execução SQL foi chamada e se o retorno está conforme esperado
        mock_cursor.execute.assert_called_once_with(
            '''SELECT incident_data_hora, incident_address, incident_denuncia, incident_resolvido FROM Incident WHERE incident_user_cpf = ?''', 
            (user_cpf,)
        )
        self.assertEqual(result, [
            ("2024-01-01 12:00:00", "Rua das Flores, 123", "Buraco na rua", False),
            ("2024-01-02 13:30:00", "Av. Central, 456", "Lâmpada queimada", True)
        ])

if __name__ == '__main__':
    unittest.main()
