from tkinter import *
from tkinter import messagebox
# Instale com = pip install ttkbootstrap
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import re
import database
import menu_principal

# Função para criar placeholders



def criar_placeholder(entry, texto, is_password=False):
    entry.insert(0, texto)
    entry.config(fg="grey")

    def on_focus_in(event):
        if entry.get() == texto:
            entry.delete(0, "end")
            entry.config(fg="black")
            if is_password:
                entry.config(show="*")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, texto)
            entry.config(fg="grey")
            if is_password:
                entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Função para validação de e-mail


def validar_email(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email) is not None

# Troca de telas


def open_login():
    tela_inicial.pack_forget()
    tela_login.pack(fill="both", expand=True)


def open_cadastro():
    tela_login.pack_forget()
    tela_cadastro.pack(fill="both", expand=True)


def return_to_login():
    tela_cadastro.pack_forget()
    tela_login.pack(fill="both", expand=True)

# Ações de login e cadastro


def realizar_login():
    email = entry_email.get()
    senha = entry_senha.get()
    user = database.check_login(email, senha)
    if user:
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        janela.destroy()
        if email == "admin" and senha == "admin":
            menu_principal.exibir_tela_administracao()
        else:
            menu_principal.exibir_menu_principal(user_id=user[0])
    else:
        messagebox.showerror("Erro", "E-mail ou senha incorretos.")


def cadastrar_usuario():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    email = entry_email_cadastro.get()
    senha = entry_senha_cadastro.get()

    if not nome.strip() or not cpf.strip() or not email.strip() or not senha.strip():
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    if not validar_email(email):
        messagebox.showerror("Erro", "E-mail inválido.")
        return

    if database.verificar_usuario_existente(cpf, email):
        messagebox.showerror("Erro", "CPF ou E-mail já cadastrados.")
    else:
        database.adicionar_usuario(nome, cpf, email, senha)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        return_to_login()


# Configuração da janela principal
janela = ttk.Window(themename="cosmo")
janela.title("Relato Popular")
janela.geometry("300x400")

# Tela Inicial
tela_inicial = Frame(janela)
tela_inicial.pack(fill="both", expand=True)

titulo_inicial = Label(
    tela_inicial, text="Bem-vindo ao Sistema", font=("Arial", 16))
titulo_inicial.pack(pady=20)

botao_login = ttk.Button(tela_inicial, text="Login",
                         bootstyle=SUCCESS, command=open_login)

botao_login.pack(pady=10)

# Tela de Login
tela_login = Frame(janela)
titulo_login = Label(tela_login, text="Login", font=("Arial", 16))
titulo_login.pack(pady=10)

entry_email = Entry(tela_login, width=30)
criar_placeholder(entry_email, "E-mail")
entry_email.pack(pady=5)

entry_senha = Entry(tela_login, width=30)
criar_placeholder(entry_senha, "Senha", is_password=True)
entry_senha.pack(pady=5)

botao_confirmar = Button(tela_login, text="Confirmar", command=realizar_login)
botao_confirmar.pack(pady=10)

link_criar_conta = Label(tela_login, text="Criar conta",
                         fg="blue", cursor="hand2")
link_criar_conta.pack(pady=5)
link_criar_conta.bind("<Button-1>", lambda e: open_cadastro())

# Tela de Cadastro
tela_cadastro = Frame(janela)

titulo_cadastro = Label(tela_cadastro, text="Cadastro", font=("Arial", 16))
titulo_cadastro.pack(pady=10)

entry_nome = Entry(tela_cadastro, width=30)
criar_placeholder(entry_nome, "Nome")
entry_nome.pack(pady=5)

entry_cpf = Entry(tela_cadastro, width=30)
criar_placeholder(entry_cpf, "CPF")
entry_cpf.pack(pady=5)

entry_email_cadastro = Entry(tela_cadastro, width=30)
criar_placeholder(entry_email_cadastro, "E-mail")
entry_email_cadastro.pack(pady=5)

entry_senha_cadastro = Entry(tela_cadastro, width=30)
criar_placeholder(entry_senha_cadastro, "Senha", is_password=True)
entry_senha_cadastro.pack(pady=5)

botao_cadastrar = Button(
    tela_cadastro, text="Cadastrar", command=cadastrar_usuario)
botao_cadastrar.pack(pady=10)

botao_voltar = Button(tela_cadastro, text="Voltar", command=return_to_login)
botao_voltar.pack(pady=5)

# Inicia a tela inicial
tela_inicial.pack(fill="both", expand=True)

janela.mainloop()
