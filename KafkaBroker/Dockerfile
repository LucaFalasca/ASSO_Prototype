FROM bitnamilegacy/kafka:latest

# Installazione di yq (per gestire lo YAML dei topic)
RUN apt-get update && apt-get install -y wget && \
    wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq && \
    chmod +x /usr/bin/yq

# Configurazione Variabili d'Ambiente (ENV)
# --- Ruolo e Cluster ---
ENV KAFKA_CFG_NODE_ID=0 \
    KAFKA_CLUSTER_ID=cluster-id \
    KAFKA_CFG_PROCESS_ROLES=controller,broker

# --- Listener ---
ENV KAFKA_CFG_LISTENERS=CLIENT://:9092,EXTERNAL://:9093,CONTROLLER://:9094 \
    KAFKA_CFG_ADVERTISED_LISTENERS=CLIENT://kafka_broker:9092,EXTERNAL://kafka_broker:9093 \
    KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CLIENT:PLAINTEXT,EXTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT \
    KAFKA_CFG_INTER_BROKER_LISTENER_NAME=CLIENT

# --- Controller KRaft ---
ENV KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka_broker:9094 \
    KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER

# --- Varie ---
ENV ALLOW_PLAINTEXT_LISTENER=yes \
    KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true