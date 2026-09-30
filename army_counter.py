import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date
import json
import os
import sys

CONFIG_FILE = "army_config.json"

class ArmyCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Счётчик дней Игоря в армии")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")
        
        # Загружаем конфигурацию
        self.config = self.load_config()
        self.start_date = self.config.get("start_date")
        
        self.setup_ui()
        self.update_display()
        # Автообновление каждую минуту
        self.auto_update()
        
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def setup_ui(self):
        # Заголовок
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(pady=20)
        
        tk.Label(
            title_frame, 
            text="🪖 Счётчик дней Игоря в армии", 
            font=("Segoe UI", 18, "bold"),
            fg="#e94560",
            bg="#1a1a2e"
        ).pack()
        
        tk.Label(
            title_frame,
            text="Автоматический подсчёт со дня призыва",
            font=("Segoe UI", 10),
            fg="#a0a0b0",
            bg="#1a1a2e"
        ).pack(pady=5)
        
        # Основная карточка
        self.main_card = tk.Frame(self.root, bg="#16213e", relief="flat", bd=0)
        self.main_card.pack(pady=20, padx=30, fill="x")
        
        # Статус
        self.status_label = tk.Label(
            self.main_card,
            text="",
            font=("Segoe UI", 14, "bold"),
            fg="#e94560",
            bg="#16213e"
        )
        self.status_label.pack(pady=20)
        
        # Счётчик дней
        self.days_label = tk.Label(
            self.main_card,
            text="",
            font=("Segoe UI", 48, "bold"),
            fg="#00d9a5",
            bg="#16213e"
        )
        self.days_label.pack(pady=10)
        
        tk.Label(
            self.main_card,
            text="дней в армии",
            font=("Segoe UI", 14),
            fg="#a0a0b0",
            bg="#16213e"
        ).pack(pady=5)
        
        # Дата призыва
        self.date_label = tk.Label(
            self.main_card,
            text="",
            font=("Segoe UI", 12),
            fg="#a0a0b0",
            bg="#16213e"
        )
        self.date_label.pack(pady=10)
        
        # Свечки (визуализация)
        candles_frame = tk.Frame(self.main_card, bg="#16213e")
        candles_frame.pack(pady=15)
        
        tk.Label(
            candles_frame,
            text="🕯 Свечки памяти:",
            font=("Segoe UI", 12, "bold"),
            fg="#ffd700",
            bg="#16213e"
        ).pack()
        
        self.candles_canvas = tk.Canvas(candles_frame, height=80, bg="#16213e", highlightthickness=0)
        self.candles_canvas.pack(pady=10)
        
        # Кнопки управления
        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(pady=20)
        
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Segoe UI", 11), padding=10)
        
        self.set_date_btn = ttk.Button(
            btn_frame,
            text="📅 Установить дату призыва",
            command=self.set_start_date,
            style="Custom.TButton"
        )
        self.set_date_btn.pack(side="left", padx=10)
        
        self.reset_btn = ttk.Button(
            btn_frame,
            text="🔄 Сбросить",
            command=self.reset_date,
            style="Custom.TButton"
        )
        self.reset_btn.pack(side="left", padx=10)
        
        # Инфо внизу
        info_frame = tk.Frame(self.root, bg="#1a1a2e")
        info_frame.pack(side="bottom", pady=15)
        
        tk.Label(
            info_frame,
            text="Обновляется автоматически • Данные сохраняются локально",
            font=("Segoe UI", 8),
            fg="#555",
            bg="#1a1a2e"
        ).pack()
    
    def calculate_days(self):
        if not self.start_date:
            return None
        try:
            start = datetime.strptime(self.start_date, "%Y-%m-%d").date()
            today = date.today()
            delta = today - start
            return delta.days
        except:
            return None
    
    def draw_candles(self, days):
        self.candles_canvas.delete("all")
        canvas_width = 440
        candle_width = 30
        candle_height = 60
        spacing = 5
        start_x = (canvas_width - (candle_width * 7 + spacing * 6)) // 2
        y_bottom = 70
        
        # Показываем свечи за последние 7 дней (или меньше если дней меньше)
        show_days = min(days, 7) if days > 0 else 0
        
        for i in range(show_days):
            x = start_x + i * (candle_width + spacing)
            # Свеча
            self.candles_canvas.create_rectangle(
                x + 10, y_bottom - candle_height,
                x + 20, y_bottom,
                fill="#ff6b35", outline="#ff4500", width=2
            )
            # Пламя
            flame_y = y_bottom - candle_height - 15
            self.candles_canvas.create_oval(
                x + 8, flame_y,
                x + 22, flame_y + 20,
                fill="#ffd700", outline="#ff8c00", width=1
            )
            self.candles_canvas.create_oval(
                x + 11, flame_y + 3,
                x + 19, flame_y + 15,
                fill="#ffaa00", outline=""
            )
            # День
            self.candles_canvas.create_text(
                x + 15, y_bottom + 15,
                text=f"+{days - i}",
                font=("Segoe UI", 8, "bold"),
                fill="#ffd700"
            )
        
        if days > 7:
            # Показываем "..." если дней больше 7
            x = start_x + 7 * (candle_width + spacing)
            self.candles_canvas.create_text(
                x + 15, y_bottom - candle_height // 2,
                text="...",
                font=("Segoe UI", 16, "bold"),
                fill="#ffd700"
            )
            self.candles_canvas.create_text(
                x + 15, y_bottom + 15,
                text=f"+{days - 7}+",
                font=("Segoe UI", 8, "bold"),
                fill="#a0a0b0"
            )
        elif days <= 0:
            self.candles_canvas.create_text(
                canvas_width // 2, 40,
                text="🕯 Свечки появятся после установки даты",
                font=("Segoe UI", 10),
                fill="#555"
            )
    
    def update_display(self):
        days = self.calculate_days()
        
        if self.start_date:
            start_formatted = datetime.strptime(self.start_date, "%Y-%m-%d").strftime("%d.%m.%Y")
            self.date_label.config(text=f"Дата призыва: {start_formatted}")
            
            if days is not None:
                if days < 0:
                    self.status_label.config(text="⏳ Призыв ещё не наступил")
                    self.days_label.config(text="0")
                    self.draw_candles(0)
                elif days == 0:
                    self.status_label.config(text="🎯 Сегодня день призыва!")
                    self.days_label.config(text="0")
                    self.draw_candles(0)
                else:
                    self.status_label.config(text="✅ Игорь в армии")
                    self.days_label.config(text=str(days))
                    self.draw_candles(days)
        else:
            self.status_label.config(text="👕 Пока он ещё на гражданке")
            self.days_label.config(text="—")
            self.date_label.config(text="Дата призыва не установлена")
            self.draw_candles(0)
    
    def set_start_date(self):
        # Диалог ввода даты
        dialog = tk.Toplevel(self.root)
        dialog.title("Установить дату призыва")
        dialog.geometry("350x250")
        dialog.resizable(False, False)
        dialog.configure(bg="#1a1a2e")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Центрируем
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(
            dialog,
            text="📅 Выберите дату призыва Игоря",
            font=("Segoe UI", 12, "bold"),
            fg="#e94560",
            bg="#1a1a2e"
        ).pack(pady=20)
        
        # Поля ввода даты
        input_frame = tk.Frame(dialog, bg="#1a1a2e")
        input_frame.pack(pady=10)
        
        # День
        tk.Label(input_frame, text="День:", fg="#fff", bg="#1a1a2e").grid(row=0, column=0, padx=5, pady=5)
        day_var = tk.StringVar(value=datetime.now().strftime("%d"))
        day_entry = ttk.Entry(input_frame, textvariable=day_var, width=5, font=("Segoe UI", 12), justify="center")
        day_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Месяц
        tk.Label(input_frame, text="Месяц:", fg="#fff", bg="#1a1a2e").grid(row=0, column=2, padx=5, pady=5)
        month_var = tk.StringVar(value=datetime.now().strftime("%m"))
        month_entry = ttk.Entry(input_frame, textvariable=month_var, width=5, font=("Segoe UI", 12), justify="center")
        month_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Год
        tk.Label(input_frame, text="Год:", fg="#fff", bg="#1a1a2e").grid(row=0, column=4, padx=5, pady=5)
        year_var = tk.StringVar(value=datetime.now().strftime("%Y"))
        year_entry = ttk.Entry(input_frame, textvariable=year_var, width=7, font=("Segoe UI", 12), justify="center")
        year_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Быстрые кнопки
        quick_frame = tk.Frame(dialog, bg="#1a1a2e")
        quick_frame.pack(pady=15)
        
        def set_quick_date(offset_days):
            target = date.today() + __import__('datetime').timedelta(days=offset_days)
            day_var.set(target.strftime("%d"))
            month_var.set(target.strftime("%m"))
            year_var.set(target.strftime("%Y"))
        
        ttk.Button(quick_frame, text="Сегодня", command=lambda: set_quick_date(0)).pack(side="left", padx=5)
        ttk.Button(quick_frame, text="Завтра", command=lambda: set_quick_date(1)).pack(side="left", padx=5)
        ttk.Button(quick_frame, text="Через неделю", command=lambda: set_quick_date(7)).pack(side="left", padx=5)
        
        def save_date():
            try:
                day = int(day_var.get())
                month = int(month_var.get())
                year = int(year_var.get())
                # Валидация
                test_date = date(year, month, day)
                self.start_date = test_date.strftime("%Y-%m-%d")
                self.config["start_date"] = self.start_date
                self.save_config()
                self.update_display()
                dialog.destroy()
                messagebox.showinfo("Успешно", f"Дата призыва установлена: {test_date.strftime('%d.%m.%Y')}")
            except ValueError as e:
                messagebox.showerror("Ошибка", "Неверная дата. Проверьте день, месяц и год.")
        
        btn_frame = tk.Frame(dialog, bg="#1a1a2e")
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="💾 Сохранить", command=save_date).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Отмена", command=dialog.destroy).pack(side="left", padx=10)
    
    def reset_date(self):
        if messagebox.askyesno("Подтверждение", "Сбросить дату призыва? Счётчик вернётся в режим 'на гражданке'."):
            self.start_date = None
            self.config.pop("start_date", None)
            self.save_config()
            self.update_display()
    
    def auto_update(self):
        self.update_display()
        # Обновляем каждую минуту (60000 мс)
        self.root.after(60000, self.auto_update)

def get_resource_path(relative_path):
    """Получает путь к ресурсу для работы и в .exe, и в скрипте"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    # Меняем рабочую директорию на папку с exe/скриптом
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    root = tk.Tk()
    # Иконка (опционально)
    try:
        root.iconbitmap(default=get_resource_path("icon.ico"))
    except:
        pass
    
    app = ArmyCounterApp(root)
    root.mainloop()