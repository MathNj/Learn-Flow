# ADR-004: OpenAI for AI-Powered Tutoring and Code Analysis

> **Scope**: AI agent capabilities for concept explanations, code review, debugging hints, and exercise generation.

- **Status:** Accepted
- **Date:** 2026-01-31
- **Feature:** learnflow-backend (Concepts, Code Review, Debug, Exercise agents)
- **Context:** LearnFlow platform requires AI-powered tutoring across 4 specialized agent services: Concepts Agent (explain Python concepts), Code Review Agent (analyze code quality), Debug Agent (provide hints), Exercise Agent (generate challenges). Need a consistent, production-grade AI API that can handle 100 concurrent student queries with <3s response time.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Core value proposition of LearnFlow
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Claude, Llama, local models
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects 4 agent services
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use OpenAI API (GPT-4 Turbo) for all AI-powered tutoring capabilities across 4 agent services.**

- **Model**: GPT-4 Turbo (gpt-4-turbo-preview) for production
- **Fallback**: GPT-3.5 Turbo for cost savings on simpler tasks
- **API Version**: OpenAI SDK 1.x+ with async/await support
- **Rate Limiting**: Circuit breaker pattern with exponential backoff
- **Token Limits**: 1000 tokens max per request (context + response)
- **Timeout**: 10 seconds per API call
- **Cost Management**: Prompt caching for common explanations, usage tracking

**Agent Services**:
```
┌───────────────────────────────────────────────────────────┐
│                      OpenAI API                           │
│                  (gpt-4-turbo-preview)                    │
└───────┬───────────────┬───────────────┬──────────────────┤
        │               │               │                  │
   ┌────▼─────┐  ┌────▼──────┐  ┌────▼─────┐  ┌──────▼──────┐
   │ Concepts │  │Code Review│  │  Debug   │  │  Exercise   │
   │  Agent   │  │  Agent    │  │  Agent   │  │   Agent     │
   └──────────┘  └───────────┘  └──────────┘  └─────────────┘
```

## Consequences

### Positive

- **Quality**: GPT-4 Turbo provides state-of-the-art reasoning for Python concepts and code analysis
- **Speed**: <3s average response time (meets performance target SC-001)
- **Ecosystem**: Mature Python SDK, extensive documentation, strong community support
- **Reliability**: 99.9% uptime SLA, redundant infrastructure, global edge deployment
- **Scalability**: Handles 100 concurrent requests via rate limiting and retries
- **Features**: Built-in function calling, JSON mode, streaming responses
- **Cost Predictability**: Pay-per-token pricing ($0.01/1K input tokens, $0.03/1K output tokens)
- **Maintenance**: No model hosting, monitoring, or infrastructure management

### Negative

- **Cost**: $0.01-0.03 per 1K tokens (estimated $50-100/month for 100 students)
- **Vendor Lock-in**: Tied to OpenAI API (hard to switch to other models later)
- **Rate Limits**: 3500 requests/minute limit (requires circuit breaker implementation)
- **Data Privacy**: Student code sent to OpenAI servers (may violate privacy requirements)
- **No Fine-Tuning**: Can't customize model for LearnFlow-specific content (unless fine-tuning)
- **Internet Dependency**: Requires internet access (can't run offline)
- **Token Limits**: 128K context window (may truncate long code submissions)

## Alternatives Considered

### Alternative A: Anthropic Claude (claude-3-opus)

- **Approach**: Use Anthropic Claude API for AI capabilities
- **Why Rejected**:
  - Slower response time (3-5s vs <3s for GPT-4 Turbo)
  - Smaller ecosystem (fewer integrations, less documentation)
  - Higher cost ($0.015/1K input vs $0.01 for GPT-4)
  - Less mature Python SDK (fewer examples, slower iteration)
  - Later adoption in market (less proven at scale)
  - Constitutional alignment: Constitution doesn't mandate specific LLM, but OpenAI is industry standard

### Alternative B: Local LLM (Llama 3, Mistral)

- **Approach**: Self-host open-source models via Ollama or vLLM
- **Why Rejected**:
  - Higher infrastructure cost (GPU instances: $300-500/month vs $50-100 for OpenAI)
  - Lower quality (Llama 3 70B scores lower than GPT-4 on benchmarks)
  - Operational burden (model monitoring, updates, scaling, GPU management)
  - Slower inference (3-5s for 70B model vs <3s for OpenAI API)
  - Higher latency (self-hosted vs OpenAI edge deployment)
  - Not aligned with "Simplicity" principle (requires ML ops expertise)

### Alternative C: Azure OpenAI

- **Approach**: Use Azure OpenAI Service (GPT-4 hosted on Azure)
- **Why Rejected**:
  - Vendor lock-in to Azure ecosystem
  - More complex setup (Azure account, Azure OpenAI resource provisioning)
  - Higher cost (Azure premium pricing vs direct OpenAI API)
  - Same model quality (GPT-4 Turbo) but with added Azure complexity
  - No clear benefit for LearnFlow use case (not enterprise scale yet)

### Alternative D: Mixed Model Strategy

- **Approach**: Use GPT-3.5 for simple tasks, GPT-4 for complex tasks, Claude for code analysis
- **Why Rejected**:
  - Increased complexity (4x more integration points, different error handling per provider)
  - Harder to test (must validate 3 different APIs)
  - No clear benefit (GPT-4 Turbo handles all use cases well)
  - Cost savings minimal (GPT-3.5 only 10x cheaper but 5x worse quality)

## References

- Backend Spec: [specs/10-learnflow-backend/spec.md](../specs/10-learnflow-backend/spec.md)
- Backend Plan: [specs/10-learnflow-backend/plan.md](../specs/10-learnflow-backend/plan.md)
- OpenAI Documentation: https://platform.openai.com/docs
- GPT-4 Turbo: https://platform.openai.com/docs/models/gpt-4-turbo
- OpenAI Python SDK: https://github.com/openai/openai-python
