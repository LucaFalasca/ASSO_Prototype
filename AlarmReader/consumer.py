from confluent_kafka import Consumer
from confluent_kafka import KafkaError, KafkaException
import sys
from datetime import datetime

from flask import Flask, render_template, jsonify
import threading

app = Flask(__name__)

# Stato iniziale dei rettangoli
stato_rettangoli = {
    "rettangolo_1": "white",
    "rettangolo_2": "white"
}

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint per ottenere i colori attuali
@app.route('/get_colors')
def get_colors():
    return jsonify(stato_rettangoli)

running = True

def kafka_consumer():
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
                msg = consumer.poll(timeout=0.3)
                if msg is None: 
                     stato_rettangoli["rettangolo_1"] = "white"
                     stato_rettangoli["rettangolo_2"] = "white"
                     continue

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
    if "sensor_alarm" in msg.value().decode('utf-8'):
        stato_rettangoli["rettangolo_1"] = "red"
    elif "fall_detected" in msg.value().decode('utf-8'): 
        stato_rettangoli["rettangolo_2"] = "red"   

if __name__ == "__main__":
    threading.Thread(target=kafka_consumer, daemon=True).start()
    app.run(host="0.0.0.0", port=8081, debug=True, use_reloader=False)

