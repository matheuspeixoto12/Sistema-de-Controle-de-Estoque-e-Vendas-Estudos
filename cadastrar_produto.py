import ttkbootstrap as tb
from tkinter import messagebox
from db import conectar
from mysql.connector import Error
from ttkbootstrap.constants import SUCCESS, OUTLINE

def cadastrar_produto():
    def salvar():
        nome = entry_nome.get().strip()
        descricao = entry_descricao.get().strip()
        preco = entry_preco.get().strip()
        estoque = entry_estoque.get().strip()

        # Valida campos obrigatórios
        if not nome:
            messagebox.showerror("Erro", "O campo Nome é obrigatório!")
            entry_nome.focus_set()
            return
        if not preco:
            messagebox.showerror("Erro", "O campo Preço é obrigatório!")
            entry_preco.focus_set()
            return
        if not estoque:
            messagebox.showerror("Erro", "O campo Estoque é obrigatório!")
            entry_estoque.focus_set()
            return

        # Valida tipos numéricos e valores lógicos
        try:
            preco_float = float(preco)
            if preco_float < 0:
                raise ValueError("Preço não pode ser negativo.")
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número decimal positivo!")
            entry_preco.focus_set()
            return

        try:
            estoque_int = int(estoque)
            if estoque_int < 0:
                raise ValueError("Estoque não pode ser negativo.")
        except ValueError:
            messagebox.showerror("Erro", "Estoque deve ser um número inteiro positivo!")
            entry_estoque.focus_set()
            return

        # Conexão e inserção no banco com tratamento de exceção
        con = None
        cursor = None
        try:
            con = conectar()
            cursor = con.cursor()

            # Verificar se já existe produto com mesmo nome para evitar duplicidade 
            cursor.execute("SELECT id_produto FROM Produto WHERE nome = %s", (nome,))
            if cursor.fetchone():
                messagebox.showerror("Erro", "Já existe um produto com esse nome cadastrado.")
                return

            # Insere o produto na tabela Produto
            sql_produto = "INSERT INTO Produto (nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s)"
            valores_produto = (nome, descricao, preco_float, estoque_int)
            cursor.execute(sql_produto, valores_produto)
            con.commit()

            # Pega o id do produto recém inserido
            id_produto = cursor.lastrowid

            # Insere a movimentação de cadastro na tabela movimentacao
            sql_movimentacao = "INSERT INTO movimentacao (id_produto, tipo, quantidade) VALUES (%s, %s, %s)"
            valores_movimentacao = (id_produto, 'cadastro', estoque_int)
            cursor.execute(sql_movimentacao, valores_movimentacao)
            con.commit()

            messagebox.showinfo("Sucesso", "Produto cadastrado e movimentação registrada com sucesso!")
            janela.destroy()  # Fecha a janela após salvar

        except Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto no banco de dados:\n{e}")

        except Exception as e:
            messagebox.showerror("Erro inesperado", f"Ocorreu um erro inesperado:\n{e}")

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

    # Cria janela filha (Toplevel)
    janela = tb.Toplevel()
    janela.title("Cadastrar Produto")
    janela.geometry("400x400")
    janela.configure(bg="#111e7a")

    # Centralizar janela
    janela.update_idletasks()
    largura, altura = 400, 400
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    # Título
    titulo = tb.Label(
        janela,
        text="Cadastro de Produto",
        font=("Arial", 18, "bold"),
        foreground="#d0e6f7",
        background="#111e7a"
    )
    titulo.pack(pady=20)

    estilo_label = {"font": ("Arial", 12), "foreground": "#d0e6f7", "background": "#111e7a"}

    tb.Label(janela, text="Nome:", **estilo_label).pack(pady=5)
    entry_nome = tb.Entry(janela, width=30)
    entry_nome.pack()

    tb.Label(janela, text="Descrição:", **estilo_label).pack(pady=5)
    entry_descricao = tb.Entry(janela, width=30)
    entry_descricao.pack()

    tb.Label(janela, text="Preço:", **estilo_label).pack(pady=5)
    entry_preco = tb.Entry(janela, width=30)
    entry_preco.pack()

    tb.Label(janela, text="Estoque:", **estilo_label).pack(pady=5)
    entry_estoque = tb.Entry(janela, width=30)
    entry_estoque.pack()

    botao_salvar = tb.Button(
        janela,
        text="Salvar",
        bootstyle=SUCCESS + OUTLINE,
        width=20,
        command=salvar
    )
    botao_salvar.pack(pady=20)

    # Focar no campo nome quando abrir a janela
    entry_nome.focus_set()
