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

def verificar_elemento(imagem, mensagem_erro):
    """Verifica se um elemento existe na tela."""
    elemento = pyautogui.locateOnScreen(imagem)
    assert elemento, mensagem_erro
    return pyautogui.locateCenterOnScreen(imagem)

def preencher_login(email, senha):
    """Preenche os campos de login."""
    if(email != "" and senha != "senha"):
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.write(email)
        time.sleep(1)
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.write(senha)
    else:
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        time.sleep(1)
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")

def executar_teste(email, senha, mensagem_esperada, descricao_teste):
    """Executa um teste de login."""
    print(f"Iniciando {descricao_teste}...")
    processo = iniciar_aplicacao()
    
    try:
        # Localiza a janela do aplicativo
        pyautogui.getWindowsWithTitle("Relato Popular")[0].maximize()
        
        # Acessa a tela de login
        botao_login = verificar_elemento("imagens/botao_login.png", "Botão Login não encontrado")
        pyautogui.click(botao_login)
        time.sleep(1)
        
        # Preenche os campos de login
        preencher_login(email, senha)
        
        # Confirma o login
        botao_confirmar = verificar_elemento("imagens/botao_confirmar.png", "Botão Confirmar não encontrado")
        pyautogui.click(botao_confirmar)
        time.sleep(1)
        
        # Verifica a mensagem exibida
        verificar_elemento(mensagem_esperada, "Mensagem esperada não exibida")
        print(f"{descricao_teste} concluído com sucesso!")

    except AssertionError as e:
        print(f"Erro no {descricao_teste}: {e}")
    
    finally:
        # Finaliza o programa
        processo.terminate()

def main():
    """Executa todos os testes."""
    # Teste 1: Login e senha corretos
    messagebox.showinfo("Teste 1", "Login e senha corretos.")
    executar_teste("blackbox@gmail.com", "blackbox", "imagens/mensagem_sucesso.png", "Teste 1: Login e senha corretos")
    
    # Teste 2: Login correto, senha incorreta
    messagebox.showwarning("Teste 2", "Login correto, senha incorreta!")
    executar_teste("blackbox@gmail.com", "errado", "imagens/mensagem_erro.png", "Teste 2: Login correto, senha incorreta")
    
    # Teste 3: Campos de formulário vazios
    messagebox.showwarning("Teste 3", "Campos de formulário estão vazios!")
    executar_teste("", "", "imagens/mensagem_erro.png", "Teste 3: Campos de formulário vazios")

if __name__ == "__main__":
    main()