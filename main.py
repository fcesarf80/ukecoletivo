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
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# JANELA
# ============================================================

root = tk.Tk()

root.title("UkeColetivo - Login")
root.geometry("1000x650")
root.minsize(900, 600)

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
    rowheight=28,
    font=("Segoe UI", 9)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 9, "bold")
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

    # --------------------------------------------------------
    # CABEÇALHO
    # --------------------------------------------------------

    cabecalho = tk.Frame(
        root,
        bg="#174d2b",
        height=65
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

    # --------------------------------------------------------
    # ÁREA PRINCIPAL
    # --------------------------------------------------------

    principal = tk.Frame(
        root,
        bg="#f4f6f5"
    )

    principal.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    # --------------------------------------------------------
    # FORMULÁRIO
    # --------------------------------------------------------

    frame_form = tk.LabelFrame(
        principal,
        text="Dados do aluno",
        font=("Segoe UI", 10, "bold"),
        bg="#f4f6f5",
        padx=12,
        pady=10
    )

    frame_form.pack(
        fill="x"
    )

    # --------------------------------------------------------
    # VARIÁVEIS
    # --------------------------------------------------------

    id_selecionado = tk.StringVar()

    nome_var = tk.StringVar()
    nascimento_var = tk.StringVar()
    telefone_var = tk.StringVar()
    email_var = tk.StringVar()
    nivel_var = tk.StringVar(value="Iniciante")
    turma_var = tk.StringVar(value="UKE-01")
    ukulele_var = tk.StringVar(value="Soprano")
    contribuicao_var = tk.StringVar(value="Ideal")

    # --------------------------------------------------------
    # LINHA 1
    # --------------------------------------------------------

    tk.Label(
        frame_form,
        text="Nome:",
        bg="#f4f6f5"
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=5,
        pady=5
    )

    entrada_nome = ttk.Entry(
        frame_form,
        textvariable=nome_var,
        width=30
    )

    entrada_nome.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

    tk.Label(
        frame_form,
        text="Nascimento:",
        bg="#f4f6f5"
    ).grid(
        row=0,
        column=2,
        sticky="w",
        padx=5
    )

    ttk.Entry(
        frame_form,
        textvariable=nascimento_var,
        width=18
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    # --------------------------------------------------------
    # LINHA 2
    # --------------------------------------------------------

    tk.Label(
        frame_form,
        text="Telefone:",
        bg="#f4f6f5"
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=5,
        pady=5
    )

    ttk.Entry(
        frame_form,
        textvariable=telefone_var,
        width=30
    ).grid(
        row=1,
        column=1,
        padx=5
    )

    tk.Label(
        frame_form,
        text="E-mail:",
        bg="#f4f6f5"
    ).grid(
        row=1,
        column=2,
        sticky="w",
        padx=5
    )

    ttk.Entry(
        frame_form,
        textvariable=email_var,
        width=25
    ).grid(
        row=1,
        column=3,
        padx=5
    )

    # --------------------------------------------------------
    # LINHA 3
    # --------------------------------------------------------

    tk.Label(
        frame_form,
        text="Nível:",
        bg="#f4f6f5"
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=5,
        pady=5
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
        width=27
    )

    combo_nivel.grid(
        row=2,
        column=1,
        padx=5
    )

    tk.Label(
        frame_form,
        text="Turma:",
        bg="#f4f6f5"
    ).grid(
        row=2,
        column=2,
        sticky="w",
        padx=5
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
        width=22
    )

    combo_turma.grid(
        row=2,
        column=3,
        padx=5
    )

    # --------------------------------------------------------
    # LINHA 4
    # --------------------------------------------------------

    tk.Label(
        frame_form,
        text="Ukulele:",
        bg="#f4f6f5"
    ).grid(
        row=3,
        column=0,
        sticky="w",
        padx=5,
        pady=5
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
        width=27
    )

    combo_ukulele.grid(
        row=3,
        column=1,
        padx=5
    )

    tk.Label(
        frame_form,
        text="Contribuição:",
        bg="#f4f6f5"
    ).grid(
        row=3,
        column=2,
        sticky="w",
        padx=5
    )

    combo_contribuicao = ttk.Combobox(
        frame_form,
        textvariable=contribuicao_var,
        values=[
            "Social",
            "Ideal",
            "Sustentadora"
        ],
        state="readonly",
        width=22
    )

    combo_contribuicao.grid(
        row=3,
        column=3,
        padx=5
    )

    # --------------------------------------------------------
    # FUNÇÃO LIMPAR
    # --------------------------------------------------------

    def limpar_formulario():

        id_selecionado.set("")
        nome_var.set("")
        nascimento_var.set("")
        telefone_var.set("")
        email_var.set("")
        nivel_var.set("Iniciante")
        turma_var.set("UKE-01")
        ukulele_var.set("Soprano")
        contribuicao_var.set("Ideal")

        tabela.selection_remove(
            tabela.selection()
        )

        entrada_nome.focus()

    # --------------------------------------------------------
    # CADASTRAR
    # --------------------------------------------------------

    def cadastrar():

        nome = nome_var.get().strip()

        if not nome:

            messagebox.showwarning(
                "Atenção",
                "Informe o nome do aluno."
            )

            entrada_nome.focus()

            return

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

    # --------------------------------------------------------
    # ALTERAR
    # --------------------------------------------------------

    def alterar():

        id_aluno = id_selecionado.get()

        if not id_aluno:

            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno para alterar."
            )

            return

        nome = nome_var.get().strip()

        if not nome:

            messagebox.showwarning(
                "Atenção",
                "Informe o nome do aluno."
            )

            return

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

    # --------------------------------------------------------
    # EXCLUIR
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # BOTÕES
    # --------------------------------------------------------

    frame_botoes = tk.Frame(
        principal,
        bg="#f4f6f5"
    )

    frame_botoes.pack(
        fill="x",
        pady=10
    )

    ttk.Button(
        frame_botoes,
        text="Cadastrar",
        style="Acao.TButton",
        command=cadastrar
    ).pack(
        side="left",
        padx=4
    )

    ttk.Button(
        frame_botoes,
        text="Alterar",
        style="Acao.TButton",
        command=alterar
    ).pack(
        side="left",
        padx=4
    )

    ttk.Button(
        frame_botoes,
        text="Excluir",
        style="Acao.TButton",
        command=excluir
    ).pack(
        side="left",
        padx=4
    )

    ttk.Button(
        frame_botoes,
        text="Limpar",
        command=limpar_formulario
    ).pack(
        side="left",
        padx=4
    )

    # --------------------------------------------------------
    # PESQUISA
    # --------------------------------------------------------

    frame_pesquisa = tk.Frame(
        principal,
        bg="#f4f6f5"
    )

    frame_pesquisa.pack(
        fill="x",
        pady=(5, 10)
    )

    tk.Label(
        frame_pesquisa,
        text="Pesquisar:",
        bg="#f4f6f5",
        font=("Segoe UI", 10, "bold")
    ).pack(
        side="left",
        padx=(0, 8)
    )

    pesquisa_var = tk.StringVar()

    entrada_pesquisa = ttk.Entry(
        frame_pesquisa,
        textvariable=pesquisa_var,
        width=35
    )

    entrada_pesquisa.pack(
        side="left"
    )

    # --------------------------------------------------------
    # TABELA
    # --------------------------------------------------------

    frame_tabela = tk.Frame(
        principal,
        bg="#f4f6f5"
    )

    frame_tabela.pack(
        fill="both",
        expand=True
    )

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
        show="headings"
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
        width=50,
        anchor="center"
    )

    tabela.column(
        "nome",
        width=220
    )

    tabela.column(
        "turma",
        width=90,
        anchor="center"
    )

    tabela.column(
        "nivel",
        width=120,
        anchor="center"
    )

    tabela.column(
        "ukulele",
        width=110,
        anchor="center"
    )

    tabela.column(
        "contribuicao",
        width=130,
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

    # --------------------------------------------------------
    # CARREGAR ALUNOS
    # --------------------------------------------------------

    def carregar_alunos():

        termo = pesquisa_var.get().strip()

        conn = conectar_bd()
        cursor = conn.cursor()

        if termo:

            cursor.execute("""
                SELECT
                    id,
                    nome,
                    turma,
                    nivel,
                    tipo_ukulele,
                    contribuicao
                FROM alunos
                WHERE nome LIKE ?
                   OR email LIKE ?
                   OR telefone LIKE ?
                ORDER BY nome
            """, (
                f"%{termo}%",
                f"%{termo}%",
                f"%{termo}%"
            ))

        else:

            cursor.execute("""
                SELECT
                    id,
                    nome,
                    turma,
                    nivel,
                    tipo_ukulele,
                    contribuicao
                FROM alunos
                ORDER BY nome
            """)

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

    # --------------------------------------------------------
    # SELECIONAR ALUNO
    # --------------------------------------------------------

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
                aluno[8] or "Ideal"
            )

    tabela.bind(
        "<<TreeviewSelect>>",
        selecionar_aluno
    )

    pesquisa_var.trace_add(
        "write",
        lambda *args: carregar_alunos()
    )

    carregar_alunos()


# ============================================================
# INICIALIZAÇÃO
# ============================================================

criar_bd()

tela_login()

centralizar_janela()

root.mainloop()