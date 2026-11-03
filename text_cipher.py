import tkinter as tk
from tkinter import messagebox, ttk

from crypto_utils import decrypt_text, encrypt_text


class TextCipherApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Criptografar textos")
        root.minsize(520, 460)

        main = ttk.Frame(root, padding=16)
        main.grid(sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        ttk.Label(main, text="Texto").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.input_text = tk.Text(main, height=8, wrap="word", undo=True)
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(0, 12))

        ttk.Label(main, text="Senha").grid(row=2, column=0, sticky="w", pady=(0, 4))
        self.password = ttk.Entry(main, show="*")
        self.password.grid(row=3, column=0, sticky="ew", pady=(0, 12))

        actions = ttk.Frame(main)
        actions.grid(row=4, column=0, sticky="new", pady=(0, 12))
        ttk.Button(actions, text="Criptografar", command=self.encrypt).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Descriptografar", command=self.decrypt).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Copiar resultado", command=self.copy_result).pack(side="left")

        ttk.Label(main, text="Resultado").grid(row=5, column=0, sticky="w", pady=(0, 4))
        self.output_text = tk.Text(main, height=8, wrap="word")
        self.output_text.grid(row=6, column=0, sticky="nsew")
        main.rowconfigure(6, weight=1)

    def _get_input(self) -> tuple[str, str]:
        text = self.input_text.get("1.0", "end-1c")
        password = self.password.get()
        if not text:
            raise ValueError("Digite ou cole um texto primeiro.")
        if not password:
            raise ValueError("Informe uma senha.")
        return text, password

    def _show_result(self, value: str) -> None:
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", value)

    def encrypt(self) -> None:
        try:
            text, password = self._get_input()
            self._show_result(encrypt_text(text, password))
        except ValueError as error:
            messagebox.showerror("Não foi possível criptografar", str(error), parent=self.root)

    def decrypt(self) -> None:
        try:
            encrypted_text, password = self._get_input()
            self._show_result(decrypt_text(encrypted_text, password))
        except ValueError as error:
            messagebox.showerror("Não foi possível descriptografar", str(error), parent=self.root)

    def copy_result(self) -> None:
        result = self.output_text.get("1.0", "end-1c")
        if not result:
            messagebox.showinfo("Copiar resultado", "Não há resultado para copiar.", parent=self.root)
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.root.update()
        messagebox.showinfo("Copiado", "Resultado copiado para a área de transferência.", parent=self.root)


def main() -> None:
    root = tk.Tk()
    TextCipherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
