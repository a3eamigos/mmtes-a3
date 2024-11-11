import unittest
from unittest.mock import patch, MagicMock
from database import (adicionar_usuario, check_login, registrar_denuncia, listar_denuncias, 
                      listar_denuncias_por_bairro, listar_todas_denuncias, 
                      atualizar_status_denuncia, obter_todos_enderecos, verificar_usuario_existente)

class TestDatabaseFunctions(unittest.TestCase):

    @patch("database.cursor")
    @patch("database.con")
    def test_adicionar_usuario(self, mock_con, mock_cursor):
        nome = "João Silva"
        cpf = 12345678901
        email = "joao@example.com"
        senha = "senha123"

        adicionar_usuario(nome, cpf, email, senha)
        
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO User (user_name, user_cpf, user_email, user_password) VALUES (?, ?, ?, ?);",
            (nome, cpf, email, senha)
        )
        mock_con.commit.assert_called_once()

    @patch("database.cursor")
    def test_verificar_usuario_existente(self, mock_cursor):
        cpf = 12345678901
        email = "joao@example.com"

        mock_cursor.fetchone.return_value = (cpf, "João Silva", email, "senha123")
        self.assertTrue(verificar_usuario_existente(cpf, email))
        
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_cpf = ? OR user_email = ?", 
            (cpf, email)
        )

        mock_cursor.reset_mock()
        mock_cursor.fetchone.return_value = None
        self.assertFalse(verificar_usuario_existente(cpf, email))
        
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_cpf = ? OR user_email = ?", 
            (cpf, email)
        )

    @patch("database.cursor")
    def test_check_login(self, mock_cursor):
        email = "joao@example.com"
        senha = "senha123"
        mock_cursor.fetchone.return_value = (12345678901, "João Silva", email, senha)

        result = check_login(email, senha)

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_email = ? AND user_password = ?", 
            (email, senha)
        )
        self.assertEqual(result, (12345678901, "João Silva", email, senha))

    @patch("database.cursor")
    @patch("database.con")
    def test_registrar_denuncia(self, mock_con, mock_cursor):
        user_cpf = 12345678901
        localizacao = "Rua das Flores, 123"
        bairro = "Centro"
        denuncia_texto = "Buraco na rua"
        foto_path = "path/to/image.png"

        registrar_denuncia(user_cpf, localizacao, bairro, denuncia_texto, foto_path)

        mock_cursor.execute.assert_called()
        args, _ = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO Incident", args[0])
        self.assertEqual(args[1], (user_cpf, localizacao, bairro, denuncia_texto, foto_path, unittest.mock.ANY, False))

        mock_con.commit.assert_called_once()

    @patch("database.cursor")
    def test_listar_denuncias(self, mock_cursor):
        user_cpf = 12345678901
        mock_cursor.fetchall.return_value = [
            ("2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False),
            ("2024-01-02 13:30:00", "Av. Central, 456", "Centro", "Lâmpada queimada", True)
        ]

        result = listar_denuncias(user_cpf)

        mock_cursor.execute.assert_called_once_with(
            '''SELECT incident_data_hora, incident_address, incident_bairro, incident_denuncia, incident_resolvido FROM Incident WHERE incident_user_cpf = ?''', 
            (user_cpf,)
        )
        self.assertEqual(result, [
            ("2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False),
            ("2024-01-02 13:30:00", "Av. Central, 456", "Centro", "Lâmpada queimada", True)
        ])

    @patch("database.cursor")
    def test_listar_denuncias_por_bairro(self, mock_cursor):
        # Dados de entrada
        user_cpf = 12345678901
        bairro = "Centro"

        # Configura o retorno esperado para o cursor.fetchall()
        mock_cursor.fetchall.return_value = [
            ("2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False),
            ("2024-01-02 13:30:00", "Av. Central, 456", "Centro", "Lâmpada queimada", True)
        ]

        # Executa a função a ser testada
        result = listar_denuncias_por_bairro(user_cpf, bairro)

        # Recupera o SQL executado e remove espaços extras e quebras de linha para comparação
        execute_call_args = "".join(mock_cursor.execute.call_args[0][0].split())
        expected_sql = "SELECT incident_data_hora, incident_address, incident_bairro, incident_denuncia, incident_resolvido FROM Incident WHERE incident_user_cpf = ? AND incident_bairro = ?"
        expected_sql = "".join(expected_sql.split())

        # Verifica se o SQL essencial está contido na chamada
        self.assertIn(expected_sql, execute_call_args)
        self.assertEqual(result, [
            ("2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False),
            ("2024-01-02 13:30:00", "Av. Central, 456", "Centro", "Lâmpada queimada", True)
        ])

    @patch("database.cursor")
    def test_listar_todas_denuncias(self, mock_cursor):
        mock_cursor.fetchall.return_value = [
            (1, "2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False)
        ]

        result = listar_todas_denuncias()

        mock_cursor.execute.assert_called_once_with(
            "SELECT incident_id, incident_data_hora, incident_address, incident_bairro, incident_denuncia, incident_resolvido FROM Incident"
        )
        self.assertEqual(result, [
            (1, "2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False)
        ])

    @patch("database.cursor")
    @patch("database.con")
    def test_atualizar_status_denuncia(self, mock_con, mock_cursor):
        incident_id = 1
        novo_status = True

        atualizar_status_denuncia(incident_id, novo_status)

        mock_cursor.execute.assert_called_once_with(
            "UPDATE Incident SET incident_resolvido = ? WHERE incident_id = ?", 
            (novo_status, incident_id)
        )
        mock_con.commit.assert_called_once()

    @patch("database.cursor")
    def test_obter_todos_enderecos(self, mock_cursor):
        mock_cursor.fetchall.return_value = [("Rua das Flores, 123",), ("Av. Central, 456",)]

        result = obter_todos_enderecos()

        mock_cursor.execute.assert_called_once_with("SELECT incident_address FROM Incident WHERE incident_resolvido = 0")
        self.assertEqual(result, ["Rua das Flores, 123", "Av. Central, 456"])

if __name__ == '__main__':
    unittest.main()
