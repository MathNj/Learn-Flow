#!/usr/bin/env python3
"""
Generate a new FastAPI microservice with Dapr integration.

This script creates a complete microservice structure with:
- FastAPI application with Dapr pub/sub support
- Dockerfile for containerization
- Kubernetes deployment manifests
- Dapr sidecar configuration
"""
import argparse
import os
import sys
from pathlib import Path


# Templates
MAIN_PY_TEMPLATE = """import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dapr.ext.fastapi import DaprApp
from dapr.clients import DaprClient

log = logging.getLogger(__name__)

app = FastAPI(
    title="{service_title}",
    description="{service_description}",
    version="0.1.0"
)

dapr_app = DaprApp(app)


# Request/Response models
class HealthResponse(BaseModel):
    status: str
    service: str


class RequestData(BaseModel):
    data: dict


@app.get("/health", response_model=HealthResponse)
async def health_check():
    '''Health check endpoint for readiness/liveness probes'''
    return {{"status": "healthy", "service": "{service_name}"}}


@app.get("/")
async def root():
    return {{"message": "Welcome to {service_title}"}}


# Dapr Pub/Sub subscription
@dapr_app.subscribe(pubsub_name="kafka", topic="{topic_name}")
async def handle_{topic_name}_event(event_data: dict):
    '''Handle events from {topic_name} topic'''
    log.info(f"Received event: {{event_data}}")

    # Process the event
    # TODO: Add your business logic here

    return {{"status": "processed"}}


# Dapr state management example
@app.post("/state/{{user_id}}")
async def save_state(user_id: str, data: RequestData):
    '''Save state using Dapr state store'''
    with DaprClient() as dapr:
        dapr.save_state(
            store_name="statestore",
            key=f"{{user_id}}_state",
            value=data.data
        )
    return {{"status": "saved"}}


@app.get("/state/{{user_id}}")
async def get_state(user_id: str):
    '''Get state using Dapr state store'''
    with DaprClient() as dapr:
        state = dapr.get_state(
            store_name="statestore",
            key=f"{{user_id}}_state"
        )
        return state.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

REQUIREMENTS_TXT = """fastapi==0.104.0
uvicorn[standard]==0.24.0
dapr==1.14.0
pydantic==2.5.0
python-dotenv==1.0.0
"""

DOCKERFILE_TEMPLATE = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

K8S_DEPLOYMENT_TEMPLATE = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  labels:
    app: {service_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "{service_name}"
        dapr.io/app-port: "8000"
        dapr.io/config: "dapr-config"
    spec:
      containers:
      - name: {service_name}
        image: {service_name}:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---

apiVersion: v1
kind: Service
metadata:
  name: {service_name}
spec:
  type: ClusterIP
  selector:
    app: {service_name}
  ports:
  - port: 8000
    targetPort: 8000
    name: http
"""

K8S_SERVICE_TEMPLATE = """# Service is included in deployment.yaml
# This file is kept for reference
"""


def generate_service(service_name, template="pubsub", topic_name=None, namespace=None):
    """Generate a new microservice."""
    # Convert service name to title
    service_title = ' '.join(word.capitalize() for word in service_name.split('-'))
    service_description = f"{service_title} microservice with Dapr integration"

    # Determine topic name
    if topic_name is None:
        topic_name = f"{service_name.replace('-', '.')}.requests"

    # Create service directory
    service_dir = Path(service_name)
    service_dir.mkdir(parents=True, exist_ok=True)

    # Create main.py
    main_py = MAIN_PY_TEMPLATE.format(
        service_name=service_name,
        service_title=service_title,
        service_description=service_description,
        topic_name=topic_name,
    )
    (service_dir / "main.py").write_text(main_py)

    # Create requirements.txt
    (service_dir / "requirements.txt").write_text(REQUIREMENTS_TXT)

    # Create Dockerfile
    (service_dir / "Dockerfile").write_text(DOCKERFILE_TEMPLATE)

    # Create k8s-deployment.yaml
    k8s_dep = K8S_DEPLOYMENT_TEMPLATE.format(service_name=service_name)
    (service_dir / "k8s-deployment.yaml").write_text(k8s_dep)

    # Create k8s-service.yaml
    (service_dir / "k8s-service.yaml").write_text(K8S_SERVICE_TEMPLATE)

    # Create dapr.yaml (config reference)
    dapr_yaml = """# Dapr Configuration Reference
# This is for reference. Actual config is applied via annotations.

apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: dapr-config
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin:9411/api/v2/spans"
  features:
  - name: proxy
    enabled: true
"""
    (service_dir / "dapr.yaml").write_text(dapr_yaml)

    # Create .dockerignore
    (service_dir / ".dockerignore").write_text("""__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.pytest_cache
.coverage
.eggs
.git
.env
.venv
venv/
""")

    print(f"Service '{service_name}' created successfully!")
    print(f"  Location: {service_dir.absolute()}")
    print(f"  Topic: {topic_name}")
    print()
    print("Next steps:")
    print(f"  1. cd {service_name}")
    print(f"  2. Edit main.py to add your business logic")
    print(f"  3. docker build -t {service_name}:latest .")
    print(f"  4. kubectl apply -f k8s-deployment.yaml")

    return service_dir


def main():
    parser = argparse.ArgumentParser(description='Generate a FastAPI microservice with Dapr')
    parser.add_argument('service_name', help='Name of the service (kebab-case)')
    parser.add_argument('--template', choices=['pubsub', 'state', 'agent'], default='pubsub',
                       help='Service template type')
    parser.add_argument('--topic', help='Kafka topic to subscribe to')
    parser.add_argument('--namespace', help='Kubernetes namespace')

    args = parser.parse_args()

    # Validate service name
    if not args.service_name.replace('-', '').isalnum():
        print("Error: Service name must be kebab-case (lowercase letters, numbers, hyphens)")
        return 1

    try:
        generate_service(args.service_name, args.template, args.topic, args.namespace)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
