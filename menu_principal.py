# menu_principal.py
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
import database
import sys
from PyQt5.QtWidgets import QApplication
from datetime import datetime
from Mapa import MapaApp

def exibir_menu_principal(user_id):
    janela = Tk()  # Cria uma nova janela
    janela.title("Relato Popular - Menu Principal")
    janela.geometry("400x500")

    # Funções da interface gráfica
    def open_nova_denuncia():
        tela_menu.pack_forget()
        tela_nova_denuncia.pack(fill="both", expand=True)

    def open_acompanhar_denuncias():
        tela_menu.pack_forget()
        carregar_denuncias()
        tela_acompanhar_denuncias.pack(fill="both", expand=True)

    def voltar_menu():
        tela_nova_denuncia.pack_forget()
        tela_acompanhar_denuncias.pack_forget()
        tela_menu.pack(fill="both", expand=True)

    def carregar_denuncias(bairro=None):
        # Limpar a área de exibição de denúncias anteriores
        for widget in frame_denuncias.winfo_children():
            widget.destroy()

        # Carregar denúncias, aplicando o filtro de bairro, se fornecido
        if bairro:
            denuncias = database.listar_denuncias_por_bairro(user_id, bairro)
        else:
            denuncias = database.listar_denuncias(user_id)

        # Exibir as denúncias
        for denuncia in denuncias:
            # Descompactar os valores da denúncia, assumindo que a consulta retorna 5 valores
            data_hora, localizacao, bairro, texto, resolvido = denuncia
            status = "Resolvido" if resolvido else "Pendente"
            Label(frame_denuncias, text=f"{data_hora} - {localizacao}\nBairro: {bairro}\nStatus: {status}\n\n{texto}", 
                wraplength=280, relief="solid", padx=10, pady=10).pack(pady=5)
            
    def selecionar_foto():
        global foto_path
        foto_path = filedialog.askopenfilename(title="Selecionar uma imagem",
                                               filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if foto_path:
            messagebox.showinfo("Imagem selecionada", f"Imagem selecionada: {foto_path.split('/')[-1]}")

    def salvar_denuncia():
        localizacao = entry_localizacao.get()
        bairro = entry_bairro.get()
        denuncia_texto = entry_denuncia.get("1.0", END).strip()
        
        if not localizacao or not denuncia_texto:
            messagebox.showerror("Erro", "Por favor, preencha os campos obrigatórios.")
            return
        if not localizacao or not bairro or not denuncia_texto:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return
        
        database.registrar_denuncia(user_id, localizacao, bairro, denuncia_texto, foto_path)
        messagebox.showinfo("Sucesso", "Denúncia registrada com sucesso!")
        voltar_menu()

    # Tela do Menu Principal
    tela_menu = Frame(janela)
    Label(tela_menu, text="Menu Principal", font=("Arial", 16)).pack(pady=10)

    botao_nova_denuncia = Button(tela_menu, text="Nova Denúncia", command=open_nova_denuncia)
    botao_nova_denuncia.pack(pady=10)

    botao_acompanhar_denuncias = Button(tela_menu, text="Acompanhar Denúncias", command=open_acompanhar_denuncias)
    botao_acompanhar_denuncias.pack(pady=10)

    # Tela de Nova Denúncia
    tela_nova_denuncia = Frame(janela)
    Label(tela_nova_denuncia, text="Nova Denúncia", font=("Arial", 16)).pack(pady=10)

    Label(tela_nova_denuncia, text="Localização:").pack()
    entry_localizacao = Entry(tela_nova_denuncia, width=50)
    entry_localizacao.pack(pady=5)

    Label(tela_nova_denuncia, text="Bairro:").pack()
    entry_bairro = Entry(tela_nova_denuncia, width=50)
    entry_bairro.pack(pady=5)

    Label(tela_nova_denuncia, text="Denúncia:").pack()
    entry_denuncia = Text(tela_nova_denuncia, width=50, height=10)
    entry_denuncia.pack(pady=5)

    botao_selecionar_foto = Button(tela_nova_denuncia, text="Selecionar Foto", command=selecionar_foto)
    botao_selecionar_foto.pack(pady=5)

    botao_salvar = Button(tela_nova_denuncia, text="Salvar", command=salvar_denuncia)
    botao_salvar.pack(pady=10)

    botao_voltar = Button(tela_nova_denuncia, text="Voltar", command=voltar_menu)
    botao_voltar.pack(pady=5)

    # Tela de Acompanhamento de Denúncias
    tela_acompanhar_denuncias = Frame(janela)
    Label(tela_acompanhar_denuncias, text="Minhas Denúncias", font=("Arial", 16)).pack(pady=10)

    # Carregar o mapa ao clicar
    def abrir_mapa():
        # Criar uma aplicação QApplication separada para o PyQt
        app = QApplication(sys.argv)
        mapa_app = MapaApp()
        mapa_app.show()
        sys.exit(app.exec_())  # Inicia o loop do PyQt

    botao_mapa = Button(tela_acompanhar_denuncias, text ="Mapa", command= abrir_mapa)
    botao_mapa.pack(pady=10)

    # Campo de entrada para filtrar por bairro
    Label(tela_acompanhar_denuncias, text="Filtrar por Bairro:").pack(pady=5)
    entry_bairro_filtro = Entry(tela_acompanhar_denuncias, width=30)
    entry_bairro_filtro.pack(pady=5)

    # Botão de filtrar
    botao_filtrar = Button(tela_acompanhar_denuncias, text="Filtrar", 
                        command=lambda: carregar_denuncias(bairro=entry_bairro_filtro.get().strip()))
    botao_filtrar.pack(pady=5)

    frame_denuncias = Frame(tela_acompanhar_denuncias)
    frame_denuncias.pack(pady=10)

    botao_voltar_acompanhar = Button(tela_acompanhar_denuncias, text="Voltar", command=voltar_menu)
    botao_voltar_acompanhar.pack(pady=10)

    # Exibe a tela do menu principal
    tela_menu.pack(fill="both", expand=True)

# menu_principal.py
def exibir_tela_administracao():
    janela_admin = Tk()
    janela_admin.title("Administração - Todas as Denúncias")
    janela_admin.geometry("500x600")

    def carregar_todas_denuncias():
        for widget in frame_denuncias_admin.winfo_children():
            widget.destroy()

        denuncias = database.listar_todas_denuncias()
        for denuncia in denuncias:
            incident_id, data_hora, localizacao, bairro, texto, resolvido = denuncia
            status_text = "Resolvido" if resolvido else "Pendente"
            status_var = StringVar(value=status_text)

            frame = Frame(frame_denuncias_admin)
            frame.pack(pady=5, fill="x")

            Label(frame, text=f"{data_hora} - {localizacao} - Bairro: {bairro}", font=("Arial", 10, "bold")).pack(anchor="w")
            Label(frame, text=texto, wraplength=400, justify="left").pack(anchor="w", padx=10)
            
            status_menu = OptionMenu(frame, status_var, "Resolvido", "Pendente")
            status_menu.pack(side="left", padx=10)

            def salvar_status(incident_id=incident_id, status_var=status_var):
                novo_status = status_var.get() == "Resolvido"
                database.atualizar_status_denuncia(incident_id, novo_status)
                carregar_todas_denuncias()  # Atualiza a lista

            Button(frame, text="Salvar Status", command=salvar_status).pack(side="left")

    # Frame para listar as denúncias
    frame_denuncias_admin = Frame(janela_admin)
    frame_denuncias_admin.pack(fill="both", expand=True, padx=10, pady=10)

    carregar_todas_denuncias()