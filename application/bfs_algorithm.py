import json
import sys
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from build_tree import build_tree, minutes_to_time, time_to_minutes

# ========== BFS Algoritması ==========
def bfs_algorithm(day, start_time, end_time, selected_categories):
    tree = build_tree(day, start_time, end_time, selected_categories)

    if not tree:
        return None, "Uygun program bulunamadı"

    schedule = []
    queue = deque()  # BFS için kuyruk
    visited = set()  # Tekrar eden programları engellemek için

    # **Kanalların sıraya konması (Ağaç sırası korunuyor)**
    channels_in_order = list(tree.keys())

    # **Her kanalın ilk programını sıraya ekle**
    max_program_count = max(len(tree[channel]) for channel in channels_in_order)  # En fazla programa sahip kanal
    for i in range(max_program_count):
        for channel in channels_in_order:
            if i < len(tree[channel]):  # Kanalın i. programı varsa ekle
                queue.append((tree[channel][i]["start"], tree[channel][i], channel))  # (Başlangıç zamanı, program, kanal)

    current_time = time_to_minutes(start_time)

    while queue:
        start, program, channel = queue.popleft()

        # **Eğer program zaten izlendi veya geçmiş saatse atla**
        if (program["program"], program["start"]) in visited or program["start"] < current_time:
            continue  

        # **Programı izleme listesine ekle**
        schedule.append({
            "channel": channel,
            "program": program["program"],
            "start": program["start"],
            "end": program["end"],
            "duration": program["duration"]
        })
        visited.add((program["program"], program["start"]))

        # **Saat güncelle ve sıradaki programları sırayla ekle**
        current_time = program["end"]

    return schedule, "BFS Algoritması tamamlandı"

# **Gantt Chart Gösterimi**
def show_gantt_chart(schedule, day, start_time, end_time):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']

    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)
    time_step = 30 if (end_minutes - start_minutes) <= 360 else 60  

    unique_channels = list(set([program["channel"] for program in schedule]))
    unique_channels.sort()
    y_positions = {channel: i for i, channel in enumerate(unique_channels)}

    for program in schedule:
        ax.barh(y=y_positions[program["channel"]], 
                width=(program["end"] - program["start"]), 
                left=program["start"], 
                color=colors[unique_channels.index(program["channel"]) % len(colors)], 
                edgecolor='black')

        ax.text(program["start"] + (program["end"] - program["start"]) / 2, 
                y_positions[program["channel"]], 
                f"{program['program']}", 
                va='center', ha='center', fontsize=10, color="white")

    ax.set_yticks(range(len(unique_channels)))
    ax.set_yticklabels(unique_channels)
    
    ax.set_xticks(range(start_minutes, end_minutes + 1, time_step))
    ax.set_xticklabels([minutes_to_time(t) for t in range(start_minutes, end_minutes + 1, time_step)])

    ax.set_xlabel("Zaman (Saat)")
    ax.set_ylabel("Kanal")
    ax.set_title(f"{day} - BFS Algoritma TV İzleme Planı")
    plt.grid(axis='x', linestyle="--", alpha=0.5)
    plt.show()

# **Ana Çalıştırma Bloğu**
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("⚠️ Eksik parametre! Kullanım:")
        print("python bfs_algorithm.py <Gün> <Başlangıç Saati> <Bitiş Saati> <Kategori1> <Kategori2> ...")
        sys.exit(1)

    selected_day = sys.argv[1]
    selected_start_time = sys.argv[2]
    selected_end_time = sys.argv[3]
    selected_categories = sys.argv[4:]

    best_schedule, message = bfs_algorithm(selected_day, selected_start_time, selected_end_time, selected_categories)

    if best_schedule:
        show_gantt_chart(best_schedule, selected_day, selected_start_time, selected_end_time)
