import tkinter as tk
from tkinter import messagebox, ttk
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        # Настройка стиля (как в калькуляторе)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Accent.TButton', font=('Arial', 10, 'bold'),
                             foreground='white', background='#0078d7',
                             bordercolor='#0078d7', focuscolor='none')
        self.style.map('Accent.TButton',
                       background=[('active', '#005a9e')])

        # Переменные для ввода
        self.length_var = tk.StringVar(value="14")
        self.count_var = tk.StringVar(value="1")

        # Переменные для чекбоксов (все включены по умолчанию)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        self.create_widgets()
        self.root.bind('<Return>', lambda event: self.generate())

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(main_frame, text="Генератор паролей",
                                 font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # Фрейм для полей ввода
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)

        # Длина пароля
        ttk.Label(input_frame, text="Длина пароля:",
                  font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=(0, 2))
        length_entry = ttk.Entry(input_frame, textvariable=self.length_var,
                                 width=10, font=('Arial', 11))
        length_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky='w')
        length_entry.focus()

        # Количество паролей
        ttk.Label(input_frame, text="Количество паролей:",
                  font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=(0, 2))
        count_entry = ttk.Entry(input_frame, textvariable=self.count_var,
                                width=10, font=('Arial', 11))
        count_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky='w')

        # Фрейм для чекбоксов (набор символов)
        charset_frame = ttk.LabelFrame(main_frame, text="Набор символов", padding=10)
        charset_frame.pack(fill='x', pady=10)

        # Располагаем чекбоксы в строку
        ttk.Checkbutton(charset_frame, text="Строчные (a-z)",
                        variable=self.use_lower).grid(row=0, column=0, padx=5)
        ttk.Checkbutton(charset_frame, text="Прописные (A-Z)",
                        variable=self.use_upper).grid(row=0, column=1, padx=5)
        ttk.Checkbutton(charset_frame, text="Цифры (0-9)",
                        variable=self.use_digits).grid(row=0, column=2, padx=5)
        ttk.Checkbutton(charset_frame, text="Символы (!@#$)",
                        variable=self.use_symbols).grid(row=0, column=3, padx=5)

        # Фрейм для кнопок
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)

        generate_btn = ttk.Button(button_frame, text="Сгенерировать",
                                   command=self.generate, style='Accent.TButton')
        generate_btn.grid(row=0, column=0, padx=10)

        reset_btn = ttk.Button(button_frame, text="Сбросить",
                               command=self.reset_fields)
        reset_btn.grid(row=0, column=1, padx=10)

        # Фрейм для результата
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Текстовое поле с увеличенным шрифтом
        self.result_text = tk.Text(
            result_frame, height=10, width=70, wrap='word',
            font=('Arial', 12), relief='solid', borderwidth=1,
            highlightthickness=1, highlightcolor='#ccc',
            bg='white'
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Запрещаем редактирование, но оставляем выделение и копирование
        self.result_text.bind('<Key>', self.block_key)
        self.result_text.bind('<Button-3>', self.show_context_menu)

        # Контекстное меню
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Копировать", command=self.copy_text)

    def block_key(self, event):
        """Разрешает только навигационные клавиши и Ctrl+C / Ctrl+A."""
        if event.state & 0x4:  # Ctrl
            if event.keysym in ('c', 'C', 'a', 'A'):
                return
        if event.keysym in ('Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Prior', 'Next'):
            return
        return 'break'

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def copy_text(self):
        try:
            selected = self.result_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            selected = self.result_text.get(1.0, tk.END).strip()
        if selected:
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
            self.root.update()

    def reset_fields(self):
        self.length_var.set("14")
        self.count_var.set("1")
        self.use_lower.set(True)
        self.use_upper.set(True)
        self.use_digits.set(True)
        self.use_symbols.set(True)
        self.result_text.delete(1.0, tk.END)
        self.root.focus_set()

    def generate(self):
        try:
            # Получаем и проверяем длину
            length_str = self.length_var.get().strip()
            if not length_str:
                raise ValueError("Укажите длину пароля")
            length = int(length_str)
            if length <= 0:
                raise ValueError("Длина должна быть положительным числом")
            if length > 1000:
                raise ValueError("Слишком большая длина (максимум 1000)")

            # Получаем и проверяем количество
            count_str = self.count_var.get().strip()
            if not count_str:
                count = 1
            else:
                count = int(count_str)
                if count <= 0:
                    raise ValueError("Количество должно быть положительным числом")
                if count > 100:
                    raise ValueError("Слишком много паролей (максимум 100)")

            # Формируем набор символов на основе чекбоксов
            chars = ""
            if self.use_lower.get():
                chars += 'abcdefghijklmnopqrstuvwxyz'
            if self.use_upper.get():
                chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if self.use_digits.get():
                chars += '0123456789'
            if self.use_symbols.get():
                chars += '!@#$'

            if not chars:
                raise ValueError("Выберите хотя бы один набор символов")

            # Генерация паролей
            passwords = []
            for _ in range(count):
                random_bytes = os.urandom(length)
                password = ''.join([chars[b % len(chars)] for b in random_bytes])
                passwords.append(password)

            # Вывод
            self.result_text.delete(1.0, tk.END)
            if count == 1:
                self.result_text.insert(1.0, passwords[0])
            else:
                for i, pwd in enumerate(passwords, 1):
                    self.result_text.insert(tk.END, f"{i:2}. {pwd}\n")

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
        except Exception as e:
            messagebox.showerror("Неожиданная ошибка", f"Произошла ошибка:\n{e}")

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()