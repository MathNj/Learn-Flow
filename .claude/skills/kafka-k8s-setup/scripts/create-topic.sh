#!/bin/bash
# Create Kafka topics

set -e

NAMESPACE="kafka"
KAFKA_POD="kafka-0"
PARTITIONS=3
REPLICATION_FACTOR=1

while [[ $# -gt 0 ]]; do
    case $1 in
        --namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        --partitions)
            PARTITIONS="$2"
            shift 2
            ;;
        --replication)
            REPLICATION_FACTOR="$2"
            shift 2
            ;;
        *)
            TOPIC_NAME="$1"
            shift
            ;;
    esac
done

if [ -z "$TOPIC_NAME" ]; then
    echo "Usage: $0 <topic-name> [--namespace <ns>] [--partitions <n>] [--replication <n>]"
    exit 1
fi

echo "Creating topic: $TOPIC_NAME"
echo "  Partitions: $PARTITIONS"
echo "  Replication Factor: $REPLICATION_FACTOR"
echo "  Namespace: $NAMESPACE"

# Create topic using kafka-topics command
kubectl exec -n "$NAMESPACE" "$KAFKA_POD" -- \
    kafka-topics.sh \
    --create \
    --if-not-exists \
    --topic "$TOPIC_NAME" \
    --partitions "$PARTITIONS" \
    --replication-factor "$REPLICATION_FACTOR" \
    --bootstrap-server localhost:9092

echo ""
echo "Topic created successfully!"
echo ""
echo "To list topics:"
echo "  kubectl exec -n $NAMESPACE $KAFKA_POD -- kafka-topics.sh --list --bootstrap-server localhost:9092"
