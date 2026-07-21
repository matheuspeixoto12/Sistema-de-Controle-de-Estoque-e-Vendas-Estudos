import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from db import conectar  #

def registrar_venda():
    produto_selecionado = None
    carrinho = []

    def limpar_dados_produto():
        nonlocal produto_selecionado
        produto_selecionado = None
        label_nome.config(text="Nome: ")
        label_preco.config(text="Preço unitário: ")
        label_estoque.config(text="Estoque disponível: ")
        entry_quantidade.delete(0, "end")
        entry_quantidade.config(state="disabled")
        btn_adicionar.config(state="disabled")

    def atualizar_lista_carrinho():
        listbox_carrinho.delete(0, tk.END)
        for item in carrinho:
            listbox_carrinho.insert(
                tk.END,
                f"{item['nome']} - Qtde: {item['quantidade']} - Total: R$ {item['total']:.2f}"
            )

    def exibir_lista_produtos():
        con = None
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("SELECT id_produto, nome, preco, estoque FROM Produto")
            resultados = cursor.fetchall()

            if not resultados:
                messagebox.showinfo("Info", "Nenhum produto cadastrado.")
                return

            lista_nomes = [
                f"{r[1]} (R$ {r[2]:.2f}, Estoque: {r[3]})" for r in resultados
            ]

            sel_window = tk.Toplevel(root)
            sel_window.title("Selecionar Produto")

            lb = tk.Listbox(sel_window, width=50)
            lb.pack(padx=10, pady=10)

            for nome in lista_nomes:
                lb.insert(tk.END, nome)

            def selecionar():
                idx = lb.curselection()
                if not idx:
                    messagebox.showwarning("Atenção", "Selecione um produto.")
                    return
                r = resultados[idx[0]]
                preencher_dados_produto(r)
                sel_window.destroy()

            tk.Button(sel_window, text="Selecionar", command=selecionar).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar produtos: {e}")
        finally:
            if con:
                con.close()

    def preencher_dados_produto(resultado):
        nonlocal produto_selecionado
        produto_selecionado = {
            "id": resultado[0],
            "nome": resultado[1],
            "preco": resultado[2],
            "estoque": resultado[3]
        }
        label_nome.config(text=f"Nome: {produto_selecionado['nome']}")
        label_preco.config(text=f"Preço unitário: R$ {produto_selecionado['preco']:.2f}")
        label_estoque.config(text=f"Estoque disponível: {produto_selecionado['estoque']}")
        entry_quantidade.config(state="normal")
        btn_adicionar.config(state="normal")
        entry_quantidade.delete(0, "end")
        entry_quantidade.focus()

    def buscar_produto():
        termo = entry_pesquisa.get().strip()
        if not termo:
            exibir_lista_produtos()
            return

        con = None
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute(
                "SELECT id_produto, nome, preco, estoque FROM Produto WHERE nome LIKE %s",
                (f"%{termo}%",)
            )
            resultado = cursor.fetchone()
            if resultado:
                preencher_dados_produto(resultado)
            else:
                messagebox.showinfo("Não encontrado", "Produto não encontrado.")
                limpar_dados_produto()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar produto: {e}")
        finally:
            if con:
                con.close()

    def adicionar_ao_carrinho():
        nonlocal produto_selecionado, carrinho
        if not produto_selecionado:
            messagebox.showwarning("Atenção", "Pesquise um produto antes de adicionar.")
            return

        try:
            quantidade = int(entry_quantidade.get())
        except ValueError:
            messagebox.showwarning("Atenção", "Digite uma quantidade válida.")
            return

        if quantidade <= 0:
            messagebox.showwarning("Atenção", "Digite uma quantidade maior que zero.")
            return

        # Verifica estoque atualizado no banco
        con = None
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("SELECT estoque FROM Produto WHERE id_produto = %s", (produto_selecionado['id'],))
            estoque_atual = cursor.fetchone()
            if estoque_atual is None:
                messagebox.showerror("Erro", "Produto não encontrado no banco.")
                return
            estoque_atual = estoque_atual[0]
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar estoque: {e}")
            return
        finally:
            if con:
                con.close()

        # Verifica se quantidade é maior que estoque
        qtde_no_carrinho = 0
        for item in carrinho:
            if item['id'] == produto_selecionado['id']:
                qtde_no_carrinho = item['quantidade']
                break

        if quantidade + qtde_no_carrinho > estoque_atual:
            messagebox.showwarning(
                "Atenção",
                "Quantidade no carrinho maior que o estoque disponível."
            )
            return

        preco_unit = produto_selecionado['preco']
        total = preco_unit * quantidade

        # Atualiza ou adiciona no carrinho
        for item in carrinho:
            if item['id'] == produto_selecionado['id']:
                item['quantidade'] += quantidade
                item['total'] = item['preco_unit'] * item['quantidade']
                break
        else:
            carrinho.append({
                "id": produto_selecionado['id'],
                "nome": produto_selecionado['nome'],
                "quantidade": quantidade,
                "preco_unit": preco_unit,
                "total": total
            })

        atualizar_lista_carrinho()
        limpar_dados_produto()
        entry_pesquisa.delete(0, "end")
        entry_pesquisa.focus()

    def finalizar_venda():
        nonlocal carrinho
        if not carrinho:
            messagebox.showwarning("Atenção", "O carrinho está vazio.")
            return

        con = None
        try:
            con = conectar()
            cursor = con.cursor()
            data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for item in carrinho:
                cursor.execute(
                    "INSERT INTO Venda (id_produto, quantidade, preco_total, data) VALUES (%s, %s, %s, %s)",
                    (item['id'], item['quantidade'], item['total'], data_venda)
                )
                cursor.execute(
                    "UPDATE Produto SET estoque = estoque - %s WHERE id_produto = %s",
                    (item['quantidade'], item['id'])
                )
                cursor.execute(
                    "INSERT INTO Movimentacao (id_produto, tipo, quantidade) VALUES (%s, %s, %s)",
                    (item['id'], 'saida', item['quantidade'])
                )

            con.commit()
            messagebox.showinfo("Sucesso", "Venda finalizada e registrada com sucesso!")
            carrinho.clear()
            atualizar_lista_carrinho()
            limpar_dados_produto()
            entry_pesquisa.delete(0, "end")
            entry_pesquisa.focus()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar venda: {e}")
            if con:
                con.rollback()
        finally:
            if con:
                con.close()

    def limpar_carrinho():
        nonlocal carrinho
        if not carrinho:
            messagebox.showinfo("Info", "Carrinho já está vazio.")
            return
        if messagebox.askyesno("Confirmação", "Deseja limpar todo o carrinho?"):
            carrinho.clear()
            atualizar_lista_carrinho()

    # === Interface Gráfica ===
    root = tk.Tk()
    root.title("Registrar Venda")

    tk.Label(root, text="Nome do Produto:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_pesquisa = tk.Entry(root, width=40)
    entry_pesquisa.grid(row=0, column=1, padx=10, pady=10)
    entry_pesquisa.focus()
    entry_pesquisa.bind("<Return>", lambda event: buscar_produto())

    label_nome = tk.Label(root, text="Nome: ")
    label_nome.grid(row=1, column=0, columnspan=2, sticky="w", padx=10)

    label_preco = tk.Label(root, text="Preço unitário: ")
    label_preco.grid(row=2, column=0, columnspan=2, sticky="w", padx=10)

    label_estoque = tk.Label(root, text="Estoque disponível: ")
    label_estoque.grid(row=3, column=0, columnspan=2, sticky="w", padx=10)

    tk.Label(root, text="Quantidade:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    entry_quantidade = tk.Entry(root, width=10, state="disabled")
    entry_quantidade.grid(row=4, column=1, sticky="w")

    btn_adicionar = tk.Button(root, text="Adicionar ao Carrinho", state="disabled", command=adicionar_ao_carrinho)
    btn_adicionar.grid(row=5, column=0, columnspan=2, pady=10)

    listbox_carrinho = tk.Listbox(root, width=60)
    listbox_carrinho.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    btn_finalizar = tk.Button(root, text="Finalizar Venda", command=finalizar_venda)
    btn_finalizar.grid(row=7, column=0, pady=10)

    btn_limpar = tk.Button(root, text="Limpar Carrinho", command=limpar_carrinho)
    btn_limpar.grid(row=7, column=1, pady=10)

    root.mainloop()
