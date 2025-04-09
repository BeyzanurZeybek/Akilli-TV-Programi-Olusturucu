import json
import sys
import matplotlib.pyplot as plt
import networkx as nx
'''
Kontrol edildi ağaç doğru. bfs ve dfste kullanılabilir.
'''
# ========== TV PROGRAMLARI YÜKLEME ========== #
def load_tv_schedule(filename="weekly_tv_schedule_channels_final.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# Saatleri dakika cinsine çevirme fonksiyonu
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes

# Dakikayı saat formatına çevirme fonksiyonu
def minutes_to_time(minutes):
    return f"{minutes // 60}:{minutes % 60:02d}"

# **Ağaç Yapısı Oluşturma (KANAL BAZLI & KRONOLOJİK)**
# **Ağaç Yapısı Oluşturma (KANAL BAZLI & KRONOLOJİK)**
# **Ağaç Yapısı Oluşturma (KANAL BAZLI & KRONOLOJİK)**
def build_tree(day, start_time, end_time, selected_categories):
    schedule = load_tv_schedule()

    if day not in schedule:
        print("❌ HATA: Seçilen gün için program bulunamadı!")
        return {}

    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)
    tree = {}

    # **Her kanalı düğüm olarak ekle ve programları ekleyerek ağacı oluştur**
    for channel, programs in schedule[day].items():
        filtered_programs = []

        for program in programs:
            program_start, program_end = program["time"].split(" - ")
            program_start_minutes = time_to_minutes(program_start)
            program_end_minutes = time_to_minutes(program_end)

            # **Eğer bitiş saati, başlangıç saatinden küçükse, bir sonraki güne aittir.**
            if program_end_minutes < program_start_minutes:
                program_end_minutes += 1440  # **24 saat ekle**

            categories = program["category"].split(" ")

            if any(cat in selected_categories for cat in categories) and program_end_minutes > start_minutes and program_start_minutes < end_minutes:
                filtered_programs.append({
                    "program": program["program"],
                    "start": program_start_minutes,
                    "end": program_end_minutes,
                    "duration": program_end_minutes - program_start_minutes  # **Negatif olmayacak şekilde hesaplandı**
                })

        # **Programları başlangıç saatine göre sırala ve ağaca ekle**
        filtered_programs.sort(key=lambda x: x["start"])
        if filtered_programs:
            tree[channel] = filtered_programs

    return tree



# **Ağaç Yapısını Görselleştir (KANAL BAZLI)**
def visualize_tree(tree):
    G = nx.DiGraph()  # Yönlü bir ağaç grafiği oluştur
    pos = {}  # Düğümlerin konumlarını saklayacak
    root_node = "TV Programları"
    G.add_node(root_node)
    pos[root_node] = (0, 0)

    x_offset = 0

    for channel, programs in tree.items():
        if programs:  # Sadece programları olan kanalları ekle
            G.add_node(channel)
            G.add_edge(root_node, channel)
            pos[channel] = (x_offset, -1)

            prev_program = channel  # İlk düğüm kanal olacak
            for idx, program in enumerate(programs):
                program_name = f"{program['program']} ({minutes_to_time(program['start'])} - {minutes_to_time(program['end'])})"
                G.add_node(program_name)
                G.add_edge(prev_program, program_name)  # **Önceki programı yeni düğüme bağla**
                pos[program_name] = (x_offset, -2 - idx)
                prev_program = program_name  # **Bağlantıyı güncelle**

            x_offset += 3  # Kanallar arasında boşluk bırak

    plt.figure(figsize=(12, 6))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, edge_color="gray", font_weight="bold", arrows=True)
    plt.title("TV Programları Ağaç Yapısı (Kanal Bazlı & Kronolojik)")
    plt.show()

# **Ana Çalıştırma Bloğu**
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("⚠️ Eksik parametre! Kullanım:")
        print("python build_tree.py <Gün> <Başlangıç Saati> <Bitiş Saati> <Kategori1> <Kategori2> ...")
        sys.exit(1)

    selected_day = sys.argv[1]
    selected_start_time = sys.argv[2]
    selected_end_time = sys.argv[3]
    selected_categories = sys.argv[4:]

    tree = build_tree(selected_day, selected_start_time, selected_end_time, selected_categories)

    if tree:
        visualize_tree(tree)
    else:
        print("\n⚠️ Uygun program bulunamadı.")
