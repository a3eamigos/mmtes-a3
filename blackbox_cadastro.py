import pyautogui
import time
import subprocess
from tkinter import *
from tkinter import messagebox

# Caminho para o seu programa TelaLogin.py
SCRIPT_PATH = "TelaLogin.py"

def iniciar_aplicacao():
    """Inicia o aplicativo e aguarda a interface carregar."""
    print("Iniciando aplicação...")
    processo = subprocess.Popen(["python", SCRIPT_PATH])
    time.sleep(2)  # Aguarda a interface carregar
    return processo

def esperar_janela(titulo, timeout=10):
    """Espera até que a janela com o título especificado esteja disponível."""
    print(f"Aguardando a janela '{titulo}' carregar...")
    for _ in range(timeout):
        janelas = pyautogui.getWindowsWithTitle(titulo)
        if janelas:
            return janelas[0]
        time.sleep(1)
    raise TimeoutError(f"A janela '{titulo}' não foi encontrada após {timeout} segundos.")

def verificar_elemento(imagem, mensagem_erro, timeout=10):
    """Verifica se um elemento existe na tela, com timeout configurável."""
    print(f"Procurando o elemento: {imagem}")
    for _ in range(timeout):
        elemento = pyautogui.locateOnScreen(imagem)  # Sem o argumento 'confidence'
        if elemento:
            return pyautogui.locateCenterOnScreen(imagem)  # Sem o argumento 'confidence'
        time.sleep(1)
    raise AssertionError(mensagem_erro)

def preencher_cadastro(nome, cpf, email, senha):
    """Preenche os campos de cadastro."""
    pyautogui.press("tab")
    pyautogui.write(nome)
    pyautogui.press("tab")
    time.sleep(1
               )
    pyautogui.write(cpf)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.write(email)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.write(senha)

def executar_teste_cadastro(nome, cpf, email, senha, mensagem_esperada, descricao_teste):
    """Executa um teste de cadastro."""
    print(f"Iniciando {descricao_teste}...")
    
    try:
        # Aguarda a janela do aplicativo
        janela = esperar_janela("Relato Popular")
        janela.maximize()
        time.sleep(1)

        # Acessa a tela de login
        botao_login = verificar_elemento("imagens/botao_login.png", "Botão Login não encontrado")
        pyautogui.click(botao_login)
        time.sleep(2)
        
        # Acessa a tela de cadastro
        botao_cadastro = verificar_elemento("imagens/botao_cadastro.png", "Botão Cadastro não encontrado")
        pyautogui.click(botao_cadastro)
        time.sleep(2)
        
        # Preenche os campos de cadastro
        preencher_cadastro(nome, cpf, email, senha)
        
        # Confirma o cadastro
        botao_confirmar_cadastro = verificar_elemento("imagens/botao_confirmar_cadastro.png", "Botão Confirmar Cadastro não encontrado")
        pyautogui.click(botao_confirmar_cadastro)
        time.sleep(3)
        
        # Verifica a mensagem exibida
        verificar_elemento(mensagem_esperada, "Mensagem esperada não exibida")
        print(f"{descricao_teste} concluído com sucesso!")

    except TimeoutError as e:
        print(e)
    except AssertionError as e:
        print(f"Erro no {descricao_teste}: {e}")

def executar_todos_os_testes():
    """Executa todos os testes consecutivamente com reinicialização do aplicativo entre eles."""
    testes = [
        {
            "nome": "Novo Usuario",
            "cpf": "1234567890000",
            "email": "novo_usuario@example.com",
            "senha": "senha123",
            "mensagem_esperada": "imagens/mensagem_sucesso_cadastro.png",
            "descricao": "Teste 1: Cadastro bem-sucedido"
        },
        {
            "nome": "Usuario Existente",
            "cpf": "1234567890000",
            "email": "usuario_existente@example.com",
            "senha": "senha123",
            "mensagem_esperada": "imagens/mensagem_erro_usuario_existente.png",
            "descricao": "Teste 2: Cadastro com usuário já existente"
        },
        {
            "nome": "",
            "cpf": "",
            "email": "",
            "senha": "",
            "mensagem_esperada": "imagens/mensagem_erro_cadastro_vazio.png",
            "descricao": "Teste 3: Cadastro com campos obrigatórios vazios"
        }
    ]

    for i, teste in enumerate(testes, start=1):
        # Exibe a mensagem antes de iniciar o teste
        if i == 1:
            messagebox.showinfo(f"Teste {i}", f"{teste['descricao']}. Clique em OK para começar.")
        elif i == 2:
            messagebox.showwarning(f"Teste {i}", f"{teste['descricao']}. Clique em OK para continuar.")
        elif i == 3:
            messagebox.showerror(f"Teste {i}", f"{teste['descricao']}. Clique em OK para prosseguir.")
        
        # Inicia o aplicativo
        processo = iniciar_aplicacao()

        try:
            # Executa o teste atual
            executar_teste_cadastro(
                teste["nome"],
                teste["cpf"],
                teste["email"],
                teste["senha"],
                teste["mensagem_esperada"],
                teste["descricao"]
            )
        finally:
            # Encerra o aplicativo após o teste
            processo.terminate()
            print(f"Teste {i} concluído. Aplicativo reiniciado para o próximo teste.")
            time.sleep(1)  # Pausa antes de reiniciar o aplicativo

def main():
    """Executa todos os testes de forma sequencial com reinicialização."""
    executar_todos_os_testes()

if __name__ == "__main__":
    main()
