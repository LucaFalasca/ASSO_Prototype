# Kafka Tutorial

This project is a simple tutorial to demonstrate the use of Apache Kafka with a producer and a consumer in a containerized environment using Docker.

## About the Project

This project consists of three main services orchestrated by Docker Compose:

* **`kafka_broker`**: A Kafka broker service using the `bitnami/kafka:latest` image. It is configured to create a topic named `test_topic` on startup.
* **`kafka_producer`**: A Python service that produces a "Hello, Kafka!" message to the `test_topic` every second.
* **`kafka_consumer`**: A Python service that consumes messages from the `test_topic` and prints them to the console.

The services are configured to start in a specific order, with the producer and consumer waiting for the Kafka broker to be healthy before they start.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Docker
* Docker Compose

### Installation and Running

1.  Clone the repository.
2.  Navigate to the project directory.
3.  Run the following command to build and start the services:
    ```sh
    docker compose up --build
    ```

## Built With

* [Docker](https://www.docker.com/)
* [Python](https://www.python.org/)
* [confluent-kafka](https://github.com/confluentinc/confluent-kafka-python)
* [Bitnami Kafka](https://bitnami.com/stack/kafka)