from confluent_kafka import Consumer
from confluent_kafka import KafkaError, KafkaException
import sys
from datetime import datetime

running = True

def main():
    print("Starting Kafka Consumer...")
    conf = {
        'bootstrap.servers': 'kafka_broker:9093', 
        'group.id': 'kafka_consumer',
        # 'auto.offset.reset': 'earliest', # Legge anche i messaggi più vecchi
        'auto.offset.reset': 'latest', # Legge solo i nuovi messaggi
    }

    consumer = Consumer(conf)
    
    basic_consume_loop(consumer, ['alarms'])

    
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
    print(f"Alarm received: {msg.value().decode('utf-8')}")
    

def shutdown():
        running = False

if __name__ == "__main__":
     main()

