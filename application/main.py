import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

DEBUG_MODE = True

# === Renk Paleti ===
BACKGROUND = "#f7f9fc"
PRIMARY = "#6c5ce7"
SECONDARY = "#00cec9"
TEXT_COLOR = "#2d3436"
BUTTON_COLOR = "#81ecec"
HIGHLIGHT = "#dfe6e9"

FONT_HEADER = ("Segoe UI", 20, "bold")
FONT_LABEL = ("Segoe UI", 12, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 11, "bold")

def run_algorithm(algorithm_name):
    selected_categories = [categories[i] for i in category_listbox.curselection()]
    selected_day = day_var.get()
    start_hour = start_hour_var.get()
    start_minute = start_minute_var.get()
    end_hour = end_hour_var.get()
    end_minute = end_minute_var.get()

    if not selected_categories or not selected_day:
        messagebox.showerror("Hata", "Lütfen tüm seçimleri yapın!")
        return

    try:
        command = ["python", f"{algorithm_name}.py", selected_day, f"{start_hour}:{start_minute}", f"{end_hour}:{end_minute}"] + selected_categories

        if DEBUG_MODE:
            print(f"[DEBUG] Çalıştırılıyor: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            messagebox.showerror("Hata", result.stderr.strip())
            return

        if DEBUG_MODE:
            print("[DEBUG] Algoritma çıktısı:")
            print(result.stdout.strip())

    except Exception as e:
        messagebox.showerror("Hata", f"Çalıştırma hatası: {e}")

# === Ana Pencere ===
root = tk.Tk()
root.title("📺 TV Programı Seçici")
root.geometry("720x850")
root.configure(bg=BACKGROUND)

# === TTK Tema Ayarı ===
style = ttk.Style()
style.theme_use("default")
style.configure("TLabel", background=BACKGROUND, foreground=TEXT_COLOR, font=FONT_NORMAL)
style.configure("TCombobox", padding=5)
style.configure("TSpinbox", padding=5)
style.map("TCombobox", fieldbackground=[("readonly", "white")])
style.configure("TButton", background=PRIMARY, foreground="white")

# === Başlık ===
tk.Label(root, text="🎥 TV Programı Seçici", font=FONT_HEADER, bg=BACKGROUND, fg=PRIMARY).pack(pady=20)

# === Kategori Seçimi ===
tk.Label(root, text="🎯 Program Türleri:", font=FONT_LABEL, bg=BACKGROUND, fg=TEXT_COLOR).pack()
categories = [
    "haber", "spor", "dram", "eğlence", "belgesel", "aşk", "yaşam", "polisiye", 
    "aile", "komedi", "aksiyon", "gerilim", "çizgifilm", "magazin", "romantikkomedi",
    "gençlik", "tarih", "bilimkurgu", "din", "yarışma", "tartışma", "askeri", "macera",
    "çizgidizi", "yemek"
]
category_var = tk.StringVar(value=categories)
category_listbox = tk.Listbox(root, listvariable=category_var, selectmode="multiple", height=8, width=30,
                              font=FONT_NORMAL, bg="white", bd=1, relief="solid", selectbackground=SECONDARY)
category_listbox.pack(pady=10)

# === Gün Seçimi ===
tk.Label(root, text="📅 Gün Seçimi:", font=FONT_LABEL, bg=BACKGROUND, fg=TEXT_COLOR).pack()
days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
day_var = tk.StringVar()
day_combobox = ttk.Combobox(root, textvariable=day_var, values=days, state="readonly", width=30, font=FONT_NORMAL)
day_combobox.pack(pady=8)

# === Saat Seçimi ===
tk.Label(root, text="🕑 Başlangıç Zamanı", font=FONT_LABEL, bg=BACKGROUND, fg=TEXT_COLOR).pack(pady=5)
time_frame = tk.Frame(root, bg=BACKGROUND)
time_frame.pack()

start_hour_var = tk.StringVar(value="00")
start_minute_var = tk.StringVar(value="00")
end_hour_var = tk.StringVar(value="00")
end_minute_var = tk.StringVar(value="00")

ttk.Label(time_frame, text="Saat:").grid(row=0, column=0, padx=5)
ttk.Spinbox(time_frame, from_=0, to=23, textvariable=start_hour_var, width=5, wrap=True).grid(row=0, column=1)

ttk.Label(time_frame, text="Dakika:").grid(row=0, column=2, padx=5)
ttk.Spinbox(time_frame, from_=0, to=59, textvariable=start_minute_var, width=5, wrap=True).grid(row=0, column=3)

tk.Label(root, text="🕔 Bitiş Zamanı", font=FONT_LABEL, bg=BACKGROUND, fg=TEXT_COLOR).pack(pady=5)
time_frame2 = tk.Frame(root, bg=BACKGROUND)
time_frame2.pack()

ttk.Label(time_frame2, text="Saat:").grid(row=0, column=0, padx=5)
ttk.Spinbox(time_frame2, from_=0, to=23, textvariable=end_hour_var, width=5, wrap=True).grid(row=0, column=1)

ttk.Label(time_frame2, text="Dakika:").grid(row=0, column=2, padx=5)
ttk.Spinbox(time_frame2, from_=0, to=59, textvariable=end_minute_var, width=5, wrap=True).grid(row=0, column=3)

# === Algoritma Butonları ===
tk.Label(root, text="🧠 Algoritma Seç:", font=FONT_LABEL, bg=BACKGROUND, fg=TEXT_COLOR).pack(pady=10)
button_frame = tk.Frame(root, bg=BACKGROUND)
button_frame.pack()

def create_algo_button(text, color, command):
    btn = tk.Button(button_frame, text=text, bg=color, fg="black", width=25, font=FONT_BUTTON,
                    activebackground=HIGHLIGHT, activeforeground=TEXT_COLOR, relief="flat", bd=0, cursor="hand2",
                    command=command)
    btn.pack(pady=6, ipadx=6, ipady=4)

create_algo_button("🔵 BFS Algoritması", "#0984e3", lambda: run_algorithm("bfs_algorithm"))
create_algo_button("🟣 DFS Algoritması", "#6c5ce7", lambda: run_algorithm("dfs_algorithm"))
create_algo_button("🟢 Greedy Algoritması", "#00b894", lambda: run_algorithm("greedy_algorithm"))
create_algo_button("🟠 A* Algoritması", "#fd9644", lambda: run_algorithm("astar_algorithm"))
create_algo_button("🔴 Genetik Algoritma", "#d63031", lambda: run_algorithm("genetic_algorithm"))

# === GUI Başlat ===
root.mainloop()
