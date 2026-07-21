import ttkbootstrap as tb
from tkinter import messagebox
from db import conectar
from mysql.connector import Error

def entrada_produto():
    def carregar_produtos():
        con = None
        cursor = None
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("SELECT id_produto, nome, estoque FROM Produto")
            produtos = cursor.fetchall()
            if not produtos:
                messagebox.showwarning("Aviso", "Nenhum produto cadastrado.")
            return produtos
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

    def salvar_entrada():
        # Verifica se algum produto foi carregado
        if not produtos:
            messagebox.showerror("Erro", "Nenhum produto disponível para selecionar.")
            return

        idx = combo_produto.current()
        if idx == -1:
            messagebox.showerror("Erro", "Selecione um produto.")
            return

        qtd_text = entry_quantidade.get().strip()
        if not qtd_text.isdigit():
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo.")
            return
        
        qtd = int(qtd_text)
        if qtd <= 0:
            messagebox.showerror("Erro", "Quantidade deve ser maior que zero.")
            return

        produto_id, nome, estoque_atual = produtos[idx]

        con = None
        cursor = None
        try:
            con = conectar()
            cursor = con.cursor()

            # Atualizar estoque somando a quantidade entrada
            sql_update = "UPDATE Produto SET estoque = estoque + %s WHERE id_produto = %s"
            cursor.execute(sql_update, (qtd, produto_id))

            # Registrar movimentação do tipo 'entrada'
            sql_mov = "INSERT INTO Movimentacao (id_produto, tipo, quantidade) VALUES (%s, %s, %s)"
            cursor.execute(sql_mov, (produto_id, 'entrada', qtd))

            con.commit()
            messagebox.showinfo("Sucesso", f"Entrada de {qtd} unidades do produto '{nome}' registrada com sucesso!")
            janela.destroy()
        except Error as e:
            if con:
                con.rollback()
            messagebox.showerror("Erro", f"Erro ao registrar entrada: {e}")
        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

    janela = tb.Toplevel()
    janela.title("Entrada de Produto")
    janela.geometry("400x300")
    janela.configure(bg="#111e7a")

    # Centralizar janela
    janela.update_idletasks()
    largura, altura = 400, 300
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    titulo = tb.Label(
        janela,
        text="Registrar Entrada de Produto",
        font=("Arial", 18, "bold"),
        foreground="#d0e6f7",
        background="#111e7a"
    )
    titulo.pack(pady=15)

    produtos = carregar_produtos()
    nomes_produtos = [p[1] for p in produtos]

    tb.Label(janela, text="Produto:", font=("Arial", 12), foreground="#d0e6f7", background="#111e7a").pack(pady=5)
    combo_produto = tb.Combobox(janela, values=nomes_produtos, state="readonly", width=30)
    combo_produto.pack()

    tb.Label(janela, text="Quantidade:", font=("Arial", 12), foreground="#d0e6f7", background="#111e7a").pack(pady=5)
    entry_quantidade = tb.Entry(janela, width=30)
    entry_quantidade.pack()

    botao_salvar = tb.Button(janela, text="Registrar Entrada", bootstyle="success", width=20, command=salvar_entrada)
    botao_salvar.pack(pady=20)
