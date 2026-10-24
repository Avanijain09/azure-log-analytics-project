import json
import random
import uuid
from datetime import datetime
from faker import Faker

# Faker initialize kiya fake data ke liye
fake = Faker()

def generate_log():
    # App ke common events aur devices
    event_types = ['login', 'view_item', 'view_item', 'add_to_cart', 'checkout', 'error', 'app_crash']
    devices = ['iOS', 'Android', 'Web']
    
    # Ek single log record ka JSON structure
    log_record = {
        "event_id": str(uuid.uuid4()), # Unique ID har event ke liye
        "user_id": random.randint(1000, 5000), # Random user id 1000 se 5000 ke beech
        "event_type": random.choice(event_types),
        "event_timestamp": datetime.utcnow().isoformat(),
        "location": fake.country(),
        "device": random.choice(devices)
    }
    return log_record

def generate_daily_logs(num_records=100):
    logs = [generate_log() for _ in range(num_records)]
    
    # File ka naam current date and time ke hisaab se banega
    filename = f"app_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Data ko local JSON file mein save kar rahe hain
    with open(filename, 'w') as f:
        for log in logs:
            f.write(json.dumps(log) + "\n")
            
    print(f"✅ Success! {num_records} logs successfully generate ho gaye hain aur {filename} mein save ho gaye hain.")

if __name__ == "__main__":
    # Hum ek baar mein 500 logs generate kar rahe hain
    generate_daily_logs(500)