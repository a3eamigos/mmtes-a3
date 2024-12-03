import pyautogui
import time
import subprocess
from tkinter import *
from tkinter import messagebox
from pathlib import Path

# Caminho para o seu programa TelaLogin.py
SCRIPT_PATH_LOGIN = "TelaLogin.py"

def iniciar_aplicacao(script_path):
    """Inicia o aplicativo e aguarda a interface carregar."""
    print(f"Iniciclsando aplicação {script_path}...")
    processo = subprocess.Popen(["python", script_path])
    time.sleep(2)  # Aguarda a interface carregar
    return processo

def verificar_elemento(imagem, mensagem_erro):
    """Verifica se um elemento existe na tela."""
    elemento = pyautogui.locateOnScreen(imagem)
    assert elemento, mensagem_erro
    return pyautogui.locateCenterOnScreen(imagem)

def realizar_login(email, senha):
    """Realiza o login no aplicativo e lida com o popup de sucesso."""
    try:
        # Localiza a janela do aplicativo
        pyautogui.getWindowsWithTitle("Relato Popular")[0].maximize()

        # Clica no botão de login
        botao_login = verificar_elemento("imagens/botao_login.png", "Botão Login não encontrado")
        pyautogui.click(botao_login)
        time.sleep(1)

        # Insere o email e a senha
        pyautogui.press("tab")
        pyautogui.write(email)
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.write(senha)
        time.sleep(1)

        # Clica no botão "Confirmar"
        botao_confirmar = verificar_elemento("imagens/botao_confirmar.png", "Botão Confirmar não encontrado")
        pyautogui.click(botao_confirmar)
        time.sleep(2)

        # Lida com o popup de sucesso
        pyautogui.press("enter")
        time.sleep(3)  # Aguarda a tela do menu principal carregar

        print("Login realizado com sucesso e menu principal carregado!")
    except AssertionError as e:
        print(f"Erro no login: {e}")

def executar_teste_registrar_denuncia(localizacao, bairro, denuncia, descricao_teste):
    """Executa o teste de registrar uma denuncia."""
    print(f"Iniciando {descricao_teste}...")
        
    try:
        # Localiza a janela do menu principal
        pyautogui.getWindowsWithTitle("Relato Popular - Menu Principal")[0].maximize()
        # Clica no botão "Acompanhar Denúncias"
        botao_nova_denuncia = verificar_elemento("imagens/botao_nova_denuncia.png", "Botão Nova Denúncia não encontrado")
        pyautogui.click(botao_nova_denuncia)
        time.sleep(1)

        # Insere o localizacao
        pyautogui.press("tab")
        if localizacao:
            pyautogui.write(localizacao)
        time.sleep(2)
        # Insere o bairro
        pyautogui.press("tab")
        if bairro:
            pyautogui.write(bairro)
        time.sleep(2)
        # Insere a denuncia
        pyautogui.press("tab")
        if denuncia:
            pyautogui.write(denuncia)
        time.sleep(2)
        # Clica no botão "Selecionar foto"
        botao_selecionar_foto = verificar_elemento("imagens/botao_selecionar_foto.png", "Botão Seleciona Foto não encontrado")
        pyautogui.click(botao_selecionar_foto)
        time.sleep(1)
        #Selecionar uma imagem para teste nos arquivos
        caminho_imagem = "mapa_interativo.png"
        pyautogui.write(caminho_imagem)
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)

        botao_salvar = verificar_elemento("imagens/botao_salvar.png", "Botão Salvar não encontrado")
        pyautogui.click(botao_salvar)
        time.sleep(2)
        pyautogui.press("enter")
        
        
        messagebox.showinfo("Teste CT004", "Teste concluído com sucesso.")
        time.sleep(5)

        print(f"{descricao_teste} concluído com sucesso!")
    except AssertionError as e:
        print(f"Erro no {descricao_teste}: {e}")

def executar_teste_ct004():
    """Executa o teste CT004 - Registrar Denúncia."""
    # Mensagem inicial do teste
    messagebox.showinfo("Teste CT004", "Listar Denúncia. Clique em OK para começar.")

    # Inicia a aplicação TelaLogin
    processo_login = iniciar_aplicacao(SCRIPT_PATH_LOGIN)

    try:
        # Realiza o login
        realizar_login(email="blackbox@gmail.com", senha="blackbox")

        # Executa o teste de listar denúncia
        executar_teste_registrar_denuncia(
            localizacao="Rua Sotero Monteiro",  # Bairro a ser filtrado
            bairro="Pituba",
            denuncia="PEGA AQUI NO MEU MOCKITO",
            descricao_teste="Teste CT004: registrar Denúncia no Bairro Pituba"
        )
    finally:
        # Fecha a aplicação após o teste
        processo_login.terminate()
        print("Teste CT004 concluído e aplicativo encerrado.")

def main():
    """Executa o teste CT004."""
    executar_teste_ct004()

if __name__ == "__main__":
    main()