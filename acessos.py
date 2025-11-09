import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from sistema_biometrico.user_manager import UserManager


def start(username):
    gerente = UserManager()

    def open_link(event):
        """
        Abre o link selecionado no navegador.
        """
        selection = listbox_links.curselection()
        if selection:
            url = listbox_links.get(selection[0])
            webbrowser.open(url)

    def show_links_for_user(username):
        user_level = gerente.get_access_level(username)
        links = gerente.get_links_by_access(user_level)

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
            gerente.close()
            import main

            main.start()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o main: {e}")

    root = tk.Tk()
    root.title("Links por Nível de Acesso")
    root.geometry("500x400")

    frame_user = ttk.Frame(root)
    frame_user.pack(pady=10)

    ttk.Label(
        frame_user,
        text=f"USUÁRIO: {username.upper()} | NÍVEL DE ACESSO: {gerente.get_access_level(username)}",
    ).pack(side=tk.LEFT, padx=5)

    btn_load = ttk.Button(frame_user, text="Sair", command=sair)
    btn_load.pack(side=tk.LEFT, padx=5)

    listbox_links = tk.Listbox(root, width=60, height=15)
    listbox_links.pack(pady=20)
    listbox_links.bind("<Double-Button-1>", open_link)
    show_links_for_user(username)
    root.mainloop()
