# TelaLogin.py
from tkinter import *
from tkinter import messagebox
import database
import menu_principal

def open_login():
    tela_inicial.pack_forget()
    tela_login.pack(fill="both", expand=True)

def open_cadastro():
    tela_login.pack_forget()
    tela_cadastro.pack(fill="both", expand=True)

def return_to_login():
    tela_cadastro.pack_forget()
    tela_login.pack(fill="both", expand=True)

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
    # Verificar se o CPF ou o email já estão cadastrados
    if database.verificar_usuario_existente(cpf, email):
        messagebox.showerror("Erro", "CPF ou E-mail já cadastrados.")
    else:
        database.adicionar_usuario(nome, cpf, email, senha)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        return_to_login()

# Configuração da janela principal
janela = Tk()
janela.title("Relato Popular")
janela.geometry("300x400")

# Tela Inicial
tela_inicial = Frame(janela)
tela_inicial.pack(fill="both", expand=True)

titulo_inicial = Label(tela_inicial, text="Bem-vindo ao Sistema", font=("Arial", 16))
titulo_inicial.pack(pady=20)

botao_login = Button(tela_inicial, text="Login", command=open_login)
botao_login.pack(pady=10)

# Tela de Login
tela_login = Frame(janela)
titulo_login = Label(tela_login, text="Login", font=("Arial", 16))
titulo_login.pack(pady=10)

entry_email = Entry(tela_login, width=30)
entry_email.insert(0, "E-mail")
entry_email.pack(pady=5)

entry_senha = Entry(tela_login, width=30, show="*")
entry_senha.insert(0, "Senha")
entry_senha.pack(pady=5)

botao_confirmar = Button(tela_login, text="Confirmar", command=realizar_login)
botao_confirmar.pack(pady=10)

link_criar_conta = Label(tela_login, text="Criar conta", fg="blue", cursor="hand2")
link_criar_conta.pack(pady=5)
link_criar_conta.bind("<Button-1>", lambda e: open_cadastro())

# Tela de Cadastro
tela_cadastro = Frame(janela)

titulo_cadastro = Label(tela_cadastro, text="Cadastro", font=("Arial", 16))
titulo_cadastro.pack(pady=10)

entry_nome = Entry(tela_cadastro, width=30)
entry_nome.insert(0, "Nome")
entry_nome.pack(pady=5)

entry_cpf = Entry(tela_cadastro, width=30)
entry_cpf.insert(0, "CPF")
entry_cpf.pack(pady=5)

entry_email_cadastro = Entry(tela_cadastro, width=30)
entry_email_cadastro.insert(0, "E-mail")
entry_email_cadastro.pack(pady=5)

entry_senha_cadastro = Entry(tela_cadastro, width=30, show="*")
entry_senha_cadastro.insert(0, "Senha")
entry_senha_cadastro.pack(pady=5)

botao_cadastrar = Button(tela_cadastro, text="Cadastrar", command=cadastrar_usuario)
botao_cadastrar.pack(pady=10)

botao_voltar = Button(tela_cadastro, text="Voltar", command=return_to_login)
botao_voltar.pack(pady=5)

# Inicia a tela inicial
tela_inicial.pack(fill="both", expand=True)

janela.mainloop()