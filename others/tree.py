import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# TV programlarını JSON dosyasından yükle
def load_tv_schedule(filename="weekly_tv_schedule_channels_final.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# Saatleri dakika cinsine çevirme fonksiyonu
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes

# Seçilen kriterlere uygun programları içeren bir ağaç oluştur
def build_program_tree(day, start_time, end_time, selected_categories):
    schedule = load_tv_schedule()
    
    if day not in schedule:
        return None

    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)

    # Graph oluştur
    G = nx.DiGraph()
    root = "Başlangıç"

    G.add_node(root)

    program_list = []  # Seçilen programları saklamak için

    # Seçilen kategorilere ve saatlere uyan programları bul
    for channel, programs in schedule[day].items():
        for program in programs:
            program_start, program_end = program["time"].split(" - ")
            program_start_minutes = time_to_minutes(program_start)
            program_end_minutes = time_to_minutes(program_end)
            categories = program["category"].split(" ")

            if any(cat in selected_categories for cat in categories) and start_minutes <= program_start_minutes < end_minutes:
                program_list.append({
                    "channel": channel,
                    "program": program["program"],
                    "start": program_start_minutes,
                    "end": program_end_minutes,
                    "node_name": f"{channel}: {program['program']} ({program['time']})"
                })

    # Programları başlangıç saatine göre sırala
    program_list.sort(key=lambda x: x["start"])

    # Ağaç yapısını oluştur
    def add_children(parent_node, parent_end_time):
        for program in program_list:
            if program["start"] >= parent_end_time:  # Önceki programın bitiş saatinden sonra başlamalı
                G.add_edge(parent_node, program["node_name"])
                add_children(program["node_name"], program["end"])  # Özyinelemeli çağrı (recursive)

    # Kök düğüme uygun başlangıç programlarını ekleyelim
    for program in program_list:
        if program["start"] == start_minutes:
            G.add_edge(root, program["node_name"])
            add_children(program["node_name"], program["end"])

    return G

# BFS Algoritması
def bfs_traversal(G, start_node):
    visited = []
    queue = deque([start_node])

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            queue.extend(G.neighbors(node))
    
    return visited

# DFS Algoritması
def dfs_traversal(G, start_node):
    visited = []
    stack = [start_node]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            stack.extend(reversed(list(G.neighbors(node))))
    
    return visited

# Ağacı çizme fonksiyonu
def draw_tree(G, title):
    plt.figure(figsize=(12, 6))
    pos = nx.spring_layout(G, seed=42, k=0.5)  # Düğüm pozisyonlarını belirle
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=9, font_weight="bold", edge_color="gray")
    plt.title(title)
    plt.show()

# Kullanıcıdan seçimler
selected_day = "Pazartesi"
selected_start_time = "18:00"
selected_end_time = "22:00"
selected_categories = ["dram", "aksiyon"]

# Ağaç oluştur
G = build_program_tree(selected_day, selected_start_time, selected_end_time, selected_categories)

if G:
    # Ağacı görselleştir
    draw_tree(G, "TV Programları Ağaç Yapısı")

    # BFS Traversal
    bfs_result = bfs_traversal(G, "Başlangıç")
    print("BFS Traversal Sırası:")
    print(" → ".join(bfs_result))

    # DFS Traversal
    dfs_result = dfs_traversal(G, "Başlangıç")
    print("\nDFS Traversal Sırası:")
    print(" → ".join(dfs_result))
else:
    print("Belirtilen kriterlere uygun program bulunamadı.")
