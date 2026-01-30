# Learn-Flow

An AI-powered Python learning platform with adaptive tutoring, real-time code execution, and mastery-based progression tracking.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Next.js Frontend                        │
│  (Dashboard, Code Editor with Monaco, Chat Interface)           │
└─────────────────────────────────────┬───────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                          API Gateway                             │
│  (Port 8080 - Unified entry point, CORS, routing)              │
└─────────────────────────────────────┬───────────────────────────┘
                                      │
                  ┌───────────────────┼───────────────────┐
                  ▼                   ▼                   ▼
         ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
         │   Kafka      │    │  PostgreSQL  │    │  Dapr        │
         │  (8 topics)  │    │   (8 tables) │    │  Sidecars    │
         └──────────────┘    └──────────────┘    └──────────────┘
                  │
                  ├─────────────────────────────────────┐
                  ▼                                     ▼
    ┌─────────────────────────────────────────────────────────────┐
│                        AI Microservices                          │
├─────────────┬─────────────┬─────────────┬──────────────────────┤
│   Port      │   Service   │  Subscribe  │      Publish         │
├─────────────┼─────────────┼─────────────┼──────────────────────┤
│    8001     │ Triage      │learning.req │ learning.resp        │
│    8002     │ Concepts    │concepts.req │ learning.resp        │
│    8003     │ Code Review │code.sub     │ learning.resp        │
│    8004     │ Debug       │debug.req    │ learning.resp        │
│    8005     │ Exercise    │-            │ exercise.gen         │
│    8006     │ Progress    │exercise.gen │ struggle.detected    │
│    8007     │ Code Exec   │-            │ progress.events      │
│    8008     │ WebSocket   │-            │ learning.resp        │
│    8009     │ Notification│struggle.det │ -                    │
└─────────────┴─────────────┴─────────────┴──────────────────────┘
```

## Features

### Student Experience
- **Adaptive Learning**: AI tutors adjust explanations based on mastery level
- **Real-time Code Execution**: Monaco editor with Python sandbox
- **Interactive Exercises**: Progressive hints, not immediate answers
- **Quiz System**: Knowledge checks with detailed feedback
- **Progress Tracking**: Mastery levels (Beginner → Mastered)
- **Streak System**: Daily learning consistency rewards

### Teacher Dashboard
- **Student Monitoring**: Real-time progress tracking
- **Struggle Alerts**: Automatic notifications when students need help
- **Exercise Generator**: AI-powered coding challenge creation
- **Class Management**: Student roster, invite links, settings

### AI Agents
| Agent | Purpose |
|-------|---------|
| Triage | Routes queries to appropriate specialist |
| Concepts | Explains Python concepts at student's level |
| Code Review | Analyzes PEP 8 style, efficiency, readability |
| Debug | Provides progressive hints (not immediate answers) |
| Exercise | Generates and validates coding challenges |
| Progress | Tracks mastery, detects struggle |

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose (for local Kafka/Postgres)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000

**Demo Accounts**:
- Student: `student@demo.com` / `demo123`
- Teacher: `teacher@demo.com` / `demo123`

### Backend Services

```bash
cd specs/8-learnflow-platform/services

# Install dependencies
pip install fastapi uvicorn websockets dapr dapr-ext-fastapi

# Start all services (requires Kafka, PostgreSQL running)
python start-all.py
```

Services run on ports 8001-8009.

### Kubernetes Deployment

```bash
# Deploy Kafka
kubectl apply -f specs/8-learnflow-platform/k8s/kafka/topics.yaml

# Deploy PostgreSQL
kubectl apply -f specs/8-learnflow-platform/k8s/postgres/deployment.yaml

# Deploy services
kubectl apply -f specs/8-learnflow-platform/k8s/services/
```

## Skills Library

This repository includes reusable Claude Skills for cloud-native development:

| Skill | Description |
|-------|-------------|
| `agents-md-gen` | Generate AGENTS.md files for codebases |
| `kafka-k8s-setup` | Deploy Kafka on Kubernetes with Helm |
| `postgres-k8s-setup` | Deploy PostgreSQL with schema migrations |
| `fastapi-dapr-agent` | Generate FastAPI microservices with Dapr |
| `mcp-code-execution` | Demonstrate MCP token efficiency pattern |
| `nextjs-k8s-deploy` | Deploy Next.js with Monaco editor |
| `docusaurus-deploy` | Initialize and deploy Docusaurus docs |
| `component-generator` | Generate React components |
| `cicd-pipeline-generator` | Generate CI/CD workflows |
| `k8s-manifest-generator` | Generate Kubernetes manifests |

See `.claude/skills/` for full list.

## Project Structure

```
learnflow/
├── frontend/                 # Next.js frontend
│   ├── app/                 # App Router pages
│   ├── components/          # React components
│   └── lib/                 # Utilities, hooks, API client
├── specs/
│   ├── 8-learnflow-platform/ # Backend microservices
│   │   ├── services/        # FastAPI services
│   │   ├── k8s/             # Kubernetes manifests
│   │   ├── db/              # Database schema
│   │   └── tests/           # Integration & E2E tests
│   └── 9-learnflow-frontend/ # Frontend specs
└── .claude/skills/           # Reusable Claude skills
```

## Environment Variables

Copy `frontend/.env.example` to `frontend/.env.local`:

```env
NEXT_PUBLIC_WS_URL=ws://localhost:8008
NEXT_PUBLIC_DEMO_MODE=false
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## Mastery Calculation

```
overall_mastery = (exercise_mastery × 0.40) +
                  (quiz_mastery × 0.30) +
                  (code_quality_mastery × 0.20) +
                  (consistency_mastery × 0.10)
```

| Score | Level | Color |
|-------|-------|-------|
| 0-40% | Beginner | Red |
| 41-70% | Learning | Yellow |
| 71-90% | Proficient | Green |
| 91-100% | Mastered | Blue |

## Struggle Detection

Triggers that alert teachers:
- Same error repeated 3× in 1 hour
- >10 minutes spent on one exercise
- Quiz score < 50%
- Keywords: "I don't understand", "I'm stuck"
- 5+ failed code executions in a row

## Testing

```bash
# Backend tests
cd specs/8-learnflow-platform
pytest tests/

# Integration tests
pytest tests/integration/test_agent_routing.py

# E2E tests
pytest tests/e2e/test_student_journey.py

# Constitution validation
pytest tests/constitution/test_constitution.py
```

## License

MIT

## Contributing

Contributions welcome! Please read our spec-driven development guidelines in `CLAUDE.md`.
