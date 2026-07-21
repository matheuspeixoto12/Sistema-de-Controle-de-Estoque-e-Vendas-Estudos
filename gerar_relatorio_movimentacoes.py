import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, ttk
from db import conectar
from mysql.connector import Error

def gerar_relatorio_movimentacoes():
    try:
        con = conectar()
        cursor = con.cursor()

        sql = """
        SELECT m.id_movimentacao, p.nome, m.tipo, m.quantidade, m.data
        FROM movimentacao m
        LEFT JOIN produto p ON m.id_produto = p.id_produto
        ORDER BY m.data DESC
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()

    except Error as e:
        messagebox.showerror("Erro", f"Erro ao consultar relatório: {e}")
        return
    finally:
        if con:
            cursor.close()
            con.close()

    janela = tb.Toplevel()
    janela.title("Relatório de Movimentações")
    janela.geometry("800x500")
    janela.configure(bg="#111e7a")

    janela.update_idletasks()
    largura = 800
    altura = 500
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    titulo = tb.Label(
        janela,
        text="Relatório de Movimentações",
        font=("Arial", 18, "bold"),
        foreground="#d0e6f7",
        background="#111e7a"
    )
    titulo.pack(pady=10)

    # Criar Treeview para mostrar os dados
    colunas = ("id_movimentacao", "produto", "tipo", "quantidade", "data")
    tree = ttk.Treeview(janela, columns=colunas, show="headings", height=15)

    # Definir os títulos das colunas
    tree.heading("id_movimentacao", text="ID")
    tree.heading("produto", text="Produto")
    tree.heading("tipo", text="Tipo")
    tree.heading("quantidade", text="Quantidade")
    tree.heading("data", text="Data")

    # Definir a largura das colunas
    tree.column("id_movimentacao", width=50, anchor="center")
    tree.column("produto", width=200)
    tree.column("tipo", width=100, anchor="center")
    tree.column("quantidade", width=100, anchor="center")
    tree.column("data", width=150, anchor="center")

    # Inserir os dados no Treeview
    for linha in resultados:
        id_movimentacao, produto, tipo, quantidade, data = linha
        tree.insert(
            "",
            "end",
            values=(
                id_movimentacao,
                produto,
                tipo,
                quantidade,
                data.strftime("%d/%m/%Y %H:%M:%S") if data else ""
            )
        )

    tree.pack(padx=10, pady=10, fill="both", expand=True)

    # Scrollbar vertical para a tabela
    scrollbar = ttk.Scrollbar(janela, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
