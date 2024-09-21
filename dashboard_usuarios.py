import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configurações do banco de dados
DB_CONFIG = {
    'dbname': 'banco_de_dados',
    'user': 'usuario',
    'password': 'senha',
    'host': 'localhost',
    'port': '5432'
}

# Função para conectar ao banco de dados
def conectar():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")

# Função para listar usuários
def listar_usuarios():
    for item in tree.get_children():
        tree.delete(item)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    cursor.close()
    conn.close()

# Função para gerar gráfico de consumo
def gerar_grafico():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT dispositivo_id, SUM(consumo) FROM ConsumoEnergia GROUP BY dispositivo_id")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()

    if dados:
        dispositivos = [f"Dispositivo {row[0]}" for row in dados]
        consumos = [row[1] for row in dados]

        fig, ax = plt.subplots()
        ax.bar(dispositivos, consumos, color='blue')
        ax.set_xlabel('Dispositivos')
        ax.set_ylabel('Consumo (kWh)')
        ax.set_title('Consumo de Energia por Dispositivo')

        # Integrando o gráfico ao Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Criar a interface gráfica
root = tk.Tk()
root.title("Dashboard do Sistema")

# Frame para a tabela de usuários
frame_usuarios = tk.Frame(root)
frame_usuarios.pack(pady=10)

# Tabela de usuários
tree = ttk.Treeview(frame_usuarios, columns=("ID", "Nome", "Email", "Senha", "Endereço", "Telefone"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Email", text="Email")
tree.heading("Senha", text="Senha")
tree.heading("Endereço", text="Endereço")
tree.heading("Telefone", text="Telefone")
tree.pack()

# Botão para listar usuários
btn_listar = tk.Button(root, text="Listar Usuários", command=listar_usuarios)
btn_listar.pack(pady=10)

# Frame para o gráfico
frame_grafico = tk.Frame(root)
frame_grafico.pack(pady=10)

# Botão para gerar gráfico
btn_grafico = tk.Button(root, text="Gerar Gráfico de Consumo", command=gerar_grafico)
btn_grafico.pack(pady=10)

root.mainloop()

