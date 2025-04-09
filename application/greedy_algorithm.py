import json
import sys
import matplotlib.pyplot as plt

# ========== TV PROGRAMLARI YÜKLEME ========== #
def load_tv_schedule(filename="weekly_tv_schedule_channels_final.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# **Saatleri dakika cinsine çevirme fonksiyonu**
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes

# **Dakikayı saat formatına çevirme fonksiyonu (örn: 720 → "12:00")**
def minutes_to_time(minutes):
    return f"{minutes // 60}:{minutes % 60:02d}"

# **Kullanıcının tercih ettiği kriterlere uygun programları seç**
def filter_programs(day, start_time, end_time, selected_categories):
    schedule = load_tv_schedule()
    
    if day not in schedule:
        print("❌ HATA: Seçilen gün için program bulunamadı!")
        return []

    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)

    # **Eğer bitiş saati, başlangıç saatinden küçükse (örneğin 23:00 - 01:00) gece yarısını geçtiğini anla**
    if end_minutes < start_minutes:
        end_minutes += 24 * 60  # **Bitiş saatine 24 saat ekleyerek ertesi güne taşı**

    valid_programs = []

    for channel, programs in schedule[day].items():
        for program in programs:
            program_start, program_end = program["time"].split(" - ")
            program_start_minutes = time_to_minutes(program_start)
            program_end_minutes = time_to_minutes(program_end)

            # **Gece yarısını geçen programları düzelt**
            if program_end_minutes < program_start_minutes:
                program_end_minutes += 24 * 60  # **Program ertesi güne geçiyorsa, 24 saat ekle**
            if end_minutes < start_minutes:
                end_minutes += 24 * 60  # **Program ertesi güne geçiyorsa, 24 saat ekle**

            categories = program["category"].split(" ")

            # **Program başlangıç zamanı uygun ve kategori eşleşiyorsa ekle**
            if any(cat in selected_categories for cat in categories) and (start_minutes <= program_start_minutes < end_minutes or program_start_minutes <= start_minutes <= program_end_minutes):
                valid_programs.append({
                    "channel": channel,
                    "program": program["program"],
                    "start": program_start_minutes,
                    "end": program_end_minutes,
                    "duration": program_end_minutes - program_start_minutes,
                    "categories": categories  
                })
    print(valid_programs)
    return valid_programs

# ========== GELİŞTİRİLMİŞ GREEDY ALGORİTMA ========== #
def greedy_algorithm(day, start_time, end_time, selected_categories):
    program_list = filter_programs(day, start_time, end_time, selected_categories)

    if not program_list:
        return None, "Uygun program bulunamadı"

    # **Programları başlangıç saatine göre sırala**
    program_list.sort(key=lambda x: x["start"])

    print("📋 Sıralanmış Program Listesi:")
    for p in program_list:
        print(f"{p['program']} ({minutes_to_time(p['start'])} - {minutes_to_time(p['end'])}, {p['duration']} dk)")

    schedule = []
    current_time = time_to_minutes(start_time)

    while current_time < time_to_minutes(end_time):
        # **Mevcut saatten itibaren başlayan programları filtrele**
        available_programs = [p for p in program_list if p["start"] >= current_time]

        if not available_programs:
            break  # **İzlenecek program kalmadıysa çık**

        # **Eğer birden fazla en erken başlayan program varsa, en uzun olanı seç**
        min_start_time = min(p["start"] for p in available_programs)
        earliest_programs = [p for p in available_programs if p["start"] == min_start_time]
        best_program = max(earliest_programs, key=lambda x: x["duration"])

        # **Programı listeye ekle ve zaman güncelle**
        schedule.append({
            "channel": best_program["channel"],
            "program": best_program["program"],
            "start": best_program["start"],
            "end": best_program["end"]
        })

        current_time = best_program["end"]  # **Saat güncellendi**

    return schedule, "Greedy Algoritma tamamlandı"

# **Gantt Chart Gösterimi (Saat Formatında)**
def show_gantt_chart(schedule, day, start_time, end_time):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']

    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)
    total_minutes = end_minutes - start_minutes

    # **Eğer izleme süresi 6 saatten kısa ise → 30 dakikalık aralıklarla göster**
    # **Eğer izleme süresi 6 saatten uzunsa → 1 saatlik aralıklarla göster**
    time_step = 30 if total_minutes <= 360 else 60  

    for idx, program in enumerate(schedule):
        ax.barh(y=idx, width=(program["end"] - program["start"]), left=program["start"], 
                color=colors[idx % len(colors)], edgecolor='black')
        ax.text(program["start"] + (program["end"] - program["start"]) / 2, idx, 
                f"{program['program']}", va='center', ha='center', fontsize=10, color="white")

    ax.set_yticks(range(len(schedule)))
    ax.set_yticklabels([p["channel"] for p in schedule])
    
    # **Dinamik X Ekseni (Saat Formatında)**
    ax.set_xticks(range(start_minutes, end_minutes + 1, time_step))  
    ax.set_xticklabels([minutes_to_time(t) for t in range(start_minutes, end_minutes + 1, time_step)])

    ax.set_xlabel("Zaman (Saat)")
    ax.set_title(f"{day} - Greedy Algoritma TV İzleme Planı")
    plt.grid(axis='x', linestyle="--", alpha=0.5)
    plt.show()

# **Ana Çalıştırma Bloğu**
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("⚠️ Eksik parametre! Kullanım:")
        print("python greedy_algorithm.py <Gün> <Başlangıç Saati> <Bitiş Saati> <Kategori1> <Kategori2> ...")
        sys.exit(1)

    selected_day = sys.argv[1]
    selected_start_time = sys.argv[2]
    selected_end_time = sys.argv[3]
    selected_categories = sys.argv[4:]

    best_schedule, message = greedy_algorithm(selected_day, selected_start_time, selected_end_time, selected_categories)

    if best_schedule:
        show_gantt_chart(best_schedule, selected_day, selected_start_time, selected_end_time)
