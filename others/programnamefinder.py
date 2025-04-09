import json
from datetime import datetime

# JSON dosyasını aç ve oku
today_date = datetime.now().strftime("%Y-%m-%d")
json_filename = f"weekly_tv_schedule_fixed_final_2025-02-02.json"

with open(json_filename, "r", encoding="utf-8") as json_file:
    weekly_schedule = json.load(json_file)

# Kanallara göre programları toplamak için sözlük
channel_programs = {}

# JSON'daki her gün için döngü
for day, channels in weekly_schedule.items():
    for channel, programs in channels.items():
        if channel not in channel_programs:
            channel_programs[channel] = set()  # Aynı programları tekrar yazmamak için SET kullanıyoruz
        
        # Program isimlerini ekleyelim
        for program in programs:
            channel_programs[channel].add(program["program"])

# **Tüm kanalları tek bir dosyaya yazalım**
output_filename = "all_channels_programs.txt"
with open(output_filename, "w", encoding="utf-8") as file:
    file.write("📺 **TÜM KANALLARDA YAYINLANAN PROGRAMLAR** 📺\n")
    file.write("="*60 + "\n\n")

    # Her kanal için programları yaz
    for channel, programs in sorted(channel_programs.items()):
        file.write(f"📡 {channel} Kanalı:\n")
        file.write("-" * 40 + "\n")
        for program in sorted(programs):  # Programları alfabetik sırayla yazalım
            file.write(program + "\n")
        file.write("\n")

print(f"Tüm kanalların program listesi başarıyla {output_filename} dosyasına yazıldı! 🎉")
