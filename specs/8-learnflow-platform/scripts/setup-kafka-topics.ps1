# Setup Kafka Topics for LearnFlow Platform (PowerShell)
# This script creates all required Kafka topics

$ErrorActionPreference = "Stop"

$KafkaBroker = $env:KAFKA_BROKERS
if (-not $KafkaBroker) {
    $KafkaBroker = "localhost:9092"
}

$Partitions = $env:PARTITIONS
if (-not $Partitions) {
    $Partitions = "3"
}

$ReplicationFactor = $env:REPLICATION_FACTOR
if (-not $ReplicationFactor) {
    $ReplicationFactor = "1"
}

Write-Host "Creating Kafka topics for LearnFlow Platform..." -ForegroundColor Green
Write-Host "Broker: $KafkaBroker"
Write-Host "Partitions: $Partitions"
Write-Host "Replication Factor: $ReplicationFactor"
Write-Host ""

# Array of topics to create
$topics = @(
    "learning.requests",
    "concepts.requests",
    "code.submissions",
    "debug.requests",
    "exercise.generated",
    "learning.responses",
    "struggle.detected",
    "progress.events"
)

# Function to check if kafka-topics.bat exists
function Test-KafkaTools {
    $kafkaTopicsPath = Get-Command kafka-topics.bat -ErrorAction SilentlyContinue

    if (-not $kafkaTopicsPath) {
        Write-Host "Error: kafka-topics.bat not found in PATH." -ForegroundColor Red
        Write-Host "Please add Kafka bin directory to PATH or install Kafka." -ForegroundColor Yellow
        exit 1
    }

    return $kafkaTopicsPath.Source
}

# Check for Kafka tools
$kafkaTopics = Test-KafkaTools

# Create each topic
foreach ($topic in $topics) {
    Write-Host "Creating topic: $topic" -ForegroundColor Cyan

    & $kafkaTopics --create `
        --bootstrap-server $KafkaBroker `
        --topic $topic `
        --partitions $Partitions `
        --replication-factor $ReplicationFactor `
        --if-not-exists

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Topic '$topic' created successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create topic '$topic'" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✅ All Kafka topics created successfully!" -ForegroundColor Green

# List all topics
Write-Host ""
Write-Host "Current topics in Kafka:" -ForegroundColor Yellow
& $kafkaTopics --list --bootstrap-server $KafkaBroker

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
