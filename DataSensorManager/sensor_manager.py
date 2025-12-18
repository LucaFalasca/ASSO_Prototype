from confluent_kafka import Consumer, Producer
from confluent_kafka import KafkaError, KafkaException
import sys
import json
import ast

running = True

print("Starting Kafka Consumer...")
conf = {
    'bootstrap.servers': 'kafka_broker:9093', 
    'group.id': 'kafka_consumer',
    # 'auto.offset.reset': 'earliest', # Legge anche i messaggi più vecchi
    'auto.offset.reset': 'latest', # Legge solo i nuovi messaggi
}

consumer = Consumer(conf)

conf_producer_alarm = {
    'bootstrap.servers': 'kafka_broker:9092', 
    'client.id': 'alarm_producer',
}

# Create a Kafka producer instance
producer = Producer(conf_producer_alarm)

topic = 'sensors_data'
alarm_topic = 'alarms'

def main():
    basic_consume_loop(consumer, ['sensors_data'])

    
def basic_consume_loop(consumer, topics):
        try:
            print(f"Subscribing to topics: {topics}")
            consumer.subscribe(topics)
            print("Consumer started, waiting for messages...")


            print(f"Polling message from topics: {topics}")
            while running:
                msg = consumer.poll(timeout=1.0)
                if msg is None: continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                        (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    msg_process(msg)
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()

def msg_process(msg):
    print(f"Received message: {msg.value().decode('utf-8')} from topic: {msg.topic()} at offset: {msg.offset()}")
    # Trasformo la stringa in una lista di numeri
    try:    
        sensor_data = ast.literal_eval(msg.value().decode('utf-8'))
        print(f"Processed sensor data: {sensor_data}")
        if sensor_data[1] > 9:
            print("Sensor value exceeds threshold, sending alarm...")
            send_alarm(sensor_data)
    except Exception as e:
        print(f"Error processing message: {e}")
    
def send_alarm(sensor_data):
     timestamp = sensor_data[0]
     producer.produce(alarm_topic, f'Alarm: Sensor value exceeds threshold! ({timestamp})')

def shutdown():
        running = False

if __name__ == "__main__":
     main()

