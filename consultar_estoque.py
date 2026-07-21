import ttkbootstrap as tb
from tkinter import messagebox, ttk
from db import conectar
from mysql.connector import Error

def consultar_estoque():
    # Função para carregar dados do banco e preencher a tabela
    def carregar_dados():
        for item in tree.get_children():
            tree.delete(item)

        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("SELECT nome, descricao, preco, estoque FROM Produto")
            produtos = cursor.fetchall()
            for produto in produtos:
                nome, descricao, preco, estoque = produto
                # Aqui, no lugar do preço mostramos o estoque
                tree.insert("", "end", values=(nome, descricao, estoque))
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao consultar estoque: {e}")
        finally:
            if con:
                cursor.close()
                con.close()

    # Criar janela filha
    janela = tb.Toplevel()
    janela.title("Consultar Estoque")
    janela.geometry("700x500")
    janela.configure(bg="#111e7a")

    # Centralizar janela
    janela.update_idletasks()
    largura, altura = 700, 500
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    # Título
    titulo = tb.Label(
        janela,
        text="Estoque de Produtos",
        font=("Arial", 18, "bold"),
        foreground="#d0e6f7",
        background="#111e7a"
    )
    titulo.pack(pady=15)

    frame_tabela = tb.Frame(janela)
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

    # Colunas da tabela
    colunas = ("Nome", "Descrição", "Quantidade")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
    tree.pack(side="left", fill="both", expand=True)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    scrollbar = tb.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    botao_atualizar = tb.Button(janela, text="Atualizar", bootstyle="info", command=carregar_dados)
    botao_atualizar.pack(pady=10)

    carregar_dados()
