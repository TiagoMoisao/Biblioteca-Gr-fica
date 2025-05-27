import tkinter as tk
from tkinter import messagebox, simpledialog

# === Classes principais ===
class Livro:
    def __init__(self, titulo, autor, codigo):
        self.titulo = titulo
        self.autor = autor
        self.codigo = codigo
        self.disponivel = True

    def __str__(self):
        estado = "Disponível" if self.disponivel else "Emprestado"
        return f"{self.codigo} | {self.titulo} | {self.autor} | {estado}"

class Aluno:
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula
        self.livros_emprestados = []
        self.limite_livros = 3

    def emprestar_livro(self, livro):
        if len(self.livros_emprestados) < self.limite_livros:
            self.livros_emprestados.append(livro)
            livro.disponivel = False
            return True
        return False

    def devolver_livro(self, livro):
        if livro in self.livros_emprestados:
            self.livros_emprestados.remove(livro)
            livro.disponivel = True
            return True
        return False

class Biblioteca:
    def __init__(self):
        self.catalogo = []
        self.alunos = []

    def adicionar_livro(self, livro):
        self.catalogo.append(livro)

    def adicionar_aluno(self, aluno):
        self.alunos.append(aluno)

    def procurar_livro_por_codigo(self, codigo):
        return next((l for l in self.catalogo if l.codigo == codigo), None)

    def procurar_aluno_por_matricula(self, matricula):
        return next((a for a in self.alunos if a.matricula == matricula), None)

    def listar_livros_disponiveis(self):
        return [l for l in self.catalogo if l.disponivel]

    def listar_todos_livros(self):
        return self.catalogo

    def listar_alunos(self):
        return self.alunos

    def emprestar_livro(self, codigo, matricula):
        livro = self.procurar_livro_por_codigo(codigo)
        aluno = self.procurar_aluno_por_matricula(matricula)
        if not livro or not aluno or not livro.disponivel:
            return False
        return aluno.emprestar_livro(livro)

    def devolver_livro(self, codigo, matricula):
        livro = self.procurar_livro_por_codigo(codigo)
        aluno = self.procurar_aluno_por_matricula(matricula)
        if not livro or not aluno or livro.disponivel:
            return False
        return aluno.devolver_livro(livro)

# === Interface gráfica ===
class BibliotecaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Biblioteca")
        self.biblioteca = Biblioteca()

        # Dados de exemplo
        self.biblioteca.adicionar_livro(Livro("Os Lusíadas", "Camões", "L000"))
        self.biblioteca.adicionar_aluno(Aluno("João Silva", "A000"))

        # Botões principais
        tk.Button(master, text="Adicionar Livro", command=self.adicionar_livro).pack(fill=tk.X)
        tk.Button(master, text="Adicionar Aluno", command=self.adicionar_aluno).pack(fill=tk.X)
        tk.Button(master, text="Listar Livros", command=self.listar_livros).pack(fill=tk.X)
        tk.Button(master, text="Listar Alunos", command=self.listar_alunos).pack(fill=tk.X)
        tk.Button(master, text="Emprestar Livro", command=self.emprestar_livro).pack(fill=tk.X)
        tk.Button(master, text="Devolver Livro", command=self.devolver_livro).pack(fill=tk.X)

    def adicionar_livro(self):
        titulo = simpledialog.askstring("Título", "Informe o título do livro:")
        autor = simpledialog.askstring("Autor", "Informe o autor do livro:")
        codigo = simpledialog.askstring("Código", "Informe o código do livro:")
        if titulo and autor and codigo:
            self.biblioteca.adicionar_livro(Livro(titulo, autor, codigo))
            messagebox.showinfo("Sucesso", "Livro adicionado!")

    def adicionar_aluno(self):
        nome = simpledialog.askstring("Nome", "Informe o nome do aluno:")
        matricula = simpledialog.askstring("Matrícula", "Informe a matrícula do aluno:")
        if nome and matricula:
            self.biblioteca.adicionar_aluno(Aluno(nome, matricula))
            messagebox.showinfo("Sucesso", "Aluno adicionado!")

    def listar_livros(self):
        livros = self.biblioteca.listar_todos_livros()
        texto = "\n".join(str(l) for l in livros) if livros else "Nenhum livro cadastrado."
        messagebox.showinfo("Livros", texto)

    def listar_alunos(self):
        alunos = self.biblioteca.listar_alunos()
        texto = "\n".join(f"{a.matricula} | {a.nome}" for a in alunos) if alunos else "Nenhum aluno cadastrado."
        messagebox.showinfo("Alunos", texto)

    def emprestar_livro(self):
        codigo = simpledialog.askstring("Código do Livro", "Informe o código do livro:")
        matricula = simpledialog.askstring("Matrícula do Aluno", "Informe a matrícula do aluno:")
        if self.biblioteca.emprestar_livro(codigo, matricula):
            messagebox.showinfo("Sucesso", "Livro emprestado com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível emprestar o livro.")

    def devolver_livro(self):
        codigo = simpledialog.askstring("Código do Livro", "Informe o código do livro:")
        matricula = simpledialog.askstring("Matrícula do Aluno", "Informe a matrícula do aluno:")
        if self.biblioteca.devolver_livro(codigo, matricula):
            messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível devolver o livro.")

# Inicializar a aplicação
root = tk.Tk()
app = BibliotecaApp(root)
root.mainloop()
