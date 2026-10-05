import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import os
import re
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO
# ============================================================

NOME_BD = "banco.db"
PASTA_IMG = "img"

CAMINHO_ICONE = os.path.join(PASTA_IMG, "icone.ico")
CAMINHO_BG = os.path.join(PASTA_IMG, "login-bg.png")


# ============================================================
# BASE DE DADOS
# ============================================================

def conectar_bd():
    return sqlite3.connect(NOME_BD)


def criar_bd():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilizadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento TEXT,
            telefone TEXT,
            email TEXT,
            nivel TEXT,
            turma TEXT,
            tipo_ukulele TEXT,
            contribuicao TEXT
        )
    """)

    conn.commit()
    conn.close()


def criar_hash(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# JANELA
# ============================================================

root = tk.Tk()

root.title("UkeColetivo - Login")
root.geometry("1000x800")
root.minsize(900, 700)

if os.path.exists(CAMINHO_ICONE):
    root.iconbitmap(CAMINHO_ICONE)


# ============================================================
# ESTILOS
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "Titulo.TLabel",
    font=("Segoe UI", 24, "bold")
)

style.configure(
    "Acao.TButton",
    font=("Segoe UI", 10, "bold"),
    padding=8
)

style.configure(
    "Treeview",
    rowheight=30,
    font=("Segoe UI", 10)
)

style.map(
    "Treeview",
    background=[("selected", "#2e7d4f")],
    foreground=[("selected", "white")]
)

style.configure(
    "Cadastrar.TButton",
    font=("Segoe UI", 10, "bold"),
    padding=8,
    background="#16a34a",
    foreground="white"
)

style.configure(
    "Alterar.TButton",
    font=("Segoe UI", 10, "bold"),
    padding=8,
    background="#2563eb",
    foreground="white"
)

style.configure(
    "Excluir.TButton",
    font=("Segoe UI", 10, "bold"),
    padding=8,
    background="#dc2626",
    foreground="white"
)

style.configure(
    "Limpar.TButton",
    font=("Segoe UI", 10, "bold"),
    padding=8,
    background="white",
    foreground="black"
)

# ============================================================
# FUNÇÕES GERAIS
# ============================================================

def limpar_tela():

    for widget in root.winfo_children():
        widget.destroy()


def centralizar_janela():

    root.update_idletasks()

    largura = root.winfo_width()
    altura = root.winfo_height()

    x = (root.winfo_screenwidth() - largura) // 2
    y = (root.winfo_screenheight() - altura) // 2

    root.geometry(
        f"{largura}x{altura}+{x}+{y}"
    )


# ============================================================
# TELA DE LOGIN
# ============================================================

def tela_login():

    limpar_tela()

    root.title("UkeColetivo - Login")

    frame_principal = tk.Frame(
        root,
        bg="white"
    )

    frame_principal.pack(
        fill="both",
        expand=True
    )

    # --------------------------------------------------------
    # IMAGEM
    # --------------------------------------------------------

    frame_imagem = tk.Frame(
        frame_principal,
        bg="#f5f5f5",
        width=450
    )

    frame_imagem.pack(
        side="left",
        fill="both",
        expand=True
    )

    frame_imagem.pack_propagate(False)

    if os.path.exists(CAMINHO_BG):

        imagem = tk.PhotoImage(
            file=CAMINHO_BG
        )

        label_imagem = tk.Label(
            frame_imagem,
            image=imagem,
            bg="#f5f5f5"
        )

        label_imagem.image = imagem

        label_imagem.pack(
            fill="both",
            expand=True
        )

    else:

        tk.Label(
            frame_imagem,
            text="Aprenda\nToque\nCompartilhe",
            font=("Segoe UI", 25, "bold"),
            fg="#174d2b",
            bg="#f5f5f5",
            justify="center"
        ).pack(expand=True)

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    frame_login = tk.Frame(
        frame_principal,
        bg="white",
        padx=50
    )

    frame_login.pack(
        side="right",
        fill="both",
        expand=True
    )

    tk.Label(
        frame_login,
        text="UkeColetivo",
        font=("Segoe UI", 28, "bold"),
        fg="#174d2b",
        bg="white"
    ).pack(
        pady=(70, 5)
    )

    tk.Label(
        frame_login,
        text="Música que aproxima",
        font=("Segoe UI", 12),
        fg="#555555",
        bg="white"
    ).pack(
        pady=(0, 35)
    )

    tk.Label(
        frame_login,
        text="E-mail",
        bg="white",
        anchor="w"
    ).pack(fill="x")

    entrada_email = ttk.Entry(
        frame_login,
        font=("Segoe UI", 11)
    )

    entrada_email.pack(
        fill="x",
        ipady=8,
        pady=(5, 15)
    )

    tk.Label(
        frame_login,
        text="Password",
        bg="white",
        anchor="w"
    ).pack(fill="x")

    entrada_password = ttk.Entry(
        frame_login,
        show="•",
        font=("Segoe UI", 11)
    )

    entrada_password.pack(
        fill="x",
        ipady=8,
        pady=(5, 25)
    )

    def fazer_login():

        email = entrada_email.get().strip()
        password = entrada_password.get()

        if not email or not password:

            messagebox.showwarning(
                "Atenção",
                "Preencha o e-mail e a Password."
            )

            return

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome
            FROM utilizadores
            WHERE email = ? AND password = ?
        """, (
            email,
            criar_hash(password)
        ))

        utilizador = cursor.fetchone()

        conn.close()

        if utilizador:

            tela_principal(utilizador)

            messagebox.showinfo(
                "Sucesso",
                f"Bem-vindo(a), {utilizador[1]}!"
            )

        else:

            messagebox.showerror(
                "Erro",
                "E-mail ou password incorretos."
            )

    ttk.Button(
        frame_login,
        text="Entrar",
        style="Acao.TButton",
        command=fazer_login
    ).pack(
        fill="x",
        pady=(0, 15)
    )

    ttk.Button(
        frame_login,
        text="Criar conta",
        command=tela_cadastro
    ).pack(fill="x")

    entrada_email.focus()


# ============================================================
# TELA DE CADASTRO DE UTILIZADOR
# ============================================================

def tela_cadastro():

    limpar_tela()

    root.title("UkeColetivo - Criar conta")

    frame = tk.Frame(
        root,
        bg="white",
        padx=100,
        pady=40
    )

    frame.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        frame,
        text="Criar conta",
        font=("Segoe UI", 26, "bold"),
        fg="#174d2b",
        bg="white"
    ).pack(
        pady=(10, 5)
    )

    tk.Label(
        frame,
        text="Cadastre-se para acessar o UkeColetivo",
        font=("Segoe UI", 11),
        fg="#555555",
        bg="white"
    ).pack(
        pady=(0, 30)
    )

    campos = []

    def criar_campo(texto, password=False):

        tk.Label(
            frame,
            text=texto,
            bg="white",
            anchor="w"
        ).pack(fill="x")

        entrada = ttk.Entry(
            frame,
            show="•" if password else ""
        )

        entrada.pack(
            fill="x",
            ipady=7,
            pady=(5, 15)
        )

        campos.append(entrada)

        return entrada

    entrada_nome = criar_campo("Nome completo")
    entrada_email = criar_campo("E-mail")
    entrada_password = criar_campo(
        "Password",
        True
    )
    entrada_confirmar = criar_campo(
        "Confirmar password",
        True
    )

    def registrar():

        nome = entrada_nome.get().strip()
        email = entrada_email.get().strip()
        password = entrada_password.get()
        confirmar = entrada_confirmar.get()

        if not nome or not email or not password or not confirmar:

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos."
            )

            return
        

        if password != confirmar:

            messagebox.showwarning(
                "Atenção",
                "As passwords não coincidem."
            )

            return

        if len(password) < 6:

            messagebox.showwarning(
                "Atenção",
                "A password deve ter pelo menos 6 caracteres."
            )

            return

        conn = conectar_bd()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO utilizadores
                (nome, email, password)
                VALUES (?, ?, ?)
            """, (
                nome,
                email,
                criar_hash(password)
            ))

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            messagebox.showerror(
                "Erro",
                "Este e-mail já está cadastrado."
            )

            return

        conn.close()

        messagebox.showinfo(
            "Sucesso",
            "Conta criada com sucesso!"
        )

        tela_login()

    ttk.Button(
        frame,
        text="Criar conta",
        style="Acao.TButton",
        command=registrar
    ).pack(
        fill="x",
        pady=(0, 10)
    )

    ttk.Button(
        frame,
        text="Voltar",
        command=tela_login
    ).pack(fill="x")

    entrada_nome.focus()


# ============================================================
# TELA PRINCIPAL - GESTÃO DE ALUNOS
# ============================================================

def tela_principal(utilizador):

    limpar_tela()
    root.title("UkeColetivo - Gestão de Alunos")

    # ========================================================
    # CABEÇALHO
    # ========================================================

    cabecalho = tk.Frame(
        root,
        bg="#174d2b",
        height=65
    )
    cabecalho.pack(fill="x")
    cabecalho.pack_propagate(False)

    tk.Label(
        cabecalho,
        text="UkeColetivo",
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg="#174d2b"
    ).pack(
        side="left",
        padx=25
    )

    tk.Label(
        cabecalho,
        text=f"Utilizador: {utilizador[1]}",
        font=("Segoe UI", 10),
        fg="white",
        bg="#174d2b"
    ).pack(
        side="left",
        padx=10
    )

    def sair():

        resposta = messagebox.askyesno(
            "Sair",
            "Deseja realmente sair da aplicação?"
        )

        if resposta:
            tela_login()

    ttk.Button(
        cabecalho,
        text="Sair",
        command=sair
    ).pack(
        side="right",
        padx=20
    )

    # ========================================================
    # ÁREA PRINCIPAL
    # ========================================================

    principal = tk.Frame(
        root,
        bg="#f4f6f5"
    )
    principal.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=18
    )

    # ========================================================
    # TÍTULO
    # ========================================================

    tk.Label(
        principal,
        text="Gestão de Alunos",
        font=("Segoe UI", 18, "bold"),
        fg="#174d2b",
        bg="#f4f6f5"
    ).pack(
        anchor="w",
        pady=(0, 12)
    )

    # ========================================================
    # FORMULÁRIO
    # ========================================================

    frame_form = tk.LabelFrame(
        principal,
        text="Dados do aluno",
        font=("Segoe UI", 10, "bold"),
        bg="#f4f6f5",
        padx=15,
        pady=5
    )
    frame_form.pack(
        fill="x"
    )

    frame_form.columnconfigure(1, weight=1)
    frame_form.columnconfigure(3, weight=1)

    # ========================================================
    # VARIÁVEIS
    # ========================================================

    id_selecionado = tk.StringVar()

    nome_var = tk.StringVar()
    nascimento_var = tk.StringVar()
    telefone_var = tk.StringVar()
    email_var = tk.StringVar()

    nivel_var = tk.StringVar(value="Iniciante")
    turma_var = tk.StringVar(value="UKE-01")
    ukulele_var = tk.StringVar(value="Soprano")
    contribuicao_var = tk.StringVar(value="Coletiva")

    turma_filtro_var = tk.StringVar(value="Todas")
    nivel_filtro_var = tk.StringVar(value="Todos")
    ukulele_filtro_var = tk.StringVar(value="Todos")
    contribuicao_filtro_var = tk.StringVar(value="Todas")

    # ========================================================
    # LINHA 1
    # ========================================================

    tk.Label(
        frame_form,
        text="Nome:",
        bg="#f4f6f5",
        font=("Segoe UI", 9)
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=(5, 8),
        pady=7
    )

    entrada_nome = ttk.Entry(
        frame_form,
        textvariable=nome_var,
        font=("Segoe UI", 10)
    )
    entrada_nome.grid(
        row=0,
        column=1,
        sticky="ew",
        padx=(0, 20),
        pady=7
    )

    tk.Label(
        frame_form,
        text="Nascimento:",
        bg="#f4f6f5",
        font=("Segoe UI", 9)
    ).grid(
        row=0,
        column=2,
        sticky="w",
        padx=(5, 8),
        pady=7
    )

    entrada_nascimento = ttk.Entry(
        frame_form,
        textvariable=nascimento_var,
        font=("Segoe UI", 10)
    )
    entrada_nascimento.grid(
        row=0,
        column=3,
        sticky="ew",
        pady=7
    )

    # ========================================================
    # LINHA 2
    # ========================================================

    tk.Label(
        frame_form,
        text="Telefone:",
        bg="#f4f6f5",
        font=("Segoe UI", 9)
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=(5, 8),
        pady=7
    )

    ttk.Entry(
        frame_form,
        textvariable=telefone_var,
        font=("Segoe UI", 10)
    ).grid(
        row=1,
        column=1,
        sticky="ew",
        padx=(0, 20),
        pady=7
    )

    tk.Label(
        frame_form,
        text="E-mail:",
        bg="#f4f6f5",
        font=("Segoe UI", 9)
    ).grid(
        row=1,
        column=2,
        sticky="w",
        padx=(5, 8),
        pady=7
    )

    ttk.Entry(
        frame_form,
        textvariable=email_var,
        font=("Segoe UI", 10)
    ).grid(
        row=1,
        column=3,
        sticky="ew",
        pady=7
    )

    # ========================================================
    # LINHA 3
    # ========================================================

    tk.Label(
        frame_form,
        text="Nível:",
        bg="#f4f6f5",
        font=("Segoe UI", 9)
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=(5, 8),
        pady=7
    )

    combo_nivel = ttk.Combobox(
        frame_form,
        textvariable=nivel_var,
        values=[
            "Iniciante",
            "Intermediário",
            "Avançado"
        ],
        state="readonly",
        font=("Segoe UI", 10)
    )
    combo_nivel.grid(
        row=2,
        column=1,
        sticky="ew",
        padx=(0, 20),
        pady=7
    )

    tk.Label(
        frame_form,
        text="Turma:",
        bg="#f4f6f5",
        font=("Segoe UI", 9)
    ).grid(
        row=2,
        column=2,
        sticky="w",
        padx=(5, 8),
        pady=7
    )

    combo_turma = ttk.Combobox(
        frame_form,
        textvariable=turma_var,
        values=[
            "UKE-01",
            "UKE-02",
            "UKE-03"
        ],
        state="readonly",
        font=("Segoe UI", 10)
    )
    combo_turma.grid(
        row=2,
        column=3,
        sticky="ew",
        pady=7
    )

    # ========================================================
    # LINHA 4
    # ========================================================

    tk.Label(
        frame_form,
        text="Ukulele:",
        bg="#f4f6f5",
        font=("Segoe UI", 9)
    ).grid(
        row=3,
        column=0,
        sticky="w",
        padx=(5, 8),
        pady=4
    )

    combo_ukulele = ttk.Combobox(
        frame_form,
        textvariable=ukulele_var,
        values=[
            "Soprano",
            "Concert",
            "Tenor",
            "Barítono"
        ],
        state="readonly",
        font=("Segoe UI", 10)
    )
    combo_ukulele.grid(
        row=3,
        column=1,
        sticky="ew",
        padx=(0, 20),
        pady=7
    )

    tk.Label(
        frame_form,
        text="Contribuição:",
        bg="#f4f6f5",
        font=("Segoe UI", 9)
    ).grid(
        row=3,
        column=2,
        sticky="w",
        padx=(5, 8),
        pady=7
    )

    combo_contribuicao = ttk.Combobox(
        frame_form,
        textvariable=contribuicao_var,
        values=[
            "Solidária",
            "Coletiva",
            "Generosa"
        ],
        state="readonly",
        font=("Segoe UI", 10)
    )
    combo_contribuicao.grid(
        row=3,
        column=3,
        sticky="ew",
        pady=7
    )

    # ========================================================
    # FUNÇÃO LIMPAR
    # ========================================================

    def limpar_formulario():

        id_selecionado.set("")
        nome_var.set("")
        nascimento_var.set("")
        telefone_var.set("")
        email_var.set("")

        nivel_var.set("Iniciante")
        turma_var.set("UKE-01")
        ukulele_var.set("Soprano")
        contribuicao_var.set("Coletiva")

        tabela.selection_remove(
            tabela.selection()
        )

        entrada_nome.focus()

    # ========================================================
    # VALIDAÇÃO DOS DADOS
    # ========================================================

    def validar_dados():

        nome = nome_var.get().strip()
        nascimento = nascimento_var.get().strip()
        telefone = telefone_var.get().strip()
        email = email_var.get().strip()

        # NOME
        if not nome:
            messagebox.showwarning(
                "Atenção",
                "Informe o nome do aluno."
            )
            entrada_nome.focus()
            return False

        # E-MAIL
        if email:
            padrao_email = r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$"

            if not re.match(padrao_email, email):
                messagebox.showwarning(
                    "Atenção",
                    "Informe um e-mail válido."
                )
                return False

        # TELEFONE
        if telefone:
            numeros = re.sub(r"\D", "", telefone)

            if len(numeros) < 9 or len(numeros) > 15:
                messagebox.showwarning(
                    "Atenção",
                    "Informe um telefone válido."
                )
                return False

        # DATA DE NASCIMENTO
        if nascimento:
            try:
                data = datetime.strptime(
                    nascimento,
                    "%d/%m/%Y"
                )

                if data > datetime.now():
                    messagebox.showwarning(
                        "Atenção",
                        "A data de nascimento não pode ser futura."
                    )
                    return False

            except ValueError:
                messagebox.showwarning(
                    "Atenção",
                    "A data de nascimento deve estar no formato DD/MM/AAAA."
                )
                return False

        return True

    # ========================================================
    # CADASTRAR
    # ========================================================

    def cadastrar():

        if not validar_dados():
            return

        nome = nome_var.get().strip()

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO alunos
            (
                nome,
                data_nascimento,
                telefone,
                email,
                nivel,
                turma,
                tipo_ukulele,
                contribuicao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nome,
            nascimento_var.get().strip(),
            telefone_var.get().strip(),
            email_var.get().strip(),
            nivel_var.get(),
            turma_var.get(),
            ukulele_var.get(),
            contribuicao_var.get()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Sucesso",
            "Aluno cadastrado com sucesso!"
        )

        limpar_formulario()
        carregar_alunos()

    # ========================================================
    # ALTERAR
    # ========================================================

    def alterar():

        id_aluno = id_selecionado.get()

        if not id_aluno:
            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno para alterar."
            )
            return

        if not validar_dados():
            return

        nome = nome_var.get().strip()

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE alunos
            SET
                nome = ?,
                data_nascimento = ?,
                telefone = ?,
                email = ?,
                nivel = ?,
                turma = ?,
                tipo_ukulele = ?,
                contribuicao = ?
            WHERE id = ?
        """, (
            nome,
            nascimento_var.get().strip(),
            telefone_var.get().strip(),
            email_var.get().strip(),
            nivel_var.get(),
            turma_var.get(),
            ukulele_var.get(),
            contribuicao_var.get(),
            id_aluno
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Sucesso",
            "Dados do aluno alterados com sucesso!"
        )

        limpar_formulario()
        carregar_alunos()
        
    # ========================================================
    # EXCLUIR
    # ========================================================

    def excluir():

        id_aluno = id_selecionado.get()

        if not id_aluno:

            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno para excluir."
            )

            return

        resposta = messagebox.askyesno(
            "Confirmar exclusão",
            f'Deseja realmente excluir "{nome_var.get()}"?'
        )

        if not resposta:
            return

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM alunos WHERE id = ?",
            (id_aluno,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Sucesso",
            "Aluno excluído com sucesso!"
        )

        limpar_formulario()
        carregar_alunos()

    # ========================================================
    # BOTÕES
    # ========================================================

    frame_botoes = tk.Frame(
        principal,
        bg="#f4f6f5"
    )

    frame_botoes.pack(
        fill="x",
        pady=12
    )

    ttk.Button(
        frame_botoes,
        text="Cadastrar",
        style="Cadastrar.TButton",
        command=cadastrar
    ).pack(
        side="left",
        padx=(0, 6)
    )

    ttk.Button(
        frame_botoes,
        text="Alterar",
        style="Alterar.TButton",
        command=alterar
    ).pack(
        side="left",
        padx=6
    )

    ttk.Button(
        frame_botoes,
        text="Excluir",
        style="Excluir.TButton",
        command=excluir
    ).pack(
        side="left",
        padx=6
    )

    ttk.Button(
        frame_botoes,
        text="Limpar",
        style="Limpar.TButton",
        command=limpar_formulario
    ).pack(
        side="left",
        padx=6
    )   

    # ========================================================
    # PESQUISA
    # ========================================================

    frame_pesquisa = tk.Frame(
        principal,
        bg="#f4f6f5"
    )

    frame_pesquisa.pack(
        fill="x",
        pady=(4, 10)
    )

    tk.Label(
        frame_pesquisa,
        text="Pesquisar aluno:",
        bg="#f4f6f5",
        font=("Segoe UI", 10, "bold")
    ).pack(
        side="left",
        padx=(0, 10)
    )

    pesquisa_var = tk.StringVar()

    entrada_pesquisa = ttk.Entry(
        frame_pesquisa,
        textvariable=pesquisa_var,
        font=("Segoe UI", 10)
    )
    entrada_pesquisa.pack(
        side="left",
        fill="x",
        expand=True
    )

        # ========================================================
    # FILTROS
    # ========================================================

    frame_filtros = ttk.Frame(principal)

    frame_filtros.pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )

    ttk.Label(
        frame_filtros,
        text="Turma:"
    ).pack(side="left", padx=(0, 5))

    combo_filtro_turma = ttk.Combobox(
        frame_filtros,
        textvariable=turma_filtro_var,
        values=["Todas", "UKE-01", "UKE-02", "UKE-03"],
        state="readonly",
        width=10
    )
    combo_filtro_turma.pack(side="left", padx=(0, 15))


    ttk.Label(
        frame_filtros,
        text="Nível:"
    ).pack(side="left", padx=(0, 5))

    combo_filtro_nivel = ttk.Combobox(
        frame_filtros,
        textvariable=nivel_filtro_var,
        values=[
            "Todos",
            "Iniciante",
            "Intermediário",
            "Avançado"
        ],
        state="readonly",
        width=15
    )
    combo_filtro_nivel.pack(side="left", padx=(0, 15))


    ttk.Label(
        frame_filtros,
        text="Ukulele:"
    ).pack(side="left", padx=(0, 5))

    combo_filtro_ukulele = ttk.Combobox(
        frame_filtros,
        textvariable=ukulele_filtro_var,
        values=[
            "Todos",
            "Soprano",
            "Concert",
            "Tenor",
            "Barítono"
        ],
        state="readonly",
        width=12
    )
    combo_filtro_ukulele.pack(side="left", padx=(0, 15))


    ttk.Label(
        frame_filtros,
        text="Contribuição:"
    ).pack(side="left", padx=(0, 5))

    combo_filtro_contribuicao = ttk.Combobox(
        frame_filtros,
        textvariable=contribuicao_filtro_var,
        values=[
            "Todas",
            "Solidária",
            "Coletiva",
            "Generosa"
        ],
        state="readonly",
        width=13
    )
    combo_filtro_contribuicao.pack(side="left")

    # ========================================================
    # TABELA
    # ========================================================

    frame_tabela = tk.LabelFrame(
        principal,
        text="Alunos cadastrados",
        font=("Segoe UI", 10, "bold"),
        bg="#f4f6f5",
        padx=5,
        pady=5
    )

    frame_tabela.pack(
        fill="both",
        expand=False,
        pady=(0, 5)
        )

    frame_tabela.configure(height=220)
    frame_tabela.pack_propagate(False)

    colunas = (
        "id",
        "nome",
        "turma",
        "nivel",
        "ukulele",
        "contribuicao"
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=colunas,
        show="headings",
        height=6
    )

    tabela.tag_configure(
    "par",
    background="#ffffff"
    )

    tabela.tag_configure(
    "impar",
    background="#f0f5f2"
    )


    tabela.heading(
        "id",
        text="ID"
    )

    tabela.heading(
        "nome",
        text="Nome"
    )

    tabela.heading(
        "turma",
        text="Turma"
    )

    tabela.heading(
        "nivel",
        text="Nível"
    )

    tabela.heading(
        "ukulele",
        text="Ukulele"
    )

    tabela.heading(
        "contribuicao",
        text="Contribuição"
    )

    tabela.column(
        "id",
        width=55,
        anchor="center",
        stretch=False
    )

    tabela.column(
        "nome",
        width=300,
        anchor="w"
    )

    tabela.column(
        "turma",
        width=100,
        anchor="center"
    )

    tabela.column(
        "nivel",
        width=140,
        anchor="center"
    )

    tabela.column(
        "ukulele",
        width=120,
        anchor="center"
    )

    tabela.column(
        "contribuicao",
        width=150,
        anchor="center"
    )

    scroll = ttk.Scrollbar(
        frame_tabela,
        orient="vertical",
        command=tabela.yview
    )

    tabela.configure(
        yscrollcommand=scroll.set
    )

    tabela.pack(
        side="left",
        fill="both",
        expand=True
    )

    scroll.pack(
        side="right",
        fill="y"
    )

       # ========================================================
    # CARREGAR ALUNOS
    # ========================================================

    def carregar_alunos():

        termo = pesquisa_var.get().strip()

        turma = turma_filtro_var.get()
        nivel = nivel_filtro_var.get()
        ukulele = ukulele_filtro_var.get()
        contribuicao = contribuicao_filtro_var.get()

        conn = conectar_bd()
        cursor = conn.cursor()

        sql = """
            SELECT
                id,
                nome,
                turma,
                nivel,
                tipo_ukulele,
                contribuicao
            FROM alunos
            WHERE 1=1
        """

        parametros = []

        # Pesquisa
        if termo:

            sql += """
                AND (
                    nome LIKE ?
                    OR email LIKE ?
                    OR telefone LIKE ?
                )
            """

            parametros.extend([
                f"%{termo}%",
                f"%{termo}%",
                f"%{termo}%"
            ])

        # Filtro turma
        if turma != "Todas":

            sql += " AND turma = ?"
            parametros.append(turma)

        # Filtro nível
        if nivel != "Todos":

            sql += " AND nivel = ?"
            parametros.append(nivel)

        # Filtro ukulele
        if ukulele != "Todos":

            sql += " AND tipo_ukulele = ?"
            parametros.append(ukulele)

        # Filtro contribuição
        if contribuicao != "Todas":

            sql += " AND contribuicao = ?"
            parametros.append(contribuicao)

        sql += " ORDER BY nome"

        cursor.execute(
            sql,
            parametros
        )

        alunos = cursor.fetchall()

        conn.close()

        for item in tabela.get_children():

            tabela.delete(item)

        for aluno in alunos:

            tabela.insert(
                "",
                "end",
                values=aluno
            )

    # ========================================================
    # SELECIONAR ALUNO
    # ========================================================

    def selecionar_aluno(event):

        selecionado = tabela.selection()

        if not selecionado:
            return

        valores = tabela.item(
            selecionado[0],
            "values"
        )

        id_aluno = valores[0]

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                nome,
                data_nascimento,
                telefone,
                email,
                nivel,
                turma,
                tipo_ukulele,
                contribuicao
            FROM alunos
            WHERE id = ?
        """, (id_aluno,))

        aluno = cursor.fetchone()

        conn.close()

        if aluno:

            id_selecionado.set(aluno[0])
            nome_var.set(aluno[1])
            nascimento_var.set(aluno[2] or "")
            telefone_var.set(aluno[3] or "")
            email_var.set(aluno[4] or "")
            nivel_var.set(aluno[5] or "Iniciante")
            turma_var.set(aluno[6] or "UKE-01")
            ukulele_var.set(aluno[7] or "Soprano")
            contribuicao_var.set(
                aluno[8] or "Coletiva"
            )

    tabela.bind(
    "<<TreeviewSelect>>",
    selecionar_aluno
    )

    pesquisa_var.trace_add(
        "write",
        lambda *args: carregar_alunos()
    )

    turma_filtro_var.trace_add(
    "write",
    lambda *args: carregar_alunos()
    )

    nivel_filtro_var.trace_add(
        "write",
        lambda *args: carregar_alunos()
    )

    ukulele_filtro_var.trace_add(
        "write",
        lambda *args: carregar_alunos()
    )

    contribuicao_filtro_var.trace_add(
        "write",
        lambda *args: carregar_alunos()
    )

    carregar_alunos()

    entrada_nome.focus()


# ============================================================
# INICIALIZAÇÃO
# ============================================================

criar_bd()

tela_login()

centralizar_janela()

root.mainloop()