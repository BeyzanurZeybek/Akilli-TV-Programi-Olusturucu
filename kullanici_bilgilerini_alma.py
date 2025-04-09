import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# JSON dosyasını yükle
today_date = datetime.now().strftime("%Y-%m-%d")
json_filename = "weekly_tv_schedule_channels_final.json"

with open(json_filename, "r", encoding="utf-8") as json_file:
    weekly_schedule = json.load(json_file)

# Kullanıcının tercihlerini alacak GUI
root = tk.Tk()
root.title("Greedy Algoritması ile TV Programı Önerisi")
root.geometry("400x500")

# Başlık
title_label = tk.Label(root, text="Greedy Algoritması ile TV Programı Önerisi", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# Kullanıcıdan program türü seçmesini iste
tk.Label(root, text="İzlemek istediğiniz program türlerini seçin:").pack()
categories = ["haber", "spor", "dram", "eğlence", "belgesel", "aşk", "yaşam", "polisiye", "aile", "komedi", "aksiyon", "gerilim", "çizgifilm", "magazin", "romantikkomedi", "gençlik", "çizgifilm", "tarih", "bilimkurgu", "din", "yarışma", "tartışma", "askeri", "macera", "çizgidizi", "yemek"]
category_var = tk.StringVar(value=categories)
category_listbox = tk.Listbox(root, listvariable=category_var, selectmode="multiple", height=6)
category_listbox.pack(pady=5)

# Kullanıcıdan gün seçmesini iste
tk.Label(root, text="Hangi günü izlemek istersiniz?").pack()
days = list(weekly_schedule.keys())
day_var = tk.StringVar()
day_combobox = ttk.Combobox(root, textvariable=day_var, values=days, state="readonly")
day_combobox.pack(pady=5)

# Kullanıcıdan saat aralığı girmesini iste
tk.Label(root, text="İzlemek istediğiniz saat aralığını girin (örn: 15:00 - 19:00)").pack()
time_entry = tk.Entry(root)
time_entry.pack(pady=5)

# Greedy Algoritması ile en fazla program izleme
def greedy_search():
    selected_categories = [categories[i] for i in category_listbox.curselection()]
    selected_day = day_var.get()
    time_range = time_entry.get()

    if not selected_categories or not selected_day or not time_range:
        messagebox.showerror("Hata", "Lütfen tüm seçimleri yapın!")
        return

    try:
        start_time, end_time = time_range.split(" - ")
        start_hour, start_minute = map(int, start_time.split(":"))
        end_hour, end_minute = map(int, end_time.split(":"))
        start_minutes = start_hour * 60 + start_minute
        end_minutes = end_hour * 60 + end_minute
    except:
        messagebox.showerror("Hata", "Saat aralığını doğru formatta girin! (örn: 15:00 - 19:00)")
        return

    # Tüm uygun programları listeleyelim
    available_programs = []
    
    if selected_day in weekly_schedule:
        for channel, programs in weekly_schedule[selected_day].items():
            for program in programs:
                program_start, program_end = program["time"].split(" - ")
                program_start_hour, program_start_minute = map(int, program_start.split(":"))
                program_end_hour, program_end_minute = map(int, program_end.split(":"))
                program_start_minutes = program_start_hour * 60 + program_start_minute
                program_end_minutes = program_end_hour * 60 + program_end_minute
                
                # Programın uygun olup olmadığını kontrol et
                if program["category"] in selected_categories and start_minutes <= program_start_minutes < end_minutes:
                    available_programs.append((channel, program, program_start_minutes, program_end_minutes))
    
    # Programları başlangıç saatine göre sırala
    available_programs.sort(key=lambda x: x[2])

    selected_schedule = []
    current_time = start_minutes

    # Açgözlü Algoritma ile en fazla program izleme
    while current_time < end_minutes and available_programs:
        # Seçilebilecek en uzun programı bul
        best_program = None
        for program in available_programs:
            if program[2] >= current_time:  # Yeni program şu anki saatten sonra başlıyorsa
                if best_program is None or (program[3] - program[2] > best_program[3] - best_program[2]):
                    best_program = program
        
        if best_program:
            selected_schedule.append((best_program[0], best_program[1]))  # Kanal ve program ekle
            current_time = best_program[3]  # Yeni bitiş saatini güncelle
            available_programs.remove(best_program)  # Seçilen programı listeden kaldır
        else:
            break  # Uygun program kalmadıysa çık

    # Önerileri kaydetme ve gösterme
    if not selected_schedule:
        messagebox.showinfo("Sonuç", "Seçtiğiniz kriterlere uygun program bulunamadı.")
    else:
        personalized_schedule = {channel: [] for channel, _ in selected_schedule}
        for channel, program in selected_schedule:
            personalized_schedule[channel].append(program)
        
        json_filename_user = f"user_tv_schedule_greedy_{today_date}.json"
        with open(json_filename_user, "w", encoding="utf-8") as json_file:
            json.dump(personalized_schedule, json_file, ensure_ascii=False, indent=4)
        messagebox.showinfo("Başarı", f"Kişisel TV programınız oluşturuldu: {json_filename_user}")

# Buton ekleyerek fonksiyonu çağır
submit_button = tk.Button(root, text="Greedy Algoritması ile TV Programımı Oluştur", command=greedy_search, bg="blue", fg="white", font=("Arial", 12, "bold"))
submit_button.pack(pady=15)

# Arayüzü çalıştır
root.mainloop()
