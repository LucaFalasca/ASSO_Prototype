import random
from confluent_kafka import Producer
import time
from datetime import datetime


def main():
    conf = {
        'bootstrap.servers': 'kafka_broker:9092', 
        'client.id': 'kafka_producer',
    }

    # Create a Kafka producer instance
    producer = Producer(conf)

    # Define the topic and message to send
    topic = 'sensors_data'

    # Send the message to the specified topic
    i = 0
    while True:
        message = get_sensor_data()
        producer.produce(topic, f"{message}")
        time.sleep(1)
        print(f"Produced message: {message} to topic: {topic}")
        i += 1

    producer.flush()

def get_sensor_data():
    # Simulate sensor data retrieval
    sensor_data = [datetime.now().isoformat()] + [random.randint(0, 10) for _ in range(5)]
    return str(sensor_data)

if __name__ == "__main__":
    main()