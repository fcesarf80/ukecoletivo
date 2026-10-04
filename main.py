import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import os


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
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ============================================================
# JANELA PRINCIPAL
# ============================================================

root = tk.Tk()
root.title("UkeColetivo - Login")
root.geometry("900x600")
root.minsize(800, 550)

if os.path.exists(CAMINHO_ICONE):
    root.iconbitmap(CAMINHO_ICONE)


# ============================================================
# ESTILO
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "Titulo.TLabel",
    font=("Segoe UI", 25, "bold")
)

style.configure(
    "Subtitulo.TLabel",
    font=("Segoe UI", 11)
)

style.configure(
    "Campo.TLabel",
    font=("Segoe UI", 10)
)

style.configure(
    "Acao.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=10
)


# ============================================================
# FUNÇÕES AUXILIARES
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

    root.geometry(f"{largura}x{altura}+{x}+{y}")


# ============================================================
# TELA DE LOGIN
# ============================================================

def tela_login():

    limpar_tela()

    root.title("UkeColetivo - Login")

    # --------------------------------------------------------
    # Container principal
    # --------------------------------------------------------

    frame_principal = tk.Frame(root, bg="white")
    frame_principal.pack(fill="both", expand=True)

    # --------------------------------------------------------
    # Lado esquerdo - imagem
    # --------------------------------------------------------

    frame_imagem = tk.Frame(
        frame_principal,
        bg="#f5f5f5",
        width=400
    )

    frame_imagem.pack(
        side="left",
        fill="both",
        expand=True
    )

    frame_imagem.pack_propagate(False)

    if os.path.exists(CAMINHO_BG):

        imagem = tk.PhotoImage(file=CAMINHO_BG)

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
            text="UkeColetivo\n\nAprenda\nToque\nCompartilhe",
            font=("Segoe UI", 24, "bold"),
            fg="#174d2b",
            bg="#f5f5f5",
            justify="center"
        ).pack(
            expand=True
        )

    # --------------------------------------------------------
    # Lado direito - login
    # --------------------------------------------------------

    frame_login = tk.Frame(
        frame_principal,
        bg="white",
        padx=45
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
    ).pack(pady=(65, 5))

    tk.Label(
        frame_login,
        text="Música que aproxima",
        font=("Segoe UI", 12),
        fg="#555555",
        bg="white"
    ).pack(pady=(0, 35))

    # --------------------------------------------------------
    # E-mail
    # --------------------------------------------------------

    tk.Label(
        frame_login,
        text="E-mail",
        font=("Segoe UI", 10),
        fg="#333333",
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

    # --------------------------------------------------------
    # Password
    # --------------------------------------------------------

    tk.Label(
        frame_login,
        text="Password",
        font=("Segoe UI", 10),
        fg="#333333",
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

    # --------------------------------------------------------
    # Login
    # --------------------------------------------------------

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

        cursor.execute(
            """
            SELECT id, nome
            FROM utilizadores
            WHERE email = ? AND password = ?
            """,
            (email, criar_hash(password))
        )

        utilizador = cursor.fetchone()

        conn.close()

        if utilizador:

            messagebox.showinfo(
                "Sucesso",
                f"Bem-vindo(a), {utilizador[1]}!"
            )

            tela_principal(utilizador)

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
        pady=(0, 20)
    )

    # --------------------------------------------------------
    # Criar conta
    # --------------------------------------------------------

    ttk.Button(
        frame_login,
        text="Criar conta",
        command=tela_cadastro
    ).pack(
        fill="x"
    )

    entrada_email.focus()

    root.bind(
        "<Return>",
        lambda event: fazer_login()
    )


# ============================================================
# TELA DE CADASTRO
# ============================================================

def tela_cadastro():

    limpar_tela()

    root.title("UkeColetivo - Criar conta")

    frame = tk.Frame(
        root,
        bg="white",
        padx=80,
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
    ).pack(pady=(10, 5))

    tk.Label(
        frame,
        text="Cadastre-se para acessar o UkeColetivo",
        font=("Segoe UI", 11),
        fg="#555555",
        bg="white"
    ).pack(pady=(0, 30))

    # --------------------------------------------------------
    # Nome
    # --------------------------------------------------------

    tk.Label(
        frame,
        text="Nome completo",
        bg="white",
        anchor="w"
    ).pack(fill="x")

    entrada_nome = ttk.Entry(frame)
    entrada_nome.pack(
        fill="x",
        ipady=7,
        pady=(5, 15)
    )

    # --------------------------------------------------------
    # E-mail
    # --------------------------------------------------------

    tk.Label(
        frame,
        text="E-mail",
        bg="white",
        anchor="w"
    ).pack(fill="x")

    entrada_email = ttk.Entry(frame)
    entrada_email.pack(
        fill="x",
        ipady=7,
        pady=(5, 15)
    )

    # --------------------------------------------------------
    # Password
    # --------------------------------------------------------

    tk.Label(
        frame,
        text="Password",
        bg="white",
        anchor="w"
    ).pack(fill="x")

    entrada_password = ttk.Entry(
        frame,
        show="•"
    )

    entrada_password.pack(
        fill="x",
        ipady=7,
        pady=(5, 15)
    )

    # --------------------------------------------------------
    # Confirmar password
    # --------------------------------------------------------

    tk.Label(
        frame,
        text="Confirmar password",
        bg="white",
        anchor="w"
    ).pack(fill="x")

    entrada_confirmar = ttk.Entry(
        frame,
        show="•"
    )

    entrada_confirmar.pack(
        fill="x",
        ipady=7,
        pady=(5, 25)
    )

    # --------------------------------------------------------
    # Registo
    # --------------------------------------------------------

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

            cursor.execute(
                """
                INSERT INTO utilizadores
                (nome, email, password)
                VALUES (?, ?, ?)
                """,
                (
                    nome,
                    email,
                    criar_hash(password)
                )
            )

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
    ).pack(
        fill="x"
    )

    entrada_nome.focus()


# ============================================================
# TELA PRINCIPAL
# ============================================================

def tela_principal(utilizador):

    limpar_tela()

    root.title("UkeColetivo - Gestão de Alunos")

    frame = tk.Frame(
        root,
        bg="white"
    )

    frame.pack(
        fill="both",
        expand=True
    )

    # --------------------------------------------------------
    # Cabeçalho
    # --------------------------------------------------------

    cabecalho = tk.Frame(
        frame,
        bg="#174d2b",
        height=70
    )

    cabecalho.pack(
        fill="x"
    )

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
        side="right",
        padx=25
    )

    # --------------------------------------------------------
    # Conteúdo
    # --------------------------------------------------------

    conteudo = tk.Frame(
        frame,
        bg="white",
        padx=40,
        pady=40
    )

    conteudo.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        conteudo,
        text="Gestão de Alunos",
        font=("Segoe UI", 24, "bold"),
        fg="#174d2b",
        bg="white"
    ).pack(pady=(40, 10))

    tk.Label(
        conteudo,
        text="Área principal do UkeColetivo",
        font=("Segoe UI", 12),
        fg="#666666",
        bg="white"
    ).pack()

    messagebox.showinfo(
        "Login efetuado",
        "Acesso à área principal realizado com sucesso."
    )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

criar_bd()

tela_login()

centralizar_janela()

root.mainloop()