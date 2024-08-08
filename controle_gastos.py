import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import json #registra dados em um arquivo de dados
import os #cria um "dialogo" entre arquivos

# Configurando a janela (colocando nome, tamanho da janela e cor de fundo)
root = ThemedTk(theme="thinice")
root.title("Controle de gastos")
largura = 534
altura = 650
root.geometry(f'{largura}x{altura}')
root.configure(bg='#7eb7c7')

# Arquivo onde os dados serão salvos
arquivo_dados = "gastos.json"

# Função para carregar dados do arquivo
def carregar_dados():
    if os.path.exists(arquivo_dados):
        with open(arquivo_dados) as file:
            return json.load(file)
    return {"renda_mensal": 0, "despesas": [], "limite_gastos": 0}

# Função para salvar dados no arquivo
def salvar_dados():
    with open(arquivo_dados) as file:
        json.dump({"renda_mensal": renda_mensal, "despesas": despesas, "limite_gastos": limite_gastos}, file)

# Função para adicionar despesa à tabela de despesas
def add_despesa():
    categoria = categoria_entrada.get()
    valor = valor_entrada.get()
    data = data_entrada.get()

    if not categoria or not valor or not data:
        messagebox.showwarning("Input Error", "Todos os campos são obrigatórios")
        return

    try:
        valor = float(valor)
    except ValueError:
        messagebox.showwarning("Input Error", "Valor deve ser um número")
        return

    despesas.append((categoria, valor, data))
    update_tabela_despesa()
    limpar_entradas()
    status_label.config(text="Despesa adicionada com sucesso", fg="green")
    salvar_dados()

    
# Função para atualizar os dados da tabela
def update_tabela_despesa():
    for row in tabela_despesa.get_children():
        tabela_despesa.delete(row)

    total_despesa = 0
    for despesa in despesas:
        tabela_despesa.insert("", "end", values=despesa)
        total_despesa += despesa[1]

    total_despesa_label.config(text=f"Total de Gastos: R$ {total_despesa:.2f}")
    saldo_restante = renda_mensal - total_despesa
    saldo_restante_label.config(text=f"Saldo Restante: R$ {saldo_restante:.2f}")
    limite_gastos_label.config(text=f"Limite de Gastos: R$ {limite_gastos:.2f}")

# Função para limpar as caixas de entrada
def limpar_entradas():
    categoria_entrada.delete(0, tk.END)
    valor_entrada.delete(0, tk.END)
    data_entrada.delete(0, tk.END)

# Função para definir a renda mensal
def definir_renda():
    global renda_mensal
    renda = renda_entrada.get()

    if not renda:
        messagebox.showwarning("Input Error", "Todos os campos são obrigatórios")
        return

    try:
        renda_mensal = float(renda)
    except ValueError:
        messagebox.showwarning("Input Error", "Valor deve ser um número")
        return

    update_tabela_despesa()
    renda_entrada.delete(0, tk.END)
    status_label.config(text="Renda definida com sucesso", fg="green")
    salvar_dados()

# Função para abrir a janela de definição de limite de gastos
def abrir_definir_limite():
    def definir_limite_gastos():
        global limite_gastos
        limite = limite_entrada.get()

        if not limite:
            messagebox.showwarning("Input Error", "Todos os campos são obrigatórios")
            return

        try:
            limite_gastos = float(limite)
        except ValueError:
            messagebox.showwarning("Input Error", "Valor deve ser um número")
            return

        limite_entrada.delete(0, tk.END)
        status_label.config(text="Limite de gastos definido com -sucesso", fg="green")
        salvar_dados()
        update_tabela_despesa()
        janela_definir_limite.destroy()

# Criando a tela para definir limite de gasto
    janela_definir_limite = tk.Toplevel(root)
    janela_definir_limite.title("Definir Limite de Gastos")
    janela_definir_limite.geometry("300x150")
    janela_definir_limite.configure(bg='#7eb7c7')

# Onde vai aparecer o limite determinado
    tk.Label(janela_definir_limite, text="Limite de Gastos:", bg='#7eb7c7', font=("Calibri", 14, "bold"), fg="#00548b").pack(pady=10)
    limite_entrada = tk.Entry(janela_definir_limite)
    limite_entrada.pack(pady=10)

# Botão de definir limite
    tk.Button(janela_definir_limite, text="Definir Limite", command=definir_limite_gastos, bg='#00548b', fg="#cde8ff", font=("Calibri", 11, "bold"), highlightthickness=5, bd=0, relief="solid").pack(pady=10)

# Para ver se o limite de gastos foi atingido
    total_despesa = sum(despesa[1] for despesa in despesas)
    if total_despesa >= limite_gastos:
        messagebox.showwarning("Limite de Gastos Atingido", f"Você atingiu o limite de gastos de R$ {limite_gastos:.2f}")

# Carregar dados salvos
data = carregar_dados()
despesas = data["despesas"]
renda_mensal = data["renda_mensal"]
limite_gastos = data["limite_gastos"]

# Apagar tudo
def apagar_tudo():
    global renda_mensal, despesas, limite_gastos
    renda_mensal = 0
    despesas = []
    limite_gastos = 0
    update_tabela_despesa()
    salvar_dados()

# Labels e caixas de entrada
tk.Label(root, text="Renda Mensal:", bg='#7eb7c7', font=("Calibri", 14, "bold"), fg="#00548b").grid(row=0, column=0, padx=10, pady=10)
renda_entrada = tk.Entry(root)
renda_entrada.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Categoria:", bg='#7eb7c7', font=("Calibri", 14, "bold"), fg="#00548b").grid(row=1, column=0, padx=10, pady=10)
categoria_entrada = tk.Entry(root)
categoria_entrada.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Valor:", bg='#7eb7c7', font=("Calibri", 14, "bold"), fg="#00548b").grid(row=2, column=0, padx=10, pady=10)
valor_entrada = tk.Entry(root)
valor_entrada.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Data (DD-MM-AAAA):", bg='#7eb7c7', font=("Calibri", 14, "bold"), fg="#00548b").grid(row=3, column=0, padx=10, pady=10)
data_entrada = tk.Entry(root)
data_entrada.grid(row=3, column=1, padx=10, pady=10)

# Botão para definir a renda
renda_botao = tk.Button(root, text="Definir Renda", command=definir_renda, bg='#00548b', fg="#cde8ff", font=("Calibri", 11, "bold"), highlightthickness=5, bd=0, relief="solid")
renda_botao.grid(row=0, column=2, padx=10, pady=10)

# Botão para abrir a janela de definir o limite de gastos
limite_botao = tk.Button(root, text="Definir Limite de Gastos", command=abrir_definir_limite, bg='#00548b', fg="#cde8ff", font=("Calibri", 11, "bold"), highlightthickness=5, bd=0, relief="solid")
limite_botao.grid(row=6, column=2, padx=10, pady=10)

# Botão para adicionar despesa
add_botao = tk.Button(root, text="Adicionar Despesa", command=add_despesa, bg='#00548b', fg="#cde8ff", font=("Calibri", 11, "bold"), highlightthickness=5, bd=0, relief="solid")
add_botao.grid(row=1, column=2, columnspan=10, pady=10)

# Botão para apagar todos os dados
apagar_botao = tk.Button(root, text="Apagar Tudo", command=apagar_tudo, bg='#e74c3c', fg="#ffffff", font=("Calibri", 11, "bold"), highlightthickness=5, bd=0, relief="solid")
apagar_botao.grid(row=7, column=2, padx=10, pady=10)

# Tabela para mostrar os gastos
colunas = ("Categoria", "Valor", "Data")
tabela_despesa = ttk.Treeview(root, columns=colunas, show='headings')
for col in colunas:
    tabela_despesa.heading(col, text=col)
tabela_despesa.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Ajustando o tamanho das colunas da tabela
tabela_despesa.column("Categoria", width=200)
tabela_despesa.column("Valor", width=150)
tabela_despesa.column("Data", width=160)

# Mudar a fonte da tabela
tabela_despesa.tag_configure("Treeview", font=("Calibri", 12))

# Labels para mostrar o quanto foi gasto, quanto sobrou e o limite de gastos
total_despesa_label = tk.Label(root, text="Total de Gastos: R$ 0.00", bg='#7eb7c7', fg="#002f4e", font=("Calibri", 11))
total_despesa_label.grid(row=6, column=0, columnspan=2, pady=10)

saldo_restante_label = tk.Label(root, text="Saldo Restante: R$ 0.00", bg='#7eb7c7', fg="#002f4e", font=("Calibri", 11))
saldo_restante_label.grid(row=7, column=0, columnspan=2, pady=10)

limite_gastos_label = tk.Label(root, text="Limite de Gastos: R$ 0.00", bg='#7eb7c7', fg="#002f4e", font=("Calibri", 11))
limite_gastos_label.grid(row=8, column=0, columnspan=2, pady=10)

# Label para fazer com que as mensagens de status apareçam
status_label = tk.Label(root, text="", bg='#7eb7c7')
status_label.grid(row=9, column=0, columnspan=3, pady=10)

# Atualizar a tabela com dados carregados
update_tabela_despesa()

root.mainloop()