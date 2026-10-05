# 🎵 UkeColetivo

## UC00618 --- Criar aplicações em linguagem de programação Python

### Projeto de Avaliação

Aplicação desktop desenvolvida em **Python + Tkinter**, com **SQLite**,
para apoio à gestão de alunos de uma escola virtual e presencial de
ukulele.

------------------------------------------------------------------------

## 1. Curso

**Curso/Ação:**\
\[CET.TPSI.N.P.32\] Técnico/a Especialista em Tecnologias e Programação
de Sistemas de Informação

**Unidade de Formação:**\
UC00618 --- Criar aplicações em linguagem de programação Python

**Formador:**\
JULIO GUILHERME MOURA MAGALHAES

**Tecnologias utilizadas:** - Python - Tkinter - SQLite - `sqlite3` -
`hashlib` - `re`

**Projeto:** UkeColetivo

------------------------------------------------------------------------

## 2. Propósito

O **UkeColetivo** é uma aplicação desktop criada para demonstrar, de
forma simples e funcional, os principais conceitos trabalhados na
UC00618.

A aplicação permite o acesso de utilizadores e a gestão dos alunos de
uma escola de ukulele, incluindo cadastro, pesquisa, filtros, alteração
e exclusão de registos.

O projeto foi desenvolvido com foco em simplicidade, organização,
facilidade de utilização, poucas telas, utilização de `messagebox` e
armazenamento local com SQLite.

------------------------------------------------------------------------

## 3. Origem do projeto

O UkeColetivo tem origem em um projeto real idealizado por **Pablo
Ferreira Farias**, professor de música, escritor e compositor, com
formação musical pela **Universidade Estadual do Ceará (UECE)** e
atualmente formando do **Curso de Direito da EstácioFIC**.

Ao longo de aproximadamente **30 anos de atuação**, Pablo participou e
ministrou aulas em diferentes projetos sociais ligados a instituições da
capital, municípios e ao Estado, além de ter desenvolvido atividades em
**clínica de musicoterapia**, incluindo trabalhos direcionados a um
público de maior poder aquisitivo.

A experiência acumulada nesses diferentes contextos contribuiu para a
construção de uma proposta que posteriormente tomou outro caminho: ao se
desvincular das atividades voltadas ao público de maior poder
aquisitivo, surgiu a decisão de desenvolver um trabalho **voluntário,
solidário e sem fins lucrativos**, tornando o ensino do ukulele mais
acessível.

O projeto disponibiliza instrumentos para alunos iniciantes e também
para pessoas que desejam simplesmente experimentar o ukulele antes de
adquirir um instrumento. As atividades podem ocorrer por meio de
orientação online e de encontros presenciais em espaços públicos.

As contribuições recebidas **não constituem remuneração ou lucro**. Os
valores arrecadados são destinados exclusivamente à manutenção dos
instrumentos e seus acessórios, à produção ou aquisição de materiais
didáticos, como apostilas, e, eventualmente, ao pagamento de taxas
relacionadas à utilização de determinados espaços públicos.

Dessa forma, o UkeColetivo procura unir **educação musical, convivência,
acesso à música e ação solidária**, mantendo uma estrutura simples e sem
finalidade lucrativa.

------------------------------------------------------------------------

## 4. Requisitos da aplicação

-   [x] Login de utilizador
-   [x] Cadastro de utilizador
-   [x] Password com mínimo de 6 caracteres
-   [x] Password armazenada por hash SHA-256
-   [x] SQLite como base de dados local
-   [x] Cadastro de alunos
-   [x] Alteração de alunos
-   [x] Exclusão de alunos
-   [x] Pesquisa de alunos
-   [x] Filtros por turma, nível, ukulele e contribuição
-   [x] Validação de dados
-   [x] Mensagens com `messagebox`
-   [x] Confirmação antes da exclusão
-   [x] Confirmação antes de sair

------------------------------------------------------------------------

## 5. Fluxo principal

``` text
Login
  │
  ├── Criar conta
  │
  └── Entrar
        │
        ▼
Gestão de Alunos
  │
  ├── Cadastrar
  ├── Alterar
  ├── Excluir
  ├── Pesquisar
  └── Filtrar
```

------------------------------------------------------------------------

## 6. Telas

### Login

A tela inicial apresenta a identidade visual do UkeColetivo, o slogan
**"Música que aproxima"**, os campos de E-mail e Password e os botões
**Entrar** e **Criar conta**.

### Cadastro de utilizador

Permite criar uma conta com nome completo, e-mail, password e
confirmação da password.

### Gestão de alunos

Permite registar e administrar:

-   Nome
-   Data de nascimento
-   Telefone
-   E-mail
-   Nível
-   Turma
-   Tipo de ukulele
-   Contribuição

Todas as telas utilizam a mesma janela principal.

------------------------------------------------------------------------

## 7. Pesquisa e filtros

A pesquisa permite localizar alunos por **nome, e-mail ou telefone**.

Os filtros podem ser combinados com a pesquisa:

-   Turma: UKE-01, UKE-02 ou UKE-03
-   Nível: Iniciante, Intermediário ou Avançado
-   Ukulele: Soprano, Concert, Tenor ou Barítono
-   Contribuição: Solidária, Coletiva ou Generosa

Os resultados são apresentados em uma `Treeview`.

------------------------------------------------------------------------

## 8. Validações

Antes do cadastro ou alteração de um aluno, a aplicação verifica:

-   nome obrigatório;
-   formato básico do e-mail;
-   telefone;
-   formato da data de nascimento;
-   existência da data;
-   impossibilidade de informar uma data de nascimento futura.

O sistema utiliza `messagebox` para apresentar os avisos e confirmações
ao utilizador.

------------------------------------------------------------------------

## 9. Base de dados

A aplicação utiliza um banco de dados **SQLite local**, armazenado em:

``` text
banco.db
```

### `utilizadores`

``` text
id
nome
email
password
```

### `alunos`

``` text
id
nome
data_nascimento
telefone
email
nivel
turma
tipo_ukulele
contribuicao
```

O ficheiro `banco.db` não é versionado no GitHub.

------------------------------------------------------------------------

## 10. Estrutura do projeto

``` text
UkeColetivo/
├── img/
│   ├── login-bg.png
│   ├── ukulele.png
│   └── icone.ico
├── main.py
├── .gitignore
└── README.md
```

O projeto mantém uma estrutura pequena, evitando ficheiros e classes
desnecessários.

------------------------------------------------------------------------

## 11. Tecnologias e conceitos demonstrados

-   Python
-   Tkinter
-   SQLite
-   CRUD
-   SQL
-   `messagebox`
-   `Treeview`
-   `Combobox`
-   funções
-   estruturas condicionais
-   validação de dados
-   expressões regulares
-   hash SHA-256
-   eventos do Tkinter

------------------------------------------------------------------------

## 12. Estado atual

**Projeto funcional e concluído para a etapa de avaliação da UC.**

As funcionalidades principais foram implementadas e testadas:

-   login;
-   criação de conta;
-   CRUD de alunos;
-   pesquisa;
-   filtros;
-   validações;
-   confirmação de exclusão;
-   confirmação de saída;
-   interface gráfica;
-   SQLite;
-   mensagens de feedback.

------------------------------------------------------------------------

## 13. Possível evolução

O projeto foi construído para poder servir posteriormente como base para
uma aplicação real mais completa.

Entre as possíveis evoluções estão:

-   gestão de encontros e aulas;
-   controlo de instrumentos;
-   materiais didáticos;
-   relatórios;
-   outras funcionalidades administrativas.

Essas funcionalidades não fazem parte da versão atual, preservando a
simplicidade do projeto desenvolvido para a UC.

------------------------------------------------------------------------

## 14. Princípio do projeto

> **"Música que aproxima."**

O UkeColetivo procura demonstrar que uma aplicação pode ser tecnicamente
simples, organizada e funcional, ao mesmo tempo em que representa uma
proposta de **educação musical, convivência, acesso à música e ação
solidária**.

------------------------------------------------------------------------

## Autor

**Fernando Cesar Ferreira Farias**

\[CET.TPSI.N.P.32\] Técnico/a Especialista em Tecnologias e Programação
de Sistemas de Informação\
**UC00618 --- Criar aplicações em linguagem de programação Python**
