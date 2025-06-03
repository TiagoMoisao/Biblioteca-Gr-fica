from customtkinter import *

app = CTk()
app.title("Sistema de Biblioteca")
app.geometry("600x400")
set_appearance_mode("dark")
set_default_color_theme("blue")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)


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


class BibliotecaApp:
    def __init__(self, master):
        self.master = master
        self.biblioteca = Biblioteca()

        self.biblioteca.adicionar_livro(Livro("Os Lusíadas", "Camões", "L000"))
        self.biblioteca.adicionar_aluno(Aluno("João Silva", "A000"))

      
        self.main_frame = CTkFrame(master)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
    
        self.create_button("Adicionar Livro", self.adicionar_livro)
        self.create_button("Adicionar Aluno", self.adicionar_aluno)
        self.create_button("Listar Livros", self.listar_livros)
        self.create_button("Listar Alunos", self.listar_alunos)
        self.create_button("Emprestar Livro", self.emprestar_livro)
        self.create_button("Devolver Livro", self.devolver_livro)

    def create_button(self, text, command):
        button = CTkButton(
            self.main_frame,
            text=text,
            command=command,
            width=200,
            height=40,
            corner_radius=8,
            fg_color="#2a2d2e",
            hover_color="#343638",
            text_color="white"
        )
        button.pack(pady=10, fill="x")

    def adicionar_livro(self):
        dialog = CTkInputDialog(
            text="Informe os dados do livro:",
            title="Adicionar Livro"
        )
        
        titulo = dialog.get_input("Título:")
        autor = dialog.get_input("Autor:")
        codigo = dialog.get_input("Código:")
        
        if titulo and autor and codigo:
            self.biblioteca.adicionar_livro(Livro(titulo, autor, codigo))
            CTkMessagebox(
                title="Sucesso",
                message="Livro adicionado!",
                icon="check",
                option_1="OK"
            )

    def adicionar_aluno(self):
        dialog = CTkInputDialog(
            text="Informe os dados do aluno:",
            title="Adicionar Aluno"
        )
        
        nome = dialog.get_input("Nome:")
        matricula = dialog.get_input("Matrícula:")
        
        if nome and matricula:
            self.biblioteca.adicionar_aluno(Aluno(nome, matricula))
            CTkMessagebox(
                title="Sucesso",
                message="Aluno adicionado!",
                icon="check",
                option_1="OK"
            )

    def listar_livros(self):
        livros = self.biblioteca.listar_todos_livros()
        texto = "\n".join(str(l) for l in livros) if livros else "Nenhum livro cadastrado."
        CTkMessagebox(
            title="Livros",
            message=texto,
            icon="info",
            option_1="OK"
        )

    def listar_alunos(self):
        alunos = self.biblioteca.listar_alunos()
        texto = "\n".join(f"{a.matricula} | {a.nome}" for a in alunos) if alunos else "Nenhum aluno cadastrado."
        CTkMessagebox(
            title="Alunos",
            message=texto,
            icon="info",
            option_1="OK"
        )

    def emprestar_livro(self):
        dialog = CTkInputDialog(
            text="Informe os dados do empréstimo:",
            title="Emprestar Livro"
        )
        
        codigo = dialog.get_input("Código do Livro:")
        matricula = dialog.get_input("Matrícula do Aluno:")
        
        if self.biblioteca.emprestar_livro(codigo, matricula):
            CTkMessagebox(
                title="Sucesso",
                message="Livro emprestado com sucesso!",
                icon="check",
                option_1="OK"
            )
        else:
            CTkMessagebox(
                title="Erro",
                message="Não foi possível emprestar o livro.",
                icon="cancel",
                option_1="OK"
            )

    def devolver_livro(self):
        dialog = CTkInputDialog(
            text="Informe os dados da devolução:",
            title="Devolver Livro"
        )
        
        codigo = dialog.get_input("Código do Livro:")
        matricula = dialog.get_input("Matrícula do Aluno:")
        
        if self.biblioteca.devolver_livro(codigo, matricula):
            CTkMessagebox(
                title="Sucesso",
                message="Livro devolvido com sucesso!",
                icon="check",
                option_1="OK"
            )
        else:
            CTkMessagebox(
                title="Erro",
                message="Não foi possível devolver o livro.",
                icon="cancel",
                option_1="OK"
            )

if __name__ == "__main__":
    app = CTk()
    BibliotecaApp(app)
    app.mainloop()
