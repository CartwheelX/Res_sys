import json
from datetime import datetime, timedelta

dates = ['2025-04-26', '2025-04-27', '2025-04-28']
time_slots = [('09:00', '13:00'), ('15:00', '18:00')]
slot_duration = 15
max_groups = 47

def generate_slots(date, start, end, duration):
    slots = []
    current_time = datetime.strptime(f"{date} {start}", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(f"{date} {end}", "%Y-%m-%d %H:%M")
    while current_time + timedelta(minutes=duration) <= end_time:
        end_slot = current_time + timedelta(minutes=duration)
        slots.append(f"{current_time.strftime('%Y-%m-%d %H:%M')} - {end_slot.strftime('%H:%M')}")
        current_time = end_slot
    return slots

all_slots = []
for date in dates:
    for start, end in time_slots:
        all_slots.extend(generate_slots(date, start, end, slot_duration))

all_slots = all_slots[:max_groups]

slots_dict = {slot: None for slot in all_slots}

with open("slots.json", "w") as f:
    json.dump(slots_dict, f, indent=4)
