"""
Tests for generator config models (US0-T002).

TDD: Tests written first, must fail before implementation.
"""
import pytest
from pydantic import ValidationError

# These imports will fail until config.py is created
# from scripts.config import ServiceType, FeatureFlag, ServiceConfig, PubSubConfig, StateConfig, InvokeConfig, AgentConfig


class TestServiceType:
    """Test ServiceType enum."""

    def test_service_type_values(self):
        """ServiceType should have all LearnFlow service types."""
        from scripts.config import ServiceType

        assert ServiceType.TRIAGE == "triage"
        assert ServiceType.CONCEPTS == "concepts"
        assert ServiceType.CODE_REVIEW == "code-review"
        assert ServiceType.DEBUG == "debug"
        assert ServiceType.EXERCISE == "exercise"
        assert ServiceType.PROGRESS == "progress"
        assert ServiceType.GENERIC == "generic"


class TestFeatureFlag:
    """Test FeatureFlag enum."""

    def test_feature_flag_values(self):
        """FeatureFlag should have all feature flags."""
        from scripts.config import FeatureFlag

        assert FeatureFlag.PUBSUB == "pubsub"
        assert FeatureFlag.STATE == "state"
        assert FeatureFlag.INVOCATION == "invocation"
        assert FeatureFlag.AGENT == "agent"
        assert FeatureFlag.HEALTH == "health"


class TestServiceConfig:
    """Test ServiceConfig model."""

    def test_valid_service_config(self):
        """ServiceConfig should validate with correct data."""
        from scripts.config import ServiceConfig, ServiceType, FeatureFlag

        config = ServiceConfig(
            service_name="test-service",
            service_type=ServiceType.TRIAGE,
            description="Test service",
        )

        assert config.service_name == "test-service"
        assert config.service_type == ServiceType.TRIAGE
        assert config.description == "Test service"
        assert config.version == "0.1.0"
        assert config.python_version == "3.11"
        assert config.port == 8000
        assert FeatureFlag.HEALTH in config.features

    def test_invalid_service_name_not_kebab_case(self):
        """ServiceConfig should reject non-kebab-case names."""
        from scripts.config import ServiceConfig, ServiceType

        with pytest.raises(ValidationError):
            ServiceConfig(
                service_name="Test_Service",  # Invalid: underscores and caps
                service_type=ServiceType.GENERIC,
                description="Invalid",
            )

    def test_invalid_port_too_low(self):
        """ServiceConfig should reject port < 1024."""
        from scripts.config import ServiceConfig, ServiceType

        with pytest.raises(ValidationError):
            ServiceConfig(
                service_name="test",
                service_type=ServiceType.GENERIC,
                description="Test",
                port=1023,
            )

    def test_invalid_port_too_high(self):
        """ServiceConfig should reject port > 65535."""
        from scripts.config import ServiceConfig, ServiceType

        with pytest.raises(ValidationError):
            ServiceConfig(
                service_name="test",
                service_type=ServiceType.GENERIC,
                description="Test",
                port=65536,
            )

    def test_agent_feature_requires_openai_model(self):
        """ServiceConfig should require openai_model when agent feature enabled."""
        from scripts.config import ServiceConfig, ServiceType, FeatureFlag

        with pytest.raises(ValidationError):
            ServiceConfig(
                service_name="test",
                service_type=ServiceType.CONCEPTS,
                description="Test",
                features=[FeatureFlag.AGENT],
                openai_model=None,  # Should be required
            )


class TestPubSubConfig:
    """Test PubSubConfig model."""

    def test_valid_pubsub_config(self):
        """PubSubConfig should validate with correct data."""
        from scripts.config import PubSubConfig, PubSubTopic

        config = PubSubConfig(
            topics=[
                PubSubTopic(
                    name="learning.query",
                    subscribe=True,
                    publish=False,
                    event_type="LearningQueryEvent",
                )
            ]
        )

        assert config.component_name == "kafka-pubsub"
        assert config.consumer_group == "learning-services"
        assert len(config.topics) == 1
        assert config.topics[0].name == "learning.query"

    def test_topic_must_subscribe_or_publish(self):
        """PubSubTopic should require at least subscribe or publish."""
        from scripts.config import PubSubTopic

        with pytest.raises(ValidationError):
            PubSubTopic(
                name="test.topic",
                subscribe=False,
                publish=False,
                event_type="TestEvent",
            )


class TestStateConfig:
    """Test StateConfig model."""

    def test_valid_state_config(self):
        """StateConfig should validate with correct data."""
        from scripts.config import StateConfig

        config = StateConfig(key_prefix="test", ttl_seconds=3600)

        assert config.component_name == "state-store"
        assert config.key_prefix == "test"
        assert config.ttl_seconds == 3600
        assert config.use_etag is True


class TestInvokeConfig:
    """Test InvokeConfig model."""

    def test_valid_invoke_config(self):
        """InvokeConfig should validate with correct data."""
        from scripts.config import InvokeConfig, InvokeTarget

        config = InvokeConfig(
            targets=[
                InvokeTarget(
                    app_id="concepts-service",
                    methods=["explain_concept"],
                    timeout_ms=5000,
                )
            ]
        )

        assert config.default_timeout_ms == 5000
        assert config.max_retries == 3
        assert len(config.targets) == 1


class TestAgentConfig:
    """Test AgentConfig model."""

    def test_valid_agent_config(self):
        """AgentConfig should validate with correct data."""
        from scripts.config import AgentConfig

        config = AgentConfig(
            model="gpt-4",
            temperature=0.7,
            max_tokens=2000,
        )

        assert config.model == "gpt-4"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
        assert config.max_history == 20

    def test_temperature_bounds(self):
        """AgentConfig should enforce temperature 0-2."""
        from scripts.config import AgentConfig

        with pytest.raises(ValidationError):
            AgentConfig(temperature=2.1)

        with pytest.raises(ValidationError):
            AgentConfig(temperature=-0.1)
