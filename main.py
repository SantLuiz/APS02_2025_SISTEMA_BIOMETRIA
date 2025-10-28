import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from BiometricSys import BiometricSys
from UserManager import UserManager


def start():
    """Cria e inicia a interface principal.

    Chamar `start()` abre a janela principal e executa o loop do Tk. Isso permite
    que outros módulos (por exemplo `acessos`) importem `main` sem abrir a GUI
    imediatamente, e chamem `main.start()` quando desejarem trocar de janela.
    """
    
    root = tk.Tk()
    root.title("Cadastro de Usuário")
    root.geometry("300x150")
    root.resizable(False, False)

   
    label_nome = ttk.Label(root, text="Nome de Usuário:")
    label_nome.pack(pady=(20, 5))

    
    entry_nome = ttk.Entry(root, width=30)
    entry_nome.pack()

    def Confere():
        biometria = BiometricSys()
        gerente = UserManager()
        username = entry_nome.get()
        template_valido = False
        
        user_id = gerente.get_user_id(username)

        if user_id is not None:

            img_path = BiometricSys.get_img_path()
            template_novo = biometria.generate_template(biometria.extract_minutiae(img_path))    
            templates_cadastrados = gerente.get_fingerprints(user_id)

            for t in templates_cadastrados:
                score = biometria.compare_templates(template_novo, t)
                if score > 90:
                    messagebox.showinfo("APROVADO!","IMPRESSÃO VALIDA")
                    template_valido = True
                    
                    try:
                        root.destroy()
                    except Exception:
                        pass
                    try:
                        import acessos
                        acessos.start(username)
                    except Exception as e:
                        messagebox.showerror("Erro", f"Não foi possível abrir a tela de acessos: {e}")
                    break
                
            if not template_valido:
                messagebox.showerror("Erro", "IMPRESSÃO INVALIDA")

        else:
            messagebox.showerror("Erro", "NOME INVALIDO")

    
    btn_inserir = ttk.Button(root, text="Inserir Digital", command = Confere)
    btn_inserir.pack(pady=20)

    
    root.mainloop()


if __name__ == "__main__":
    start()
