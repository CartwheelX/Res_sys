from flask import Flask, render_template, request
import json

app = Flask(__name__)
SLOTS_FILE = 'slots.json'

def load_slots():
    with open(SLOTS_FILE, 'r') as f:
        return json.load(f)

def save_slots(slots):
    with open(SLOTS_FILE, 'w') as f:
        json.dump(slots, f, indent=4)

def categorize_slots(slots):
    """
    Organize the slots into a nested dictionary:
    {
        'YYYY-MM-DD': {
            'morning': {slot_string: reserved_by, ...},
            'afternoon': {slot_string: reserved_by, ...}
        },
        ...
    }
    """
    categorized = {}
    for slot, reserved_by in slots.items():
        try:
            # Expects slot in the format: "YYYY-MM-DD HH:MM - HH:MM"
            date, time_range = slot.split(" ", 1)
            start_time = time_range.split(" - ")[0]
            hour = int(start_time.split(":")[0])
        except Exception as e:
            # Skip or handle unexpected slot formats
            continue

        if date not in categorized:
            categorized[date] = {"morning": {}, "afternoon": {}}
        # Morning period: 9:00 to 13:00
        if 9 <= hour < 13:
            categorized[date]["morning"][slot] = reserved_by
        # Afternoon period: 15:00 to 18:00
        elif 15 <= hour < 18:
            categorized[date]["afternoon"][slot] = reserved_by
    return categorized

@app.route('/', methods=['GET', 'POST'])
def reserve():
    slots = load_slots()
    message = ""
    
    if request.method == "POST":
        student_name = request.form.get("student_name")
        selected_slot = request.form.get("slot")
        
        if not selected_slot:
            message = "Please select a slot before submitting."
        else:
            if slots.get(selected_slot) is None:
                slots[selected_slot] = student_name
                save_slots(slots)
                message = f"Successfully reserved slot {selected_slot} for {student_name}!"
            else:
                message = f"Slot {selected_slot} is already reserved by {slots[selected_slot]}."
    
    # Categorize the slots for display
    categorized_slots = categorize_slots(slots)
    
    return render_template("reserve.html", categorized_slots=categorized_slots, message=message)

if __name__ == "__main__":
    app.run(debug=True)
