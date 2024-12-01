import unittest
from unittest.mock import patch
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

        # Caso positivo: todos os dados estão corretos
        result = adicionar_usuario(nome, cpf, email, senha)

        # Validação do retorno
        self.assertTrue(result, "Esperava-se True no caso positivo, indicando sucesso na operação.")
        self.assertIsInstance(result, bool, "O retorno deve ser do tipo bool no caso positivo.")

        # Validar se o comando SQL foi chamado corretamente
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO User (user_name, user_cpf, user_email, user_password) VALUES (?, ?, ?, ?);",
            (nome, cpf, email, senha)
        )
        mock_con.commit.assert_called_once()

        # Resetar mocks para o próximo caso
        mock_cursor.reset_mock()
        mock_con.reset_mock()

        # Caso negativo: nome está vazio
        result = adicionar_usuario("", cpf, email, senha)

        # Validação do retorno
        self.assertFalse(result, "Esperava-se False no caso negativo, indicando falha na operação.")
        self.assertIsInstance(result, bool, "O retorno deve ser do tipo bool no caso negativo.")

        # Certificar-se de que nenhuma operação foi executada
        mock_cursor.execute.assert_not_called()
        mock_con.commit.assert_not_called()

    @patch("database.cursor")
    def test_verificar_usuario_existente(self, mock_cursor):
        cpf = 12345678901
        email = "joao@example.com"

        # Caso positivo: usuário encontrado
        mock_cursor.fetchone.return_value = (cpf, "João Silva", email, "senha123")
        result = verificar_usuario_existente(cpf, email)

        # Validação do retorno esperado
        self.assertTrue(result, "Esperava-se True para um usuário existente, mas foi retornado False.")

        # Validação do tipo do retorno
        self.assertIsInstance(result, bool, "O retorno da função deve ser do tipo bool.")
        
        # Validação da consulta SQL
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_cpf = ? AND user_email = ?", 
            (cpf, email)
        )

        # Resetar mocks para o próximo caso
        mock_cursor.reset_mock()

        # Caso negativo: usuário não encontrado
        mock_cursor.fetchone.return_value = None
        result = verificar_usuario_existente(cpf, email)

        # Validação do retorno esperado
        self.assertFalse(result, "Esperava-se False para um usuário inexistente, mas foi retornado True.")

        # Validação do tipo do retorno
        self.assertIsInstance(result, bool, "O retorno da função deve ser do tipo bool.")
        
        # Validação da consulta SQL
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_cpf = ? AND user_email = ?", 
            (cpf, email)
        )

    @patch("database.cursor")
    def test_check_login(self, mock_cursor):
        email = "joao@example.com"
        senha = "senha123"
        expected_result = (12345678901, "João Silva", email, senha)

        # Caso positivo: usuário encontrado
        mock_cursor.fetchone.return_value = expected_result
        result = check_login(email, senha)

        # Validação do comando SQL
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_email = ? AND user_password = ?",
            (email, senha)
        )

        # Validação do retorno no caso positivo
        self.assertEqual(result, expected_result, "Esperava-se o retorno dos dados do usuário no caso positivo.")
        self.assertIsInstance(result, tuple, "O retorno no caso positivo deve ser do tipo tuple.")

        # Resetar mocks para o próximo caso
        mock_cursor.reset_mock()

        # Caso negativo: usuário não encontrado
        mock_cursor.fetchone.return_value = None
        result = check_login(email, senha)

        # Validação do comando SQL
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM User WHERE user_email = ? AND user_password = ?",
            (email, senha)
        )

        # Validação do retorno no caso negativo
        self.assertIsNone(result, "Esperava-se None no caso negativo, quando o usuário não é encontrado.")

    @patch("database.cursor")
    @patch("database.con")
    def test_registrar_denuncia(self, mock_con, mock_cursor):
        user_cpf = 12345678901
        localizacao = "Rua das Flores, 123"
        bairro = "Centro"
        denuncia_texto = "Buraco na rua"
        foto_path = "path/to/image.png"

        # Caso positivo: todos os dados estão preenchidos corretamente
        result = registrar_denuncia(user_cpf, localizacao, bairro, denuncia_texto, foto_path)

        # Validação do retorno
        self.assertTrue(result, "Esperava-se True no caso positivo, indicando sucesso na operação.")
        self.assertIsInstance(result, bool, "O retorno no caso positivo deve ser do tipo bool.")

        # Validação do comando SQL executado
        mock_cursor.execute.assert_called_once()
        args, _ = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO Incident", args[0], "O SQL executado deveria ser uma inserção na tabela Incident.")
        self.assertEqual(
            args[1], 
            (user_cpf, localizacao, bairro, denuncia_texto, foto_path, unittest.mock.ANY, False),
            "Os parâmetros passados para o SQL não correspondem aos esperados."
        )
        mock_con.commit.assert_called_once()

        # Resetar mocks para o próximo caso
        mock_cursor.reset_mock()
        mock_con.reset_mock()

        # Caso negativo: localização ausente
        result = registrar_denuncia(user_cpf, "", bairro, denuncia_texto, foto_path)

        # Validação do retorno
        self.assertFalse(result, "Esperava-se False no caso negativo, indicando falha na operação.")
        self.assertIsInstance(result, bool, "O retorno no caso negativo deve ser do tipo bool.")

        # Certificar-se de que nenhuma operação foi executada no banco
        mock_cursor.execute.assert_not_called()
        mock_con.commit.assert_not_called()

    @patch("database.cursor")
    def test_listar_denuncias(self, mock_cursor):
        user_cpf = 12345678901
        expected_result = [
            ("2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False),
            ("2024-01-02 13:30:00", "Av. Central, 456", "Centro", "Lâmpada queimada", True)
        ]

        # Configuração do retorno esperado do banco de dados
        mock_cursor.fetchall.return_value = expected_result

        # Chamar a função a ser testada
        result = listar_denuncias(user_cpf)

        # Normalizar a consulta SQL esperada e a real para evitar discrepâncias de espaçamento
        def normalize_sql(sql):
            return " ".join(sql.split())

        expected_sql = """
            SELECT incident_data_hora, incident_address, incident_bairro, incident_denuncia, incident_resolvido
            FROM Incident WHERE incident_user_cpf = ?
        """
        
        # Normalizando a SQL esperada
        expected_sql_normalized = normalize_sql(expected_sql)

        # Normalizando a SQL real
        real_sql_normalized = normalize_sql(mock_cursor.execute.call_args[0][0])

        # Comparar as versões normalizadas
        self.assertEqual(real_sql_normalized, expected_sql_normalized, "O comando SQL executado não corresponde ao esperado.")

        # Validação do retorno
        self.assertEqual(result, expected_result, "O resultado retornado não corresponde ao esperado.")
        self.assertIsInstance(result, list, "O retorno da função deve ser uma lista.")

        # Verificação adicional (caso necessário): se o retorno está no formato esperado
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 5 for item in result), 
                        "Cada item da lista deve ser uma tupla com 5 elementos.")

    @patch("database.cursor")
    def test_listar_denuncias_por_bairro(self, mock_cursor):
        # Dados de Entrada
        user_cpf = 12345678901
        bairro = "Centro"
        
        # Configuração do retorno esperado do banco de dados
        mock_cursor.fetchall.return_value = [
            ("2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False),
            ("2024-01-02 13:30:00", "Av. Central, 456", "Centro", "Lâmpada queimada", True),
        ]

        # Chamar a função a ser testada
        result = listar_denuncias_por_bairro(user_cpf, bairro)

        # SQL esperado
        sql_esperado = """
            SELECT incident_data_hora, incident_address, incident_bairro, incident_denuncia, incident_resolvido 
            FROM Incident 
            WHERE incident_user_cpf = ? AND incident_bairro = ?
        """
        
        # Normalização da string SQL para ignorar quebras de linha e espaços extras
        def normalize_sql(sql):
            return " ".join(sql.split())
        
        # Normalizando as SQLs
        sql_real = normalize_sql(mock_cursor.execute.call_args[0][0])
        sql_esperado = normalize_sql(sql_esperado)

        # Comparar a SQL real com a esperada
        self.assertEqual(sql_real, sql_esperado, "O comando SQL executado não corresponde ao esperado.")

        # Verificação do retorno
        self.assertEqual(result, [
            ("2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False),
            ("2024-01-02 13:30:00", "Av. Central, 456", "Centro", "Lâmpada queimada", True),
        ], "O resultado retornado não corresponde ao esperado.")
        
        self.assertIsInstance(result, list, "O retorno da função deve ser uma lista.")

        # Verificar se cada item é uma tupla com 5 elementos
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 5 for item in result), 
                        "Cada item da lista deve ser uma tupla com 5 elementos.")


    @patch("database.cursor")
    def test_listar_todas_denuncias(self, mock_cursor):
        # Configuração do retorno esperado do banco de dados
        expected_result = [
            (1, "2024-01-01 12:00:00", "Rua das Flores, 123", "Centro", "Buraco na rua", False)
        ]

        mock_cursor.fetchall.return_value = expected_result
        
        # Chamar a função a ser testada
        result = listar_todas_denuncias()

        # Verificar se o comando SQL foi executado corretamente
        mock_cursor.execute.assert_called_once_with(
            "SELECT incident_id, incident_data_hora, incident_address, incident_bairro, incident_denuncia, incident_resolvido FROM Incident"
        )

        # Validação do retorno
        self.assertEqual(result, expected_result, "O resultado retornado não corresponde ao esperado.")
        self.assertIsInstance(result, list, "O retorno da função deve ser uma lista.")

        # Verificar se cada item é uma tupla com 6 elementos
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 6 for item in result), 
                        "Cada item da lista deve ser uma tupla com 6 elementos.")

    @patch("database.cursor")
    @patch("database.con")
    def test_atualizar_status_denuncia(self, mock_con, mock_cursor):
        # Dados de Entrada
        incident_id = 1
        novo_status = True

        # Chamar a função a ser testada
        result = atualizar_status_denuncia(incident_id, novo_status)

        # Verificar se o comando SQL foi executado corretamente
        mock_cursor.execute.assert_called_once_with(
            "UPDATE Incident SET incident_resolvido = ? WHERE incident_id = ?", 
            (novo_status, incident_id)
        )

        # Verificar se o commit foi chamado
        mock_con.commit.assert_called_once()

        # Validação do retorno
        self.assertIsNone(result, "O retorno esperado para o caso positivo deve ser None.")


    @patch("database.cursor")
    def test_obter_todos_enderecos(self, mock_cursor):
        # Dados esperados de retorno
        expected_result = ["Rua das Flores, 123", "Av. Central, 456"]
        
        # Configuração do retorno esperado do banco de dados
        mock_cursor.fetchall.return_value = [("Rua das Flores, 123",), ("Av. Central, 456",)]

        # Chamar a função a ser testada
        result = obter_todos_enderecos()

        # Verificar se o comando SQL foi executado corretamente
        mock_cursor.execute.assert_called_once_with(
            "SELECT incident_address FROM Incident WHERE incident_resolvido = 0"
        )

        # Verificação do retorno
        self.assertEqual(result, expected_result, "O retorno da função não é o esperado.")
        self.assertIsInstance(result, list, "O retorno não é do tipo 'list'.")


if __name__ == '__main__':
    unittest.main()
