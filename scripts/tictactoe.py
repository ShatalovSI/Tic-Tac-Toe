import player
import themes
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import tkinter.messagebox
import webbrowser as wb


class TicTacToeGame:
    def __init__(self, first_player_name, second_player_name):
        self.first_player = player.Player(first_player_name)
        self.second_player = player.Player(second_player_name)
        self.current_player = self.first_player
        self.root = tk.Tk()
        self.field_buttons = []
        self.pixelVirtual = tk.PhotoImage(width=1, height=1)
        self.total_games = 0
        self.total_draws = 0
        self.theme = themes.default_theme
        self.var = tkinter.IntVar()
        self.var.set(0)

    # ----------------------------------------------------------------------------------------- Настройки главного окна
    def root_window_settings(self):
        x = 500
        y = 100
        self.root.wm_geometry("330x382+%d+%d" % (x, y))
        self.root.title('Крестики-нолики')
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.root.resizable(0, 0)
        self.root.config(bg=self.theme['window_bg'])

        for child in self.root.winfo_children():
            child.destroy()

        root_menu = tk.Menu(self.root)
        self.root.config(menu=root_menu)

        game_menu = tk.Menu(root_menu, tearoff=0)
        game_menu.add_command(label="Создать новую", command=self.create_root_window)
        game_menu.add_command(label="Таблица победителей", command=self.create_table_of_winners_window)
        game_menu.add_command(label="Настройки", command=self.create_settings_window)
        game_menu.add_command(label="Сменить имя", command=self.create_change_window)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.on_closing)

        help_menu = tk.Menu(root_menu, tearoff=0)
        help_menu.add_command(label="Помощь", command=self.create_help_window)
        help_menu.add_command(label="О программе", command=self.create_about_program_window)

        root_menu.add_cascade(label="Игра", menu=game_menu)
        root_menu.add_cascade(label="Справка", menu=help_menu)

    # --------------------------------------------------------------------------------- Создание приветственного экрана
    def create_hello_window(self):
        self.root_window_settings()

        bg = tk.PhotoImage(file="images/background.png")
        canvas = tk.Canvas(self.root, width=320, height=382)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg, anchor="nw")
        canvas.create_text(160, 70, text="КРЕСТИКИ-НОЛИКИ", fill='white', font=("Helvetica", "16", "bold"))

        button = tk.Button(
            self.root,
            bg='white',
            text='НАЧАТЬ',
            relief='flat',
            width=15,
            cursor='hand2',
            font=("Helvetica", "16", "bold"),
            command=self.create_change_window
        )
        button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

        self.root.update()
        print(self.root.wm_geometry())

        self.root.mainloop()

    # ----------------------------------------------------------------------------------------- Создание экрана с игрой
    def create_root_window(self):
        self.root_window_settings()

        self.field_buttons = [tk.Button(
            self.root,
            text='',
            image=self.pixelVirtual,
            width=100,
            height=100,
            bg=self.theme['game_button_bg'],
            fg=self.theme['game_button_fg'],
            relief='flat',
            padx=1,
            font=('Arial', 20, 'bold'),
            command=lambda x=i: self.push(x, first_label, second_label, current_label),
            compound="c"
        ) for i in range(9)]

        row, col = 0, 0
        for i in range(9):
            self.field_buttons[i].grid(row=row, column=col, sticky='news', padx=2, pady=2)
            col += 1
            if col == 3:
                row += 1
                col = 0

        first_label = tk.Label(
            text=self.first_player.name + '\n' + str(self.first_player.wins_count),
            bg=self.theme['game_label_bg'],
            fg=self.theme['label_fg']

        )
        second_label = tk.Label(
            text=self.second_player.name + '\n' + str(self.second_player.wins_count),
            bg=self.theme['game_label_bg'],
            fg=self.theme['label_fg']
        )
        current_label = tk.Label(
            text='Ходит:\n' + self.current_player.name,
            bg=self.theme['game_label_bg'],
            fg=self.theme['label_fg']
        )

        first_label.grid(row=3, column=0, pady=8)
        second_label.grid(row=3, column=2, pady=8)
        current_label.grid(row=3, column=1, pady=8)

        for i in range(2):
            self.root.grid_columnconfigure(i, minsize=60)
            self.root.columnconfigure(i, weight=1, minsize=60)

        for i in range(3):
            self.root.grid_rowconfigure(i, minsize=60)
            self.root.rowconfigure(i, weight=1, minsize=60)

    # ----------------------------------------------------------------------------------------------- Экран смены имени
    def create_change_window(self):
        self.root_window_settings()

        change_frame = self.get_main_frame()
        self.get_main_label(change_frame,
                            'Введите имена игроков').grid(row=0, column=0, sticky='ew', columnspan=2, pady=10)
        self.get_separator(change_frame).grid(row=1, column=0, columnspan=2, ipadx=200, pady=10)

        tk.Label(
            change_frame,
            text="Первый Игрок",
            fg=self.theme['label_fg'],
            bg=self.theme['label_bg']
        ).grid(row=2, column=0, sticky=tk.W, pady=10)

        tk.Label(
            change_frame,
            text="Второй Игрок",
            fg=self.theme['label_fg'],
            bg=self.theme['label_bg']
        ).grid(row=3, column=0, sticky=tk.W, pady=10)

        register_first_name = tk.Entry(change_frame, bg=self.theme['entry_bg'], fg=self.theme['entry_fg'])
        register_second_name = tk.Entry(change_frame, bg=self.theme['entry_bg'], fg=self.theme['entry_fg'])

        register_first_name.insert(0, self.first_player.name)
        register_second_name.insert(0, self.second_player.name)

        register_btn = tk.Button(
            change_frame,
            width=15,
            text='Ввод',
            relief=tk.SOLID,
            cursor='hand2',
            bg=self.theme['button_bg'],
            command=lambda: self.change_players_name(register_first_name, register_second_name)
        )

        register_first_name.grid(row=2, column=1, pady=10, padx=20)
        register_second_name.grid(row=3, column=1, pady=10, padx=20)
        register_btn.grid(row=4, column=1, pady=10, padx=20)
        change_frame.pack(fill="both", expand=True, padx=20, pady=20)
        change_frame.grid_columnconfigure(0, weight=1)
        change_frame.grid_columnconfigure(1, weight=1)

    # ------------------------------------------------------------------------------------ Создание таблицы победителей
    def create_table_of_winners_window(self):

        def get_label(text):
            return tk.Label(winners_frame, text=text, bg=self.theme['label_bg'], fg=self.theme['label_fg'])

        self.root_window_settings()

        winners_frame = self.get_main_frame()
        self.get_main_label(winners_frame,
                            'Таблица победителей').grid(row=0, column=0, sticky='ew', columnspan=2, pady=10)
        self.get_separator(winners_frame).grid(row=1, column=0, columnspan=2, ipadx=200, pady=10)

        get_label(self.first_player.name).grid(row=2, column=0, sticky='ew', pady=10)
        get_label(self.second_player.name).grid(row=2, column=1, sticky='ew', pady=10)
        get_label(self.first_player.wins_count).grid(row=3, column=0, sticky='ew', pady=10)
        get_label(self.second_player.wins_count).grid(row=3, column=1, sticky='ew', pady=10)

        self.get_separator(winners_frame).grid(row=4, column=0, columnspan=2, ipadx=200, pady=10)

        get_label('Всего игр').grid(row=5, column=0, sticky='ew', pady=10)
        get_label('Всего ничьих').grid(row=5, column=1, sticky='ew', pady=10)
        get_label(self.total_games).grid(row=6, column=0, sticky='ew', pady=10)
        get_label(self.total_draws).grid(row=6, column=1, sticky='ew', pady=10)

        self.get_separator(winners_frame).grid(row=7, column=0, columnspan=2, ipadx=200, pady=10)

        register_btn = tk.Button(
            winners_frame,
            width=15,
            text='Сбросить',
            relief=tk.SOLID,
            cursor='hand2',
            bg=self.theme['button_bg'],
            command=self.reset_winners
        )
        register_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=20)
        winners_frame.pack(fill="both", expand=True, padx=20, pady=20)

        winners_frame.grid_columnconfigure(0, weight=1)
        winners_frame.grid_columnconfigure(1, weight=1)

    # -------------------------------------------------------------------------------------------- Создание окна помощи
    def create_help_window(self):
        self.root_window_settings()

        help_frame = self.get_main_frame()
        self.get_main_label(help_frame, 'Правила игры').grid(row=0, column=0, sticky='ew', pady=10)
        self.get_separator(help_frame).grid(row=1, column=0, ipadx=200, pady=10)

        help_textbox = tk.scrolledtext.ScrolledText(
            help_frame,
            width=40,
            relief=tk.SOLID,
            height=16,
            bg=self.theme['textbox_bg'],
            fg=self.theme['textbox_fg']
        )
        help_textbox.grid(row=2, column=0, sticky='news')
        text1 = 'Кре́стики-но́лики — логическая \nигра между двумя противниками \nна квадратном поле 3 на 3 \nклетки ' \
                'или большего размера \n(вплоть до «бесконечного \nполя»). Один из игроков играет «крестиками», ' \
                'второй — \n«ноликами». Игроки по очереди ставят на свободные клетки \nполя 3х3 знаки (один всегда ' \
                '\nкрестики, другой всегда \nнолики). Первый, выстроивший в ряд 3 своих фигуры по \nвертикали, ' \
                'горизонтали или \nдиагонали, выигрывает. Первый ход делает игрок, ставящий \nкрестики. Обычно по ' \
                'завершении партии выигравшая сторона \nзачёркивает чертой свои три \nзнака (нолика или крестика), ' \
                '\nсоставляющих сплошной ряд.'
        help_textbox.insert(tk.INSERT, text1)
        help_textbox.configure(state='disabled')

        help_frame.pack(fill="both", expand=True, padx=20, pady=20)
        help_frame.grid_columnconfigure(0, weight=1)
        help_frame.grid_columnconfigure(1, weight=1)

    # --------------------------------------------------------------------------------------- Создание окна о программе
    def create_about_program_window(self):
        self.root_window_settings()

        about_frame = self.get_main_frame()
        self.get_main_label(about_frame, 'О программе').grid(row=0, column=0, sticky='ew', columnspan=2, pady=10)
        self.get_separator(about_frame).grid(row=1, column=0, ipadx=200, pady=10)

        tk.Label(
            about_frame,
            bg=self.theme['label_bg'],
            fg=self.theme['label_fg'],
            text='Крестики-нолики на двоих\nВерсия: 2.0',
        ).grid(row=2, column=0, pady=10)

        tk.Label(
            about_frame,
            bg=self.theme['label_bg'],
            text='Лицензионное соглашение',
            cursor='hand2',
            fg='#4b6eaf',
        ).grid(row=3, column=0, pady=10)

        label = tk.Label(
            about_frame,
            bg=self.theme['label_bg'],
            text='Связаться с автором',
            cursor='hand2',
            fg='#4b6eaf',
        )

        label.grid(row=4, column=0, pady=10)
        label.bind("<Button-1>", self.callback)

        about_frame.pack(fill="both", expand=True, padx=20, pady=20)
        about_frame.grid_columnconfigure(0, weight=1)

    @staticmethod
    def callback(event):
        wb.open_new(r"https://t.me/return_zero")

    # ------------------------------------------------------------------------------------------ Создание окна настроек
    def create_settings_window(self):
        self.root_window_settings()

        settings_frame = self.get_main_frame()
        self.get_main_label(settings_frame, 'Настройки').grid(row=0, column=0, sticky='ew', pady=10)
        self.get_separator(settings_frame).grid(row=1, column=0, ipadx=200, pady=10)

        tk.Label(
            settings_frame,
            bg=self.theme['label_bg'],
            fg=self.theme['label_fg'],
            text='Выберите тему оформления:',
        ).grid(row=2, column=0, sticky='ew', pady=10)

        rb0 = tk.Radiobutton(settings_frame, text="Классическая", command=self.change_theme,
                             variable=self.var, value=0, bg=self.theme['label_bg'])
        rb1 = tk.Radiobutton(settings_frame, text="Коралловая", command=self.change_theme,
                             variable=self.var, value=1, bg=self.theme['label_bg'])
        rb2 = tk.Radiobutton(settings_frame, text="Темная", command=self.change_theme,
                             variable=self.var, value=2, bg=self.theme['label_bg'])
        rb3 = tk.Radiobutton(settings_frame, text="Экстравагантная", command=self.change_theme,
                             variable=self.var, value=3, bg=self.theme['label_bg'])

        rb0.grid(row=3, column=0, sticky='ew', pady=10)
        rb1.grid(row=4, column=0, sticky='ew', pady=10)
        rb2.grid(row=5, column=0, sticky='ew', pady=10)
        rb3.grid(row=6, column=0, sticky='ew', pady=10)

        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

        settings_frame.grid_columnconfigure(0, weight=1)

    # ---------------------------------------------------------------------------------------------------- Сменить тему
    def change_theme(self):
        if self.var.get() == 0:
            self.theme = themes.default_theme
            self.create_settings_window()
        elif self.var.get() == 1:
            self.theme = themes.coral_theme
            self.create_settings_window()
        elif self.var.get() == 2:
            self.theme = themes.dark_theme
            self.create_settings_window()
        else:
            self.theme = themes.toxic_theme
            self.create_settings_window()

    # ----------------------------------------------------------------------------------------- Создание основной рамки
    def get_main_frame(self):
        return tk.Frame(
            self.root,
            bd=2,
            bg=self.theme['frame_bg'],
            relief=tk.SOLID,
            padx=10,
            pady=10,
        )

    # --------------------------------------------------------------------------------------------- Создание сепаратора
    @staticmethod
    def get_separator(root):
        return ttk.Separator(
            master=root,
            orient=tk.HORIZONTAL,
            class_=ttk.Separator,
            takefocus=1,
            cursor='plus'
        )

    # ------------------------------------------------------------------------------------ Создание основного заголовка
    def get_main_label(self, root, text):
        return tk.Label(
            root,
            text=text,
            fg=self.theme['label_fg'],
            font=("Helvetica", "11", "bold"),
            bg=self.theme['label_bg']
        )

    # ------------------------------------------------------------------------------------ Сбросить таблицу победителей
    def reset_winners(self):
        self.first_player.wins_count = 0
        self.second_player.wins_count = 0
        self.total_games = 0
        self.total_draws = 0
        self.create_table_of_winners_window()

    # ------------------------------------------------------------------------------------------------- Проверка победы
    def check_victory(self):
        solution = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

        for i in solution:
            if all(j in self.current_player.player_positions for j in i):
                return True
        return False

    # ------------------------------------------------------------------------------------------------- Проверка ничьей
    def check_tie(self):
        if len(self.first_player.player_positions) + len(self.second_player.player_positions) == 9:
            return True
        return False

    # ------------------------------------------------------------------------------------------------------ Перезапуск
    def restart_game(self, current):
        for button in self.field_buttons:
            button.config(text='', state='active')
        self.first_player.reset_positions()
        self.second_player.reset_positions()
        self.change_players()
        current.config(text='Ходит:\n' + self.current_player.name)

    # --------------------------------------------------------------------------------------------------- Смена игроков
    def change_players(self):
        if self.current_player == self.first_player:
            self.current_player = self.second_player
        else:
            self.current_player = self.first_player

    # --------------------------------------------------------------------------------------------------- Закрытие окна
    def on_closing(self):
        if tkinter.messagebox.askokcancel('Выход из приложения', 'Хотите выйти из приложения?'):
            self.root.destroy()

    # ----------------------------------------------------------------------------------------------------- Смена имени
    def change_players_name(self, first_entry, second_entry):
        self.first_player.name = first_entry.get()
        self.second_player.name = second_entry.get()
        self.create_root_window()

    # --------------------------------------------------------------------------------------------- Клик на кнопке поля
    def push(self, x, first, second, current):
        self.current_player.player_positions.append(x + 1)

        if self.current_player == self.first_player:
            self.field_buttons[x].config(text='X', state='disabled')
        else:
            self.field_buttons[x].config(text='O', state='disabled')

        if self.check_victory():
            self.total_games += 1
            self.current_player.wins_count += 1
            first.config(text=self.first_player.name + '\n' + str(self.first_player.wins_count))
            second.config(text=self.second_player.name + '\n' + str(self.second_player.wins_count))

            for button in self.field_buttons:
                button.config(state='disabled')
            self.restart_game(current)
            self.create_root_window()
            return

        if self.check_tie():
            self.total_games += 1
            self.total_draws += 1
            for button in self.field_buttons:
                button.config(state='disabled')
            self.restart_game(current)
            self.create_root_window()
            return

        self.change_players()
        current.config(text='Ходит:\n' + self.current_player.name)

    # ----------------------------------------------------------------------------------------------------- Начало игры
    def start_game(self):
        self.create_hello_window()
        self.root.mainloop()
