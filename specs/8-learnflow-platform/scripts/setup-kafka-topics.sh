#!/bin/bash
# Setup Kafka Topics for LearnFlow Platform
# This script creates all required Kafka topics

set -e

KAFKA_BROKER=${KAFKA_BROKER:-localhost:9092}
PARTITIONS=${PARTITIONS:-3}
REPLICATION_FACTOR=${REPLICATION_FACTOR:-1}

echo "Creating Kafka topics for LearnFlow Platform..."
echo "Broker: $KAFKA_BROKER"
echo "Partitions: $PARTITIONS"
echo "Replication Factor: $REPLICATION_FACTOR"
echo ""

# Array of topics to create
declare -a topics=(
    "learning.requests"
    "concepts.requests"
    "code.submissions"
    "debug.requests"
    "exercise.generated"
    "learning.responses"
    "struggle.detected"
    "progress.events"
)

# Create each topic
for topic in "${topics[@]}"
do
    echo "Creating topic: $topic"
    kafka-topics.sh --create \
        --bootstrap-server $KAFKA_BROKER \
        --topic "$topic" \
        --partitions $PARTITIONS \
        --replication-factor $REPLICATION_FACTOR \
        --if-not-exists
done

echo ""
echo "✅ All Kafka topics created successfully!"

# List all topics
echo ""
echo "Current topics in Kafka:"
kafka-topics.sh --list --bootstrap-server $KAFKA_BROKER

echo ""
echo "Done!"
