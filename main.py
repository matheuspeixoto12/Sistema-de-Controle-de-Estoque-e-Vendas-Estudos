import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

from cadastrar_produto import cadastrar_produto
from entrada_produto import entrada_produto
from registrar_venda import registrar_venda
from consultar_estoque import consultar_estoque
from gerar_relatorio import gerar_relatorio_vendas
from gerar_relatorio_movimentacoes import gerar_relatorio_movimentacoes

def carregar_icone(url, tamanho=(30, 30)):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(tamanho)
    return ImageTk.PhotoImage(img)

def main():
    janela = tb.Window(themename="flatly")
    janela.title("Sistema de Vendas e Estoque - Graal")
    janela.geometry("1020x420")
    janela.configure(bg="#111e7a")

    logo_url = "https://playgrounds.com.br/wp-content/uploads/2017/11/logo-graal.png"
    logo_img = carregar_icone(logo_url, tamanho=(320, 210))

    logo_label = tb.Label(janela, image=logo_img, background="#111e7a")
    logo_label.pack(pady=1)

    titulo = tb.Label(
        janela, 
        text="Menu Principal", 
        font=("Arial", 22, "bold"), 
        foreground="#111e7a", 
        background="#d0e6f7"
    )
    titulo.pack(pady=1)

    icones = {
        "cadastrar": carregar_icone("https://cdn-icons-png.flaticon.com/512/1828/1828817.png"),
        "entrada": carregar_icone("https://cdn-icons-png.flaticon.com/512/709/709496.png"),
        "venda": carregar_icone("https://cdn-icons-png.flaticon.com/512/3159/3159066.png"),
        "estoque": carregar_icone("https://cdn-icons-png.flaticon.com/512/3514/3514516.png"),
        "relatorio": carregar_icone("https://cdn-icons-png.flaticon.com/512/2331/2331970.png"),
        "sair": carregar_icone("https://cdn-icons-png.flaticon.com/512/1828/1828665.png"),
    }

    def criar_botao(texto, comando, icone):
        frame = tb.Frame(janela, bootstyle="light")
        btn = tb.Button(
            frame, 
            text=texto, 
            width=25, 
            image=icone, 
            compound="left", 
            bootstyle=PRIMARY + OUTLINE,
            command=comando
        )
        btn.pack(side="left", padx=10)
        frame.pack(pady=10)

    criar_botao("Cadastrar Produto", cadastrar_produto, icones["cadastrar"])
    criar_botao("Entrada de Produto", entrada_produto, icones["entrada"])
    criar_botao("Registrar Venda", registrar_venda, icones["venda"])
    criar_botao("Consultar Estoque", consultar_estoque, icones["estoque"])
    criar_botao("Gerar Relatório de Vendas", gerar_relatorio_vendas, icones["relatorio"])
    criar_botao("Gerar Relatório de Movimentacoes", gerar_relatorio_movimentacoes, icones["relatorio"])
    criar_botao("Sair", janela.destroy, icones["sair"])

    janela.mainloop()

if __name__ == "__main__":
    main()
