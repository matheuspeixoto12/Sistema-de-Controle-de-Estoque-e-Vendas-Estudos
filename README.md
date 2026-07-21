# 📦 Sistema de Controle de Estoque e Vendas - Projeto Graal

## 📖 Sobre o projeto

Este projeto foi desenvolvido como trabalho acadêmico com o objetivo de criar um sistema de gerenciamento de estoque e vendas para uma franquia da rede Graal.

O sistema permite controlar produtos, movimentações de estoque e vendas de maneira simples, utilizando uma interface gráfica desenvolvida em Python.

---

## 🚀 Funcionalidades

- ✅ Cadastro de produtos
- ✅ Consulta de produtos
- ✅ Entrada de produtos no estoque
- ✅ Registro de vendas
- ✅ Controle automático do estoque
- ✅ Relatório de movimentações
- ✅ Relatório de vendas

---

## 🛠 Tecnologias utilizadas

- Python
- Tkinter
- ttkbootstrap
- MySQL
- MySQL Connector
- Modelagem DER/MER

---

## 📂 Estrutura do projeto

```
Projeto/
│
├── cadastrar_produto.py
├── consultar_estoque.py
├── entrada_produto.py
├── registrar_venda.py
├── gerar_relatorio.py
├── gerar_relatorio_movimentacoes.py
├── db.py
├── main.py
│
├── logo-graal.png
├── programming.png
│
├── build/
├── dist/
└── README.md
```

---

## 🗄 Banco de Dados

O sistema utiliza o MySQL para armazenamento das informações.

Principais tabelas:

- Produto
- Movimentação
- Vendas
- Relatórios

Relacionamentos:

- Produto → Vendas (1:N)
- Produto → Movimentações (1:N)
- Vendas → Relatórios (1:1)

---

## 💻 Como executar

### 1 - Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/Estudos.git
```

### 2 - Entre na pasta

```bash
cd Estudos
```

### 3 - Instale as dependências

```bash
pip install ttkbootstrap
pip install mysql-connector-python
```

### 4 - Configure o banco de dados

Altere as informações de conexão no arquivo:

```
db.py
```

informando:

- Host
- Usuário
- Senha
- Banco de dados

### 5 - Execute

```bash
python main.py
```

---

## 📸 Imagens

Você pode adicionar aqui algumas imagens do sistema.

Exemplo:

```
/imagens/tela-principal.png
/imagens/cadastro-produto.png
```

---

## 📚 Aprendizados

Durante o desenvolvimento deste projeto foram aplicados conhecimentos em:

- Programação em Python
- Interface gráfica com Tkinter
- Integração com banco de dados MySQL
- CRUD
- Modelagem de banco de dados
- Controle de estoque
- Relatórios
- Organização de projetos

---

## 👨‍💻 Desenvolvido por

**Matheus Simões**

Projeto desenvolvido para fins acadêmicos e como parte do aprendizado em Desenvolvimento de Sistemas.
