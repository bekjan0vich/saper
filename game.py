import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import os


class ModernSaper:
    def __init__(self, root):
        self.root = root
        self.root.title("TERMINAL MINESWEEPER")
        self.root.configure(bg="#001a00")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        self.nickname = "Player"
        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.first_click = True
        self.menu_screen()

   

    def ask_nickname_step(self):
        name = simpledialog.askstring("Nickname", "Enter your nickname:")
        self.nickname = name if name else "Player"
        self.show_difficulty_levels()

    def show_difficulty_levels(self):
        for w in self.root.winfo_children():
            w.destroy()# ---------------- MENU ----------------
    def menu_screen(self):
        self.timer_running = False
        for w in self.root.winfo_children():
            w.destroy()

        main = tk.Frame(self.root, bg="#001a00")
        main.place(relx=0.5, rely=0.5, anchor="center")

        frame = tk.Frame(main, bg="#001a00", highlightbackground="#00FF00", highlightthickness=3)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="[ TERMINAL MINESWEEPER ]", font=("Courier", 35, "bold"),
                 fg="#00FF00", bg="#001a00").pack(pady=30)

        # START баскычы: Аны чакырганда ask_nickname_step иштейт
        tk.Button(frame, text="[ START GAME ]", font=("Courier", 22, "bold"),
                  fg="#00FF00", bg="#003300", activebackground="#00FF00", activeforeground="black",
                  width=20, relief="flat", command=self.ask_nickname_step).pack(pady=10)

        tk.Button(frame, text="[ EXIT ]", font=("Courier", 18), fg="red", bg="#001a00",
                  relief="flat", command=self.root.quit).pack(pady=20)

    # Жаңы кошулуучу логика:
    def ask_nickname_step(self):
        # Эгер мурун ат жазылбаса (б.а. демейки "Player" болсо) гана сурайт
        if self.nickname == "Player":
            name = simpledialog.askstring("Nickname", "Enter your nickname:")
            if name:
                self.nickname = name
        
        # Анан дароо деңгээлдерди көрсөтөбүз
        self.show_difficulty_levels()

        main = tk.Frame(self.root, bg="#001a00")
        main.place(relx=0.5, rely=0.5, anchor="center")

        frame = tk.Frame(main, bg="#001a00", highlightbackground="#00FF00", highlightthickness=3)
        frame.pack(padx=20, pady=20)

        style = {"font": ("Courier", 22, "bold"), "fg": "#00FF00", "bg": "#003300",
                 "activebackground": "#00FF00", "activeforeground": "black", "width": 20, "relief": "flat"}

        tk.Button(frame, text="EASY (8x8)", **style, command=lambda: self.start_game(8, 10)).pack(pady=10)
        tk.Button(frame, text="MEDIUM (16x16)", **style, command=lambda: self.start_game(16, 40)).pack(pady=10)
        tk.Button(frame, text="HARD (32x32)", **style, command=lambda: self.start_game(32, 100)).pack(pady=10)
        tk.Button(frame, text="RECORDS", **style, command=self.show_records).pack(pady=10)
        tk.Button(frame, text="[ BACK ]", font=("Courier", 18), fg="red", bg="#001a00",
                  relief="flat", command=self.menu_screen).pack(pady=20)

    # ---------------- START GAME ----------------
    def start_game(self, size, mines):
        for w in self.root.winfo_children():
            w.destroy()
        self.SIZE = size
        self.MINES = mines
        self.board = [[0] * size for _ in range(size)]
        self.mines, self.buttons, self.revealed, self.flags = set(), [], set(), set()
        self.first_click, self.timer_running = True, True
        self.start_time = time.time()
        self.create_ui()
        self.update_timer()

    # ---------------- UI (Авто-ресайз кошулду) ----------------
    def create_ui(self):
        # Башкы маалымат панели
        header = tk.Frame(self.root, bg="#001a00")
        header.pack(pady=20)
        self.mine_label = tk.Label(header, text=f"MINES: {self.MINES}", fg="#FFCC00", bg="#001a00",
                                   font=("Courier", 20, "bold"))
        self.mine_label.pack(side="left", padx=20)
        self.timer_label = tk.Label(header, text="TIME: 000", fg="#FFCC00", bg="#001a00", font=("Courier", 20, "bold"))
        self.timer_label.pack(side="left", padx=20)
        tk.Label(header, text=f"PLAYER: {self.nickname}", fg="#00FF00", bg="#001a00", font=("Courier", 16)).pack(
            side="left", padx=20)
        tk.Button(header, text="[ MENU ]", fg="#00FF00", bg="#001a00", font=("Courier", 14), relief="flat",
                  command=self.menu_screen).pack(side="left", padx=20)

        # Клеткалар жайгашкан аянт
        # Фонду кара түскө өзгөртөбүз, ошондо баскычтардын ортосундагы сызыктар көрүнөт
        grid = tk.Frame(self.root, bg="#000000", padx=2, pady=2)
        grid.pack()

        # Динамикалык өлчөм
        btn_w = 2 if self.SIZE > 20 else 3
        font_size = 10 if self.SIZE > 20 else 14

        for x in range(self.SIZE):
            row = []
            for y in range(self.SIZE):
                # relief="raised" баскычтарга көлөкө берип, аларды айырмалайт
                btn = tk.Button(grid,
                                width=btn_w,
                                height=1,
                                bg="#003300",
                                fg="#00FF00",
                                relief="raised",
                                font=("Courier", font_size, "bold"))

                btn.bind("<Button-1>", lambda e, x=x, y=y: self.left_click(x, y))
                btn.bind("<Button-3>", lambda e, x=x, y=y: self.right_click(x, y))

                # padx=1, pady=1 клеткалардын ортосунда 1 пикселдик аралык калтырат
                btn.grid(row=x, column=y, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"TIME: {self.elapsed_time}")
            self.root.after(1000, self.update_timer)


    def create_mines(self, safe_x, safe_y):
        while len(self.mines) < self.MINES:
            x, y = random.randint(0, self.SIZE - 1), random.randint(0, self.SIZE - 1)
            if (x, y) != (safe_x, safe_y): self.mines.add((x, y))
        for x, y in self.mines:
            self.board[x][y] = -1
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.SIZE and 0 <= ny < self.SIZE and self.board[nx][ny] != -1: self.board[nx][ny] += 1


    def left_click(self, x, y):
        if (x, y) in self.flags: return
        if self.first_click:
            self.create_mines(x, y)
            self.first_click = False
        if (x, y) in self.mines:
            self.timer_running = False
            self.show_all_mines()
            messagebox.showinfo("GAME OVER", "💥 BOOM!")
            self.menu_screen()
            return
        self.reveal(x, y)
        self.check_win()


    def right_click(self, x, y):
        if (x, y) in self.revealed: return
        if (x, y) in self.flags:
            self.flags.remove((x, y))
            self.buttons[x][y].config(text="")
        else:
            self.flags.add((x, y))
            self.buttons[x][y].config(text="!", fg="red")


    def reveal(self, x, y):
        if (x, y) in self.revealed: return
        self.revealed.add((x, y))
        btn = self.buttons[x][y]
        number = self.board[x][y]
        btn.config(bg="#005500", relief="sunken")
        if number > 0:
            btn.config(text=str(number))
        elif number == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.SIZE and 0 <= ny < self.SIZE: self.reveal(nx, ny)


    def save_record(self):
        file = "records.txt"
        records = []
        if os.path.exists(file):
            with open(file, "r") as f:
                for line in f:
                    name, score = line.strip().split(",")
                    records.append((name, int(score)))
        records.append((self.nickname, self.elapsed_time))
        records = sorted(records, key=lambda x: x[1])[:5]
        with open(file, "w") as f:
            for r in records: f.write(f"{r[0]},{r[1]}\n")


    def show_records(self):
        file = "records.txt"
        if not os.path.exists(file):
            messagebox.showinfo("Records", "No records yet")
            return
        text = ""
        with open(file) as f:
            for i, line in enumerate(f, 1):
                name, score = line.strip().split(",")
                text += f"{i}. {name} - {score}s\n"
        messagebox.showinfo("TOP 5 RECORDS", text)



    def check_win(self):
        if len(self.revealed) == self.SIZE * self.SIZE - self.MINES:
            self.timer_running = False
            self.save_record()
            messagebox.showinfo("WINNER", f"🏆 {self.nickname} WIN!\nTime: {self.elapsed_time}s")
            self.menu_screen()


    def show_all_mines(self):
        for x, y in self.mines:
            self.buttons[x][y].config(text="*", bg="red", fg="white")


if __name__ == "__main__":
    root = tk.Tk()
    game = ModernSaper(root)
    root.mainloop()