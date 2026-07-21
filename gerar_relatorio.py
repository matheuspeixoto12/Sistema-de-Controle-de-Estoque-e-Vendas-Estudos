import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, ttk
from db import conectar
from mysql.connector import Error

def gerar_relatorio_vendas():
    try:
        con = conectar()
        cursor = con.cursor()

        sql = """
        SELECT 
            v.id_venda,
            p.nome AS produto,
            v.quantidade,
            v.preco_total,
            v.data
        FROM venda v
        JOIN produto p ON v.id_produto = p.id_produto
        ORDER BY v.data DESC;
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()

        # Calcular totais
        total_quantidade = sum(row[2] for row in resultados)
        total_valor = sum(row[3] for row in resultados)

    except Error as e:
        messagebox.showerror("Erro", f"Erro ao consultar relatório: {e}")
        return
    finally:
        if con:
            cursor.close()
            con.close()

    janela = tb.Toplevel()
    janela.title("Relatório de Vendas")
    janela.geometry("750x600")
    janela.configure(bg="#111e7a")

    janela.update_idletasks()
    largura = 750
    altura = 600
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    titulo = tb.Label(
        janela,
        text="Relatório de Vendas",
        font=("Arial", 18, "bold"),
        foreground="#d0e6f7",
        background="#111e7a"
    )
    titulo.pack(pady=10)

    # Treeview
    colunas = ("id_venda", "produto", "quantidade", "total", "data")
    tree = ttk.Treeview(janela, columns=colunas, show="headings", height=20)

    tree.heading("id_venda", text="ID")
    tree.heading("produto", text="Produto")
    tree.heading("quantidade", text="Quantidade")
    tree.heading("total", text="Valor Total")
    tree.heading("data", text="Data da Venda")

    tree.column("id_venda", width=50, anchor="center")
    tree.column("produto", width=250)
    tree.column("quantidade", width=100, anchor="center")
    tree.column("total", width=120, anchor="e")
    tree.column("data", width=180, anchor="center")

    # Inserir dados
    for linha in resultados:
        id_venda, produto, quantidade, preco_total, data = linha
        tree.insert(
            "",
            "end",
            values=(
                id_venda,
                produto,
                quantidade,
                f"R$ {preco_total:.2f}",
                data.strftime("%d/%m/%Y %H:%M:%S") if data else ""
            )
        )
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(janela, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    rodape_frame = tb.Frame(janela, background="#0a1a4a")
    rodape_frame.pack(fill="x", padx=10, pady=(0, 20))

    label_quantidade = tb.Label(
        rodape_frame,
        text=f"Quantidade Total Vendida: {total_quantidade}",
        font=("Arial", 14, "bold"),
        foreground="#ffffff",
        background="#0a1a4a"
    )
    label_quantidade.pack(side="left", padx=10, pady=10)

    label_valor = tb.Label(
        rodape_frame,
        text=f"Valor Total Vendido: R$ {total_valor:.2f}",
        font=("Arial", 14, "bold"),
        foreground="#ffffff",
        background="#0a1a4a"
    )
    label_valor.pack(side="right", padx=10, pady=10)
