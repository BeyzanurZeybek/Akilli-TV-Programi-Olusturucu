import heapq
from build_tree import build_tree, minutes_to_time, time_to_minutes

# ========== A* Algoritması ==========
def a_star_algorithm(day, start_time, end_time, selected_categories):
    tree = build_tree(day, start_time, end_time, selected_categories)

    if not tree:
        return None, "Uygun program bulunamadı"

    open_list = []
    heapq.heappush(open_list, (0, time_to_minutes(start_time), []))  # (f(n), şu anki zaman, izlenen programlar)

    best_schedule = []
    max_duration = 0

    while open_list:
        f_n, current_time, watched_programs = heapq.heappop(open_list)

        # **Toplam izlenen süreyi kontrol et**
        total_duration = sum(p[3] - p[2] for p in watched_programs)  # (end - start)
        if total_duration > max_duration:
            max_duration = total_duration
            best_schedule = watched_programs

        # **Uygun programları sıraya ekle**
        for channel, programs in tree.items():
            for program in programs:
                if program["start"] >= current_time:  # **Zamanı geçen programları atla**
                    new_schedule = watched_programs + [(channel, program["program"], program["start"], program["end"])]
                    g_n = total_duration + (program["end"] - program["start"])  # Şu ana kadarki toplam izleme süresi
                    h_n = program["duration"]  # Heuristic: uzun süreli programları tercih et
                    f_n = g_n + h_n  # A*'ın maliyet fonksiyonu

                    heapq.heappush(open_list, (f_n, program["end"], new_schedule))

    return best_schedule, "A* Algoritması tamamlandı"

# **Gantt Chart Gösterimi**
def show_gantt_chart(schedule, day, start_time, end_time):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']

    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)
    time_step = 30 if (end_minutes - start_minutes) <= 360 else 60  

    unique_channels = list(set([program[0] for program in schedule]))  # Kanal isimleri
    unique_channels.sort()
    y_positions = {channel: i for i, channel in enumerate(unique_channels)}

    for program in schedule:
        ax.barh(y=y_positions[program[0]], 
                width=(program[3] - program[2]), 
                left=program[2], 
                color=colors[unique_channels.index(program[0]) % len(colors)], 
                edgecolor='black')

        ax.text(program[2] + (program[3] - program[2]) / 2, 
                y_positions[program[0]], 
                f"{program[1]}", 
                va='center', ha='center', fontsize=10, color="white")

    ax.set_yticks(range(len(unique_channels)))
    ax.set_yticklabels(unique_channels)
    
    ax.set_xticks(range(start_minutes, end_minutes + 1, time_step))
    ax.set_xticklabels([minutes_to_time(t) for t in range(start_minutes, end_minutes + 1, time_step)])

    ax.set_xlabel("Zaman (Saat)")
    ax.set_ylabel("Kanal")
    ax.set_title(f"{day} - A* Algoritma TV İzleme Planı")
    plt.grid(axis='x', linestyle="--", alpha=0.5)
    plt.show()

# **Ana Çalıştırma Bloğu**
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5:
        print("⚠️ Eksik parametre! Kullanım:")
        print("python astar_algorithm.py <Gün> <Başlangıç Saati> <Bitiş Saati> <Kategori1> <Kategori2> ...")
        sys.exit(1)

    selected_day = sys.argv[1]
    selected_start_time = sys.argv[2]
    selected_end_time = sys.argv[3]
    selected_categories = sys.argv[4:]

    best_schedule, message = a_star_algorithm(selected_day, selected_start_time, selected_end_time, selected_categories)

    if best_schedule:
        show_gantt_chart(best_schedule, selected_day, selected_start_time, selected_end_time)
