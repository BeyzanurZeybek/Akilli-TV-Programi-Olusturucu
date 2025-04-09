import json
import random
import sys
import pickle
import os  # PKL dosyasını silmek için
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

DEBUG_MODE = True  # Debug modu aç/kapat

# ========== TV PROGRAMLARI YÜKLEME ========== #
def load_tv_schedule(filename="weekly_tv_schedule_channels_final.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# Saatleri dakika cinsine çevirme fonksiyonu
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes

# Kullanıcının tercih ettiği kriterlere uygun programları seç

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



# ========== GENETİK ALGORİTMA ========== #
# Fitness fonksiyonu (Çakışmaları Engelleyen Versiyon)
def fitness(schedule, start_time, end_time):
    total_duration = 0
    category_bonus = 0
    penalty = 0
    last_end_time = time_to_minutes(start_time)

    for program in schedule:
        if program["start"] < last_end_time:  # **Çakışma varsa cezalandır**
            penalty += 100  
        else:
            total_duration += program["duration"]
            category_bonus += 10
            last_end_time = program["end"]

    return total_duration + category_bonus - penalty

# **Başlangıç popülasyonu oluştururken kategori uyumluluğunu zorunlu kıl**
def generate_population(program_list, selected_categories, size=20):
    valid_programs = [p for p in program_list if any(cat in selected_categories for cat in p["categories"])]
    population = []
    for _ in range(size):
        individual = []
        current_time = 0
        for program in sorted(valid_programs, key=lambda x: x["start"]):
            if program["start"] >= current_time:
                individual.append(program)
                current_time = program["end"]
        population.append(individual)
    return population

# **Seçim - Turnuva Seçimi**
def selection(population, start_time, end_time):
    tournament_size = 4
    selected = []
    for _ in range(len(population)):
        competitors = random.sample(population, tournament_size)
        best = max(competitors, key=lambda x: fitness(x, start_time, end_time))
        selected.append(best)
    return selected

# **Çaprazlama - Kategori Uyumluluğu ve Çakışmaları Engelleyerek**
def crossover(parent1, parent2, selected_categories):
    if len(parent1) < 2 or len(parent2) < 2:
        return parent1, parent2

    cut = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = [p.copy() for p in parent1[:cut] + parent2[cut:] if any(cat in selected_categories for cat in p["categories"])]
    child2 = [p.copy() for p in parent2[:cut] + parent1[cut:] if any(cat in selected_categories for cat in p["categories"])]

    # **Çakışmaları Engelle**
    def remove_conflicts(schedule):
        fixed_schedule = []
        current_time = 0
        for program in sorted(schedule, key=lambda x: x["start"]):
            if program["start"] >= current_time:
                fixed_schedule.append(program)
                current_time = program["end"]
        return fixed_schedule

    return remove_conflicts(child1), remove_conflicts(child2)

# **Mutasyon - Kategori Uyumluluğunu ve Çakışmaları Koruyarak**
def mutate(schedule, program_list, selected_categories, mutation_rate=0.05):
    valid_programs = [p for p in program_list if any(cat in selected_categories for cat in p["categories"])]
    if random.random() < mutation_rate and valid_programs:
        if schedule:
            mutated = schedule[:]
            mutated[random.randint(0, len(mutated) - 1)] = random.choice(valid_programs).copy()
            return crossover(mutated, mutated, selected_categories)[0]  # Çakışmaları tekrar engelle
    return schedule

# **Genetik Algoritmayı çalıştır**
def genetic_algorithm(day, start_time, end_time, selected_categories, generations=200, population_size=20):
    program_list = filter_programs(day, start_time, end_time, selected_categories)

    if not program_list:
        return None, "Uygun program bulunamadı"

    # **PKL Dosyasını Sil ve Yeni Popülasyon Başlat**
    if os.path.exists("population.pkl"):
        os.remove("population.pkl")

    population = generate_population(program_list, selected_categories, population_size)

    best_individual = None
    best_fitness = float('-inf')

    for _ in range(generations):
        selected_population = selection(population, start_time, end_time)

        next_generation = []
        for i in range(0, len(selected_population), 2):
            if i + 1 < len(selected_population):
                child1, child2 = crossover(selected_population[i], selected_population[i + 1], selected_categories)
                next_generation.extend([mutate(child1, program_list, selected_categories), mutate(child2, program_list, selected_categories)])
            else:
                next_generation.append(mutate(selected_population[i], program_list, selected_categories))

        population = next_generation

        current_best = max(population, key=lambda x: fitness(x, start_time, end_time))
        current_best_fitness = fitness(current_best, start_time, end_time)

        if current_best_fitness > best_fitness:
            best_individual = current_best
            best_fitness = current_best_fitness

    return best_individual, f"En iyi çözüm fitness skoru: {best_fitness}"

# Dakikayı saat formatına çevirme fonksiyonu (örn: 720 → "12:00")
def minutes_to_time(minutes):
    return f"{minutes // 60}:{minutes % 60:02d}"

# **Gantt Chart Gösterimi**
# **Gantt Chart Gösterimi (Saat Formatında)**
def show_gantt_chart(schedule, day, start_time, end_time):
    fig, ax = plt.subplots(figsize=(12, 6))  # Daha geniş ekran
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

    ax.set_xlabel("Zaman (Saat)")  # Açıklama değiştirildi
    ax.set_title(f"{day} - Genetik Algoritma TV İzleme Planı")
    plt.grid(axis='x', linestyle="--", alpha=0.5)
    plt.show()


# **Ana Çalıştırma Bloğu**
if __name__ == "__main__":
    selected_day, selected_start_time, selected_end_time, selected_categories = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    best_schedule, message = genetic_algorithm(selected_day, selected_start_time, selected_end_time, selected_categories)
    
    if best_schedule:
        show_gantt_chart(best_schedule, selected_day, selected_start_time, selected_end_time)