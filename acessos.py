import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import webbrowser
# explicit import
from UserManager import UserManager
# sys/subprocess were previously used for spawning main; now we call main.start() directly

def start(username):
    gerente = UserManager()

    # --- Funções para o banco ---
    def open_link(event):
        """
        Abre o link selecionado no navegador.
        """
        selection = listbox_links.curselection()
        if selection:
            url = listbox_links.get(selection[0])
            webbrowser.open(url)

    # --- Interface ---
    def show_links_for_user(username):
        # Aqui buscamos o nível de acesso do usuário no banco
              
        user_level = gerente.get_acess_lvl(username)
        links = gerente.get_links_by_access(user_level)
        
        # Limpa a lista antes de adicionar os novos links
        listbox_links.delete(0, tk.END)
        for link in links:
            listbox_links.insert(tk.END, link)
    
    def sair():
        """Fecha esta janela e chama `main.start()` para abrir a janela principal.

        Essa abordagem evita spawn de processo e permite trocar janelas dentro
        do mesmo processo (mais limpa)."""
        try:
            root.destroy()
        except Exception:
            pass

        try:
            import main
            # chama a função start do módulo main para abrir a janela principal
            main.start()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o main: {e}")

    # --- Janela principal ---
    root = tk.Tk()
    root.title("Links por Nível de Acesso")
    root.geometry("500x400")

    # Entrada de usuário
    frame_user = ttk.Frame(root)
    frame_user.pack(pady=10)

    ttk.Label(frame_user, text=f"USUÁRIO: {username.upper()} | NÍVEL DE ACESSO: {gerente.get_acess_lvl(username)}").pack(side=tk.LEFT, padx=5)

    btn_load = ttk.Button(frame_user, text="Sair", command=sair)
    btn_load.pack(side=tk.LEFT, padx=5)

    # Lista de links
    listbox_links = tk.Listbox(root, width=60, height=15)
    listbox_links.pack(pady=20)
    listbox_links.bind("<Double-Button-1>", open_link)  # duplo clique abre o link
    show_links_for_user(username)
    root.mainloop()


