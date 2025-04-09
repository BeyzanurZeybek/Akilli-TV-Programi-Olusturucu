# tv_schedule_utils.py

import json

class TVScheduleUtils:
    def __init__(self, json_filename="weekly_tv_schedule_channels_final.json"):
        self.json_filename = json_filename
        self.weekly_schedule = self.load_schedule()

    def load_schedule(self):
        """ JSON dosyasını yükleyerek program verisini getirir. """
        with open(self.json_filename, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    def filter_programs(self, day, start_minutes, end_minutes, selected_categories):
        """
        Belirtilen gün ve saat aralığında, kullanıcı tercihlerine uygun programları getirir.
        """
        if day not in self.weekly_schedule:
            return []

        filtered_programs = []

        for channel, programs in self.weekly_schedule[day].items():
            for program in programs:
                program_start, program_end = program["time"].split(" - ")
                program_start_hour, program_start_minute = map(int, program_start.split(":"))
                program_end_hour, program_end_minute = map(int, program_end.split(":"))
                program_start_minutes = program_start_hour * 60 + program_start_minute
                program_end_minutes = program_end_hour * 60 + program_end_minute

                program_categories = program["category"].split(" ")

                # Eğer programın kategorilerinden biri seçilen kategorilere uyuyorsa
                if any(category in selected_categories for category in program_categories):
                    # Eğer program belirtilen saat aralığında izlenebilirse ekle
                    if program_end_minutes > start_minutes and program_start_minutes < end_minutes:
                        filtered_programs.append((channel, program_start_minutes, program_end_minutes, program))

        return filtered_programs

    def format_time(self, minutes):
        """ Dakika cinsinden verilen zamanı HH:MM formatına çevirir. """
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

