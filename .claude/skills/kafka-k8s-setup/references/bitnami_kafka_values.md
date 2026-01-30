# Bitnami Kafka Helm Values Reference

This document describes the Helm values used by the kafka-k8s-setup skill when deploying the Bitnami Kafka chart.

## Chart Information

- **Repository**: https://charts.bitnami.com/bitnami
- **Chart**: bitnami/kafka
- **Version**: 30.0.0 (pinned for stability)
- **Documentation**: https://github.com/bitnami/charts/tree/main/bitnami/kafka

## Default Values

### Development Defaults

```yaml
replicaCount: 1
persistence:
  enabled: false
externalAccess:
  enabled: false
autoCreateTopicsEnable: false
resources: {}
```

### Production Overrides

```yaml
replicaCount: 3
persistence:
  enabled: true
  size: 8Gi
externalAccess:
  enabled: true
  service:
    type: LoadBalancer
    ports:
      external: 9094
resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 2000m
    memory: 4Gi
```

## Value Descriptions

### replicaCount

Number of Kafka broker pods.

- **Development**: 1 (single broker)
- **Production**: 3 (high availability)

### persistence

Persistent volume claims for Kafka data storage.

| Parameter | Default | Description |
|-----------|---------|-------------|
| enabled | false | Enable PVC creation |
| size | 8Gi | PVC size per broker |

### externalAccess

External access configuration for connecting from outside the cluster.

| Parameter | Default | Description |
|-----------|---------|-------------|
| enabled | false | Enable external service |
| service.type | LoadBalancer | Service type |
| service.ports.external | 9094 | External port |

### resources

CPU and memory requests/limits for Kafka containers.

| Parameter | Production | Description |
|-----------|------------|-------------|
| requests.cpu | 500m | Minimum CPU |
| requests.memory | 1Gi | Minimum memory |
| limits.cpu | 2000m | Maximum CPU |
| limits.memory | 4Gi | Maximum memory |

### autoCreateTopicsEnable

Controls automatic topic creation.

- **Disabled (false)**: Topics must be created explicitly using `create_topics.sh`
- **Enabled (true)**: Kafka auto-creates topics on first use

This skill disables auto-creation to ensure explicit topic management.

## Connection Strings

### Internal (Default)

```
<release>-kafka-bootstrap.<namespace>.svc.cluster.local:9092
```

Example: `my-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092`

### External (LoadBalancer)

```
<external-ip>:9094
```

Get external IP:
```bash
kubectl get svc <release>-kafka-external-bootstrap -n <namespace>
```

## Additional Resources

- [Bitnami Kafka Chart README](https://github.com/bitnami/charts/tree/main/bitnami/kafka)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
