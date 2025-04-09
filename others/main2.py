import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

DEBUG_MODE = True  # Debug modunu aç/kapat

def run_algorithm(algorithm_name):
    """
    Seçilen algoritmayı çalıştırır, gerekli parametreleri iletir ve sonucu GUI'de gösterir.
    """
    selected_categories = [categories[i] for i in category_listbox.curselection()]
    selected_day = day_var.get()
    start_hour = start_hour_var.get()
    start_minute = start_minute_var.get()
    end_hour = end_hour_var.get()
    end_minute = end_minute_var.get()
    
    if DEBUG_MODE:
        print(f"\n[DEBUG] '{algorithm_name}' algoritması butona basıldı.")

    if not selected_categories or not selected_day:
        messagebox.showerror("Hata", "Lütfen tüm seçimleri yapın!")
        if DEBUG_MODE:
            print("[DEBUG] Kullanıcı seçim yapmadan butona bastı.")
        return
    
    try:
        # Algoritmayı çalıştır ve sonucu al
        command = ["python", f"{algorithm_name}.py", selected_day, f"{start_hour}:{start_minute}", f"{end_hour}:{end_minute}"] + selected_categories

        if DEBUG_MODE:
            print(f"[DEBUG] Çalıştırılacak komut: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)

        if DEBUG_MODE:
            print(f"[DEBUG] Subprocess returncode: {result.returncode}")

        # Hata kontrolü
        if result.returncode != 0:
            error_message = result.stderr.strip()
            messagebox.showerror("Hata", f"Algoritma çalıştırılırken hata oluştu:\n{error_message}")
            if DEBUG_MODE:
                print(f"[DEBUG] Algoritma çalıştırılırken hata oluştu:\n{error_message}")
            return
        
        # Sonucu GUI'ye düzgün şekilde yazdır
        output_text = result.stdout.strip()
        if DEBUG_MODE:
            print(f"[DEBUG] Algoritma çıktısı:\n{output_text if output_text else '[Boş Çıktı]'}")

        if not output_text:
            output_text = "⚠️ Algoritma sonucu boş döndü!"

        display_results(output_text)

    except Exception as e:
        error_message = f"Algoritma çalıştırılırken hata oluştu: {e}"
        messagebox.showerror("Hata", error_message)
        if DEBUG_MODE:
            print(f"[DEBUG] Exception oluştu: {error_message}")

def display_results(result_text):
    """
    Çalıştırılan algoritmanın sonucunu GUI içinde gösterir.
    """
    result_label.config(text=result_text, justify="left", font=("Arial", 10))
    result_label.pack(pady=10)
    root.update_idletasks()  # GUI'nin hemen güncellenmesini sağla

    if DEBUG_MODE:
        print(f"[DEBUG] Sonuç GUI'ye yazıldı.\n")

# **Ana Arayüzü Tanımla**
root = tk.Tk()
root.title("TV Programı Seçici (Debug Modu)")
root.geometry("600x750")

tk.Label(root, text="📺 TV Programı Seçici", font=("Arial", 16, "bold")).pack(pady=10)

# **Program Türü Seçici**
tk.Label(root, text="İzlemek istediğiniz program türlerini seçin:").pack()
categories = [
    "haber", "spor", "dram", "eğlence", "belgesel", "aşk", "yaşam", "polisiye", 
    "aile", "komedi", "aksiyon", "gerilim", "çizgifilm", "magazin", "romantikkomedi",
    "gençlik", "tarih", "bilimkurgu", "din", "yarışma", "tartışma", "askeri", "macera",
    "çizgidizi", "yemek"
]
category_var = tk.StringVar(value=categories)
category_listbox = tk.Listbox(root, listvariable=category_var, selectmode="multiple", height=8)
category_listbox.pack(pady=5)

# **Gün Seçici**
tk.Label(root, text="📅 Hangi günü izlemek istersiniz?").pack()
days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
day_var = tk.StringVar()
day_combobox = ttk.Combobox(root, textvariable=day_var, values=days, state="readonly")
day_combobox.pack(pady=5)

# **Saat Seçici**
tk.Label(root, text="🕒 İzlemek istediğiniz başlangıç saatini seçin:").pack()
start_hour_var = tk.StringVar(value="00")
start_hour_spinbox = ttk.Spinbox(root, from_=0, to=23, textvariable=start_hour_var, wrap=True, width=5)
start_hour_spinbox.pack(pady=2)

tk.Label(root, text="Dakika seçin:").pack()
start_minute_var = tk.StringVar(value="00")
start_minute_spinbox = ttk.Spinbox(root, from_=0, to=59, textvariable=start_minute_var, wrap=True, width=5)
start_minute_spinbox.pack(pady=2)

tk.Label(root, text="Bitiş saatini seçin:").pack()
end_hour_var = tk.StringVar(value="00")
end_hour_spinbox = ttk.Spinbox(root, from_=0, to=23, textvariable=end_hour_var, wrap=True, width=5)
end_hour_spinbox.pack(pady=2)

tk.Label(root, text="Bitiş dakikasını seçin:").pack()
end_minute_var = tk.StringVar(value="00")
end_minute_spinbox = ttk.Spinbox(root, from_=0, to=59, textvariable=end_minute_var, wrap=True, width=5)
end_minute_spinbox.pack(pady=2)

# **Algoritma Seçimi Butonları**
tk.Label(root, text="📌 Algoritma Seçin:").pack(pady=5)
tk.Button(root, text="BFS Algoritması", command=lambda: run_algorithm("bfs_algorithm"), bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(root, text="DFS Algoritması", command=lambda: run_algorithm("dfs_algorithm"), bg="purple", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(root, text="Greedy Algoritması", command=lambda: run_algorithm("greedy_algorithm"), bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(root, text="A* Algoritması", command=lambda: run_algorithm("astar_algorithm"), bg="orange", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(root, text="Genetik Algoritma", command=lambda: run_algorithm("genetic_algorithm"), bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

# **Sonuç Gösterme Alanı**
result_label = tk.Label(root, text="", wraplength=550, justify="left", font=("Arial", 10))
result_label.pack(pady=10)

root.mainloop()