"""
Generator configuration models for FastAPI Dapr Agent (US0-T002).

Defines Pydantic models for service generation configuration.
"""
import re
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


class ServiceType(str, Enum):
    """LearnFlow microservice types."""
    TRIAGE = "triage"
    CONCEPTS = "concepts"
    CODE_REVIEW = "code-review"
    DEBUG = "debug"
    EXERCISE = "exercise"
    PROGRESS = "progress"
    GENERIC = "generic"


class FeatureFlag(str, Enum):
    """Optional features to include in generated service."""
    PUBSUB = "pubsub"
    STATE = "state"
    INVOCATION = "invocation"
    AGENT = "agent"
    HEALTH = "health"


class PubSubTopic(BaseModel):
    """Kafka topic configuration."""
    name: str = Field(..., description="Topic name")
    subscribe: bool = Field(default=True, description="Service subscribes to this topic")
    publish: bool = Field(default=False, description="Service publishes to this topic")
    event_type: str = Field(..., description="Event type name for schema")

    @model_validator(mode="after")
    def validate_subscribe_or_publish(self):
        """At least one of subscribe or publish must be True."""
        if not self.subscribe and not self.publish:
            raise ValueError("At least one of 'subscribe' or 'publish' must be True")
        return self


class PubSubConfig(BaseModel):
    """Dapr pub/sub configuration."""
    component_name: str = Field(default="kafka-pubsub", description="Dapr component name")
    topics: List[PubSubTopic] = Field(default_factory=list, description="Topics to subscribe/publish")
    consumer_group: str = Field(default="learning-services", description="Kafka consumer group")


class StateConfig(BaseModel):
    """Dapr state store configuration."""
    component_name: str = Field(default="state-store", description="Dapr state component name")
    key_prefix: str = Field(default="", description="Prefix for all state keys")
    ttl_seconds: Optional[int] = Field(default=None, description="Default TTL for state entries")
    use_etag: bool = Field(default=True, description="Use ETag for optimistic concurrency")

    @field_validator("ttl_seconds")
    @classmethod
    def validate_ttl(cls, v: Optional[int]) -> Optional[int]:
        """TTL must be positive if set."""
        if v is not None and v <= 0:
            raise ValueError("ttl_seconds must be positive")
        return v


class InvokeTarget(BaseModel):
    """Target service for invocation."""
    app_id: str = Field(..., description="Dapr app ID of target service")
    methods: List[str] = Field(..., description="Methods this service may call")
    timeout_ms: int = Field(default=5000, description="Invocation timeout")

    @field_validator("timeout_ms")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Timeout must be positive."""
        if v <= 0:
            raise ValueError("timeout_ms must be positive")
        return v


class InvokeConfig(BaseModel):
    """Dapr service invocation configuration."""
    targets: List[InvokeTarget] = Field(default_factory=list, description="Services this may invoke")
    default_timeout_ms: int = Field(default=5000, description="Default timeout")
    max_retries: int = Field(default=3, description="Default retry count")

    @field_validator("max_retries")
    @classmethod
    def validate_retries(cls, v: int) -> int:
        """Retries must be non-negative."""
        if v < 0:
            raise ValueError("max_retries must be non-negative")
        return v


class AgentConfig(BaseModel):
    """OpenAI agent integration configuration."""
    model: str = Field(default="gpt-4", description="OpenAI model name")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Sampling temperature")
    max_tokens: int = Field(default=2000, ge=1, description="Max response tokens")
    system_prompt_template: str = Field(
        default="You are a helpful AI tutor for learning Python.",
        description="System prompt for the agent"
    )
    context_key: str = Field(
        default="conversation:{session_id}",
        description="State key pattern for conversation history"
    )
    max_history: int = Field(default=20, ge=1, description="Max messages in history")


class ServiceConfig(BaseModel):
    """Configuration for generating a FastAPI microservice."""
    service_name: str = Field(..., description="Name of the service (kebab-case)")
    service_type: ServiceType = Field(..., description="Type of microservice")
    description: str = Field(..., description="Service description for docs")
    version: str = Field(default="0.1.0", description="Initial version")
    python_version: str = Field(default="3.11", description="Python version")
    features: List[FeatureFlag] = Field(
        default_factory=lambda: [FeatureFlag.HEALTH],
        description="Features to include"
    )
    port: int = Field(default=8000, description="Application port")
    openai_model: Optional[str] = Field(default=None, description="OpenAI model for agent services")

    @field_validator("service_name")
    @classmethod
    def validate_kebab_case(cls, v: str) -> str:
        """Service name must be kebab-case (lowercase letters, numbers, hyphens)."""
        if not re.match(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$", v):
            raise ValueError(
                "service_name must be kebab-case (lowercase letters, numbers, hyphens only, "
                "must start and end with alphanumeric)"
            )
        return v

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Port must be between 1024 and 65535."""
        if not 1024 <= v <= 65535:
            raise ValueError("port must be between 1024 and 65535")
        return v

    @model_validator(mode="after")
    def validate_agent_requires_model(self):
        """Agent feature requires openai_model."""
        if FeatureFlag.AGENT in self.features and not self.openai_model:
            raise ValueError("openai_model is required when agent feature is enabled")
        return self


# Service type predefined configurations
SERVICE_TYPE_CONFIGS = {
    ServiceType.TRIAGE: {
        "features": [FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE, FeatureFlag.INVOCATION],
        "topics": [
            PubSubTopic(name="learning.query", subscribe=True, publish=False, event_type="LearningQueryEvent"),
            PubSubTopic(name="learning.routed", subscribe=False, publish=True, event_type="LearningRoutedEvent"),
        ],
        "invoke_targets": [
            InvokeTarget(app_id="concepts-service", methods=["explain_concept"]),
            InvokeTarget(app_id="code-review-service", methods=["review_code"]),
            InvokeTarget(app_id="debug-service", methods=["debug_error"]),
            InvokeTarget(app_id="exercise-service", methods=["generate_exercise"]),
            InvokeTarget(app_id="progress-service", methods=["get_progress"]),
        ],
        "state_ttl": 3600,
    },
    ServiceType.CONCEPTS: {
        "features": [FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE, FeatureFlag.AGENT],
        "topics": [
            PubSubTopic(name="learning.concept-request", subscribe=True, publish=False, event_type="ConceptRequestEvent"),
            PubSubTopic(name="learning.concept-response", subscribe=False, publish=True, event_type="ConceptResponseEvent"),
        ],
        "openai_model": "gpt-4",
        "state_ttl": 86400,
    },
    ServiceType.CODE_REVIEW: {
        "features": [FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE, FeatureFlag.AGENT],
        "topics": [
            PubSubTopic(name="code.review-request", subscribe=True, publish=False, event_type="CodeReviewRequestEvent"),
            PubSubTopic(name="code.review-feedback", subscribe=False, publish=True, event_type="CodeFeedbackEvent"),
        ],
        "openai_model": "gpt-4",
        "state_ttl": None,
    },
    ServiceType.DEBUG: {
        "features": [FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE, FeatureFlag.AGENT],
        "topics": [
            PubSubTopic(name="code.error-request", subscribe=True, publish=False, event_type="ErrorRequestEvent"),
            PubSubTopic(name="code.error-hint", subscribe=False, publish=True, event_type="ErrorHintEvent"),
        ],
        "openai_model": "gpt-4",
        "state_ttl": 86400,
    },
    ServiceType.EXERCISE: {
        "features": [FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE, FeatureFlag.AGENT],
        "topics": [
            PubSubTopic(name="exercise.request", subscribe=True, publish=False, event_type="ExerciseRequestEvent"),
            PubSubTopic(name="exercise.submission", subscribe=True, publish=False, event_type="ExerciseSubmissionEvent"),
            PubSubTopic(name="exercise.response", subscribe=False, publish=True, event_type="ExerciseResponseEvent"),
            PubSubTopic(name="exercise.graded", subscribe=False, publish=True, event_type="ExerciseGradedEvent"),
        ],
        "openai_model": "gpt-4",
        "state_ttl": None,
    },
    ServiceType.PROGRESS: {
        "features": [FeatureFlag.HEALTH, FeatureFlag.PUBSUB, FeatureFlag.STATE],
        "topics": [
            PubSubTopic(name="learning.concept-response", subscribe=True, publish=False, event_type="ConceptResponseEvent"),
            PubSubTopic(name="code.review-feedback", subscribe=True, publish=False, event_type="CodeFeedbackEvent"),
            PubSubTopic(name="exercise.graded", subscribe=True, publish=False, event_type="ExerciseGradedEvent"),
            PubSubTopic(name="struggle.alert", subscribe=False, publish=True, event_type="StruggleAlertEvent"),
        ],
        "state_ttl": None,
    },
    ServiceType.GENERIC: {
        "features": [FeatureFlag.HEALTH],
        "topics": [],
        "state_ttl": None,
    },
}


def get_service_config(service_type: ServiceType, service_name: str, description: str, **kwargs) -> ServiceConfig:
    """Get a ServiceConfig with predefined values for a service type."""
    type_config = SERVICE_TYPE_CONFIGS.get(service_type, SERVICE_TYPE_CONFIGS[ServiceType.GENERIC])

    # Build config from type defaults
    config_kwargs = {
        "service_name": service_name,
        "service_type": service_type,
        "description": description,
        "features": type_config["features"],
    }

    # Add topics if pubsub feature enabled
    if FeatureFlag.PUBSUB in type_config["features"]:
        config_kwargs["pubsub"] = PubSubConfig(topics=type_config["topics"])

    # Add state config if state feature enabled
    if FeatureFlag.STATE in type_config["features"]:
        config_kwargs["state"] = StateConfig(ttl_seconds=type_config["state_ttl"])

    # Add invoke config if invocation feature enabled
    if FeatureFlag.INVOCATION in type_config["features"] and "invoke_targets" in type_config:
        config_kwargs["invoke"] = InvokeConfig(targets=type_config["invoke_targets"])

    # Add agent config if agent feature enabled
    if FeatureFlag.AGENT in type_config["features"]:
        config_kwargs["agent"] = AgentConfig(model=type_config.get("openai_model", "gpt-4"))
        config_kwargs["openai_model"] = type_config.get("openai_model", "gpt-4")

    # Override with any provided kwargs
    config_kwargs.update(kwargs)

    return ServiceConfig(**config_kwargs)
