import json
from datetime import datetime

# JSON dosyasını aç ve oku
today_date = datetime.now().strftime("%Y-%m-%d")
json_filename = f"weekly_tv_schedule_360tv_updated_2025-02-04.json"

with open(json_filename, "r", encoding="utf-8") as json_file:
    weekly_schedule = json.load(json_file)

# teve2 Programlarının Doğru Kategorileri
teve2_program_categories = {
    "Akasya Durağı": "komedi",
    "Alın Yazım": "dram",
    "Ankara'nın Dikmeni": "komedi",
    "Asi": "dram aşk",
    "BCL Maç Özetleri": "spor",
    "Ben Bilmem Eşim Bilir": "eğlence",
    "Binbir Gece": "dram aşk",
    "Bizi Birleştiren Hayat": "dram",
    "Camdaki Kız": "dram aşk",
    "Geniş Aile": "komedi",
    "Kampüsistan": "gençlik dram",
    "Kavak Yelleri": "gençlik dram",
    "Kelime Oyunu": "eğlence",
    "Maç Saati": "spor",
    "Maç Sonu": "spor",
    "Müzik": "yaşam müzik",
    "Rehber": "yaşam",
    "THY Euroleague Maç Özetleri": "spor",
    "THY Euroleague Transfer Dosyası": "spor",
    "Yalan Dünya": "komedi",
    "Çocuklar Duymasın": "komedi aile",
    "Çok Akustik": "yaşam",
    "Çok Gezenti": "yaşam",
    "Öyle Bir Geçer Zaman Ki": "dram",
    "Üç Kız Kardeş": "dram aile"
}

# Tüm günlerde teve2 kanalının programlarını güncelle
updated = False  # Güncelleme yapıldığını takip etmek için

for day, channels in weekly_schedule.items():
    if "TEVE 2" in channels:
        for program in channels["TEVE 2"]:
            program_name = program["program"]
            if program_name in teve2_program_categories:
                print(f"Güncellendi: {program_name} -> {teve2_program_categories[program_name]}")
                program["category"] = teve2_program_categories[program_name]
                updated = True

# Eğer güncelleme yapıldıysa yeni JSON'u kaydet
if updated:
    updated_json_filename = f"weekly_tv_schedule_teve2_updated_{today_date}.json"
    with open(updated_json_filename, "w", encoding="utf-8") as json_file:
        json.dump(weekly_schedule, json_file, ensure_ascii=False, indent=4)
    print(f"teve2 program kategorileri güncellendi! Yeni dosya: {updated_json_filename}")
else:
    print("⚠️ teve2 programlarında güncellenecek bir kategori bulunamadı!")
