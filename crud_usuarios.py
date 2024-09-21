import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

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

# Funções CRUD
def criar_usuario():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()
    endereco = entry_endereco.get()
    telefone = entry_telefone.get()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Usuarios (nome, email, senha, endereco, telefone) VALUES (%s, %s, %s, %s, %s)",
                   (nome, email, senha, endereco, telefone))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
    listar_usuarios()

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

def atualizar_usuario():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Seleção", "Selecione um usuário para atualizar.")
        return
    usuario_id = tree.item(selected_item)['values'][0]
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()
    endereco = entry_endereco.get()
    telefone = entry_telefone.get()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE Usuarios SET nome=%s, email=%s, senha=%s, endereco=%s, telefone=%s WHERE id=%s",
                   (nome, email, senha, endereco, telefone, usuario_id))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
    listar_usuarios()

def deletar_usuario():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Seleção", "Selecione um usuário para deletar.")
        return
    usuario_id = tree.item(selected_item)['values'][0]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Usuarios WHERE id=%s", (usuario_id,))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Usuário deletado com sucesso!")
    listar_usuarios()

# Interface Gráfica
root = tk.Tk()
root.title("Sistema CRUD de Usuários")

# Campos de entrada
tk.Label(root, text="Nome").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Email").grid(row=1, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1)

tk.Label(root, text="Senha").grid(row=2, column=0)
entry_senha = tk.Entry(root, show='*')
entry_senha.grid(row=2, column=1)

tk.Label(root, text="Endereço").grid(row=3, column=0)
entry_endereco = tk.Entry(root)
entry_endereco.grid(row=3, column=1)

tk.Label(root, text="Telefone").grid(row=4, column=0)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=4, column=1)

# Botões
tk.Button(root, text="Criar", command=criar_usuario).grid(row=5, column=0)
tk.Button(root, text="Atualizar", command=atualizar_usuario).grid(row=5, column=1)
tk.Button(root, text="Deletar", command=deletar_usuario).grid(row=5, column=2)

# Treeview para listar usuários
tree = ttk.Treeview(root, columns=("ID", "Nome", "Email", "Senha", "Endereço", "Telefone"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Email", text="Email")
tree.heading("Senha", text="Senha")
tree.heading("Endereço", text="Endereço")
tree.heading("Telefone", text="Telefone")
tree.grid(row=6, column=0, columnspan=3)

listar_usuarios()  # Listar usuários ao iniciar

root.mainloop()

