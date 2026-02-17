import json
import random
from datetime import datetime, timedelta

with open('fixtures/vehicle_data_valid.ndjson', 'w') as f:
    base_time = datetime.now() - timedelta(hours=2)
    
    for i in range(100):
        record = {
            "vehicle_id": random.randint(1000, 1050),
            "timestamp": (base_time + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "speed": round(random.uniform(0, 80), 2),
            "fuel_level": round(random.uniform(10, 100), 2),
            "engine_temp": round(random.uniform(80, 110), 2),
            "latitude": round(random.uniform(37.0, 38.0), 6),
            "longitude": round(random.uniform(-122.5, -121.5), 6),
            "odometer": random.randint(10000, 150000),
            "battery_voltage": round(random.uniform(12.0, 14.5), 2),
            "status": random.choice(["active", "idle", "parked"])
        }
        f.write(json.dumps(record) + '\n')
