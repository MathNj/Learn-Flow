# Implementation Tasks: Next.js Kubernetes Deploy

**Feature**: 6-nextjs-k8s-deploy | **Branch**: `6-nextjs-k8s-deploy` | **Date**: 2025-01-27

**Specification**: [spec.md](./spec.md)

## Task Execution Rules

- Execute tasks sequentially within each phase unless marked `[P]` for parallel
- Mark tasks as `[X]` when complete
- Follow TDD: Write tests before implementation where applicable
- All tasks must pass Constitution validation before completion

---

## Phase 0: Setup (Next.js Project, TypeScript, Monaco)

**User Story**: Generate Next.js Boilerplate (US3), Monaco Editor Integration (US2)

### US0-T001: Create skill directory structure

Create `.claude/skills/nextjs-k8s-deploy/` with:
- `SKILL.md` (main skill file, <1000 tokens per SC-005)
- `scripts/` (executable deployment scripts)
- `templates/` (Next.js project templates)
- `k8s/` (Kubernetes manifest templates)
- `references/` (deep documentation)

**File**: `.claude/skills/nextjs-k8s-deploy/*`

**Test**: Directory exists with all subdirectories

### US0-T002: Create SKILL.md with progressive disclosure

Write SKILL.md following Constitution VI:
- YAML frontmatter (name, description)
- Quick start deployment (<1000 tokens when loaded)
- References to deep docs in references/
- When to use guidelines

**File**: `.claude/skills/nextjs-k8s-deploy/SKILL.md`

**Test**: SKILL.md loads in <1000 tokens

### US0-T003: Create Next.js project template [P]

Create `templates/nextjs_app/` with:
- `package.json` (Next.js, React, TypeScript dependencies)
- `tsconfig.json` (TypeScript configuration)
- `next.config.js` (Next.js configuration)
- `tailwind.config.ts` (Tailwind CSS configuration)
- `.eslintrc.json` (ESLint configuration)
- `src/app/` (App router structure)

**File**: `.claude/skills/nextjs-k8s-deploy/templates/nextjs_app/*`

**Test**: Template has all required configuration files

### US0-T004: Create Monaco editor component template [P]

Create `templates/monaco/` with:
- `MonacoEditor.tsx` (Monaco wrapper component)
- `CodePanel.tsx` (Editor + console panel layout)
- `useMonaco.ts` (Monaco initialization hook)
- `types.ts` (Monaco type definitions)

**File**: `.claude/skills/nextjs-k8s-deploy/templates/monaco/*`

**Test**: Monaco component renders without errors

---

## Phase 1: Core Implementation (Pages, Dockerfile, K8s Manifests)

**User Story**: Deploy Next.js Application (US1), Monaco Editor Integration (US2), Generate Next.js Boilerplate (US3)

### US1-T001: Create Landing Page template [P]

Create `templates/pages/landing.tsx` with:
- Hero section with CTA
- Feature highlights
- Navigation structure
- Responsive layout with Tailwind

**File**: `.claude/skills/nextjs-k8s-deploy/templates/pages/landing.tsx`

**Test**: Page renders without errors

### US1-T002: Create Login/Register Page template [P]

Create `templates/pages/auth.tsx` with:
- Login form
- Register form
- Form validation
- Error handling

**File**: `.claude/skills/nextjs-k8s-deploy/templates/pages/auth.tsx`

**Test**: Auth forms have validation

### US1-T003: Create Student Dashboard template [P]

Create `templates/pages/student-dashboard.tsx` with:
- Progress tracking display
- Module navigation
- Recent activity
- Streak counter

**File**: `.claude/skills/nextjs-k8s-deploy/templates/pages/student-dashboard.tsx`

**Test**: Dashboard displays progress data

### US1-T004: Create Code Editor Page template

Create `templates/pages/code-editor.tsx` with:
- Monaco editor integration
- Python syntax highlighting
- Code execution panel
- Output console

**File**: `.claude/skills/nextjs-k8s-deploy/templates/pages/code-editor.tsx`

**Test**: Editor renders Monaco and accepts input

### US1-T005: Create Chat Interface template [P]

Create `templates/pages/chat.tsx` with:
- Chat message list
- Message input
- AI response handling
- WebSocket integration placeholder

**File**: `.claude/skills/nextjs-k8s-deploy/templates/pages/chat.tsx`

**Test**: Chat interface accepts messages

### US1-T006: Create Quiz Interface template [P]

Create `templates/pages/quiz.tsx` with:
- Question display
- Code editor for answers
- Submit/next buttons
- Results display

**File**: `.claude/skills/nextjs-k8s-deploy/templates/pages/quiz.tsx`

**Test**: Quiz interface renders questions

### US1-T007: Create Teacher Dashboard template [P]

Create `templates/pages/teacher-dashboard.tsx` with:
- Class progress overview
- Student list with status
- Struggle alerts
- Exercise management

**File**: `.claude/skills/nextjs-k8s-deploy/templates/pages/teacher-dashboard.tsx`

**Test**: Dashboard displays class data

### US1-T008: Create Exercise Generator template [P]

Create `templates/pages/exercise-generator.tsx` with:
- Exercise form
- Preview pane
- Save/publish options
- Exercise list

**File**: `.claude/skills/nextjs-k8s-deploy/templates/pages/exercise-generator.tsx`

**Test**: Generator creates exercises

### US1-T009: Create Dockerfile template

Create `templates/Dockerfile` with:
- Multi-stage build (deps → build → production)
- Node.js base image
- Build arguments for configuration
- Production-optimized runtime
- Health check endpoint

**File**: `.claude/skills/nextjs-k8s-deploy/templates/Dockerfile`

**Test**: Dockerfile builds successfully

### US1-T010: Create Kubernetes Deployment manifest [P]

Create `k8s/deployment.yaml` template with:
- Deployment spec with replicas
- Container image reference
- Resource limits (CPU, memory)
- Environment variable injection
- Volume mounts (if needed)

**File**: `.claude/skills/nextjs-k8s-deploy/k8s/deployment.yaml`

**Test**: Manifest is valid Kubernetes YAML

### US1-T011: Create Kubernetes Service manifest [P]

Create `k8s/service.yaml` template with:
- Service type (ClusterIP/NodePort/LoadBalancer)
- Port configuration
- Selector labels

**File**: `.claude/skills/nextjs-k8s-deploy/k8s/service.yaml`

**Test**: Service exposes correct ports

### US1-T012: Create Kubernetes Ingress manifest [P]

Create `k8s/ingress.yaml` template with:
- Ingress rules for host/route
- TLS configuration placeholder
- Backend service reference

**File**: `.claude/skills/nextjs-k8s-deploy/k8s/ingress.yaml`

**Test**: Ingress routes to service

### US1-T013: Create generate_project.py script

Create deployment generator script:
- CLI argument parsing (--app-name, --pages, --features, --output)
- Template selection based on features
- File and directory creation
- Next.js project structure generation

**File**: `.claude/skills/nextjs-k8s-deploy/scripts/generate_project.py`

**Test**: Generates valid Next.js project

---

## Phase 2: Integration (Build Optimization, Health Checks, Environment)

**User Story**: Build and Deployment Optimization (US5), Environment Configuration (US4), Deploy Next.js Application (US1)

### US2-T001: Create build optimization configuration

Create build optimization settings:
- `next.config.js` with SWC minification
- Bundle analyzer configuration
- Image optimization setup
- Static generation options

**File**: `.claude/skills/nextjs-k8s-deploy/templates/next.config.optimized.js`

**Test**: Build produces optimized bundle

### US2-T002: Create health check endpoints [P]

Create health check routes:
- `/health` (liveness probe)
- `/ready` (readiness probe)
- Startup probe configuration

**File**: `.claude/skills/nextjs-k8s-deploy/templates/app/health/route.ts`

**Test**: Health endpoints return 200 OK

### US2-T003: Create environment variable handling [P]

Create environment configuration:
- `.env.example` template
- `env.ts` for runtime environment access
- Kubernetes ConfigMap template
- Kubernetes Secret template

**File**: `.claude/skills/nextjs-k8s-deploy/templates/env/*`

**Test**: Environment variables inject correctly

### US2-T004: Create deploy.sh script [P]

Create deployment script:
- Build Docker image
- Push to registry
- Apply Kubernetes manifests
- Wait for rollout completion
- Return application URL

**File**: `.claude/skills/nextjs-k8s-deploy/scripts/deploy.sh`

**Test**: Script deploys to Kubernetes successfully

### US2-T005: Create HPA manifest template [P]

Create Horizontal Pod Autoscaler manifest:
- CPU/memory utilization triggers
- Min/max replica configuration
- Target metrics

**File**: `.claude/skills/nextjs-k8s-deploy/k8s/hpa.yaml`

**Test**: HPA scales based on load

---

## Phase 3: Testing and Validation

**User Story**: All user stories

### US3-T001: Create project generation test

Test script validates:
- Project structure is correct
- All selected pages are included
- Configuration files are valid
- Project builds successfully

**File**: `.claude/skills/nextjs-k8s-deploy/tests/test_generate_project.py`

**Test**: All generation tests pass

### US3-T002: Create deployment validation script

Create validation script:
- Check pods are ready
- Verify service endpoints
- Test ingress routing
- Validate health checks

**File**: `.claude/skills/nextjs-k8s-deploy/scripts/validate_deployment.sh`

**Test**: Validates deployed application

### US3-T003: Create Monaco integration test [P]

Test Monaco component:
- Editor initializes
- Python syntax highlighting works
- Code execution panel functions
- Output displays correctly

**File**: `.claude/skills/nextjs-k8s-deploy/tests/test_monaco.py`

**Test**: Monaco integration works

### US3-T004: Create bundle size validation

Create bundle validation:
- Measure production bundle size
- Verify under 500KB gzipped (SC-004)
- Identify large dependencies

**File**: `.claude/skills/nextjs-k8s-deploy/scripts/check_bundle.sh`

**Test**: Bundle size meets requirements

### US3-T005: Constitution validation

Verify Constitution compliance:
- SC-001: Single command deployment
- SC-002: <3 minute deployment time
- SC-003: Monaco <2 second load
- SC-004: Bundle <500KB gzipped
- SC-005: SKILL.md <1000 tokens
- MCP Code Execution pattern usage
- Kubernetes-Native deployment

**Test**: All success criteria met

---

## Task Summary

| Phase | Tasks | User Stories |
|-------|-------|--------------|
| Phase 0: Setup | 4 | US2, US3 |
| Phase 1: Core | 13 | US1, US2, US3 |
| Phase 2: Integration | 5 | US1, US4, US5 |
| Phase 3: Testing | 5 | All |

**Total**: 27 tasks

**Parallel Tasks**: 8 (can execute simultaneously)
