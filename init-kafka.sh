#!/bin/bash

# Aspetta che Kafka sia attivo
echo "Aspettando che Kafka sia pronto..."
while ! kafka-topics.sh --bootstrap-server localhost:9092 --list >/dev/null 2>&1; do
  sleep 2
done

TOPIC="sensors_data"

echo "Kafka è pronto. Creo i topic..."
kafka-topics.sh --create --if-not-exists \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic $TOPIC

echo "Topic $TOPIC creato."

TOPIC="alarms"

kafka-topics.sh --create --if-not-exists \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic $TOPIC

echo "Topic $TOPIC creato."