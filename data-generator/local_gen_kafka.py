import json
import time
import random
from datetime import datetime, timedelta
from kafka import KafkaProducer

# Kafka configuration - matches your local_kafka connection
KAFKA_BROKER = 'localhost:9092'  # External port (map to kafka:29092 internally)
KAFKA_TOPIC = 'test-topic'

# Vehicle IDs from your sample data
VEHICLE_IDS = list(range(1000, 1050))

# Status options
STATUSES = ['active', 'idle', 'parked']

def generate_vehicle_data():
    """Generate a single vehicle data record matching the structure"""
    return {
        'vehicle_id': random.choice(VEHICLE_IDS),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'speed': round(random.uniform(0, 80), 2),
        'fuel_level': round(random.uniform(10, 100), 2),
        'engine_temp': round(random.uniform(80, 110), 2),
        'latitude': round(random.uniform(37.0, 38.0), 6),
        'longitude': round(random.uniform(-122.5, -121.5), 6),
        'odometer': random.randint(10000, 150000),
        'battery_voltage': round(random.uniform(12.0, 14.5), 2),
        'status': random.choice(STATUSES)
    }

def main():
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        # Optional: Add reliability settings
        acks='all',
        retries=3
    )
    
    print(f"Connected to Kafka broker: {KAFKA_BROKER}")
    print(f"Sending messages to topic: {KAFKA_TOPIC}")
    print("Press Ctrl+C to stop\n")
    
    message_count = 0
    
    try:
        while True:
            # Generate and send vehicle data
            vehicle_data = generate_vehicle_data()
            
            # Send to Kafka
            future = producer.send(KAFKA_TOPIC, value=vehicle_data)
            
            # Wait for confirmation
            record_metadata = future.get(timeout=10)
            
            message_count += 1
            print(f"[{message_count}] Sent: vehicle_id={vehicle_data['vehicle_id']}, "
                  f"speed={vehicle_data['speed']}, status={vehicle_data['status']}")
            
            # Wait before sending next message (adjust as needed)
            time.sleep(1)  # 1 message per second
            
    except KeyboardInterrupt:
        print(f"\n\nStopping... Sent {message_count} messages total")
    finally:
        producer.close()

if __name__ == '__main__':
    main()