# Implementation Plan: LearnFlow Frontend

**Branch**: `9-learnflow-frontend` | **Date**: 2025-01-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/9-learnflow-frontend/spec.md`

## Summary

Build a Next.js 16 frontend for the LearnFlow Python learning platform with Monaco editor integration, real-time AI chat via WebSocket, and dual dashboards for students and teachers. The application connects to existing FastAPI microservices (ports 8100-8109, 8180) and implements responsive design with performance targets of <3s page load and <500ms chat latency.

## Technical Context

**Language/Version**: TypeScript 5, Next.js 16.1.6
**Primary Dependencies**: React 19, @monaco-editor/react, Zustand, TanStack Query, Tailwind CSS 4, Recharts
**Storage**: Client-side state (Zustand) + server state via API Gateway (port 8180)
**Testing**: Vitest, Playwright, React Testing Library
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge) on desktop and tablet (>=768px)
**Project Type**: web (Next.js App Router)
**Performance Goals**:
- Page load: <3s on 4G
- Chat message receipt: <500ms
- Code execution: <5s
**Constraints**:
- WebSocket connection required for real-time chat
- Monaco editor for Python syntax highlighting
- Color-coded mastery levels (Red/Yellow/Green/Blue)
- Responsive design for desktop and tablet
**Scale/Scope**:
- 11 pages (3 public, 5 student, 3 teacher)
- 10+ core components (editor, chat, dashboard, etc.)
- Integration with 9 backend microservices

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Skills-First Development

**Status**: PARTIAL - This is application code, not a skill. However, we will use the `nextjs-k8s-deploy` skill which embodies deployment best practices.

**Justification**: Frontend applications are the product layer that demonstrates skills. The underlying deployment patterns are captured in the `nextjs-k8s-deploy` reusable skill.

### II. MCP Code Execution Pattern

**Status**: NOT APPLICABLE - Frontend does not use MCP tools.

### III. Test-First with Independent User Stories

**Status**: COMPLIANT

- Tests written BEFORE implementation (Red-Green-Refactor)
- User stories independently testable:
  - US1: Student Dashboard (P1)
  - US2: Code Editor (P1)
  - US3: AI Chat (P1)
  - US4: Quiz/Exercise (P2)
  - US5: Teacher Dashboard (P2)
  - US6: Authentication (P2)
- Each story has acceptance scenarios with Given-When-Then format

### IV. Spec-Driven Development

**Status**: COMPLIANT

- spec.md created before implementation
- Contains: User Scenarios (prioritized), Requirements, Success Criteria, Edge Cases
- This plan.md defines Technical Context and Project Structure

### V. Microservices with Event-Driven Architecture

**Status**: NOT APPLICABLE - Frontend connects to existing microservices via API Gateway.

**Integration Points**:
- WebSocket Service (port 8108) for real-time chat
- API Gateway (port 8180) for REST endpoints
- Code Execution Service (port 8107) for running Python

### VI. Progressive Disclosure

**Status**: COMPLIANT

- Component documentation in respective directories
- Quick start guide in quickstart.md
- Deep documentation in README and component JSDoc

### VII. Kubernetes-Native Deployment

**Status**: VIA SKILL - Will use `nextjs-k8s-deploy` skill for K8s manifests

### VIII. Observability and Logging

**Status**: COMPLIANT

- Structured console logging for debugging
- Error tracking with user-friendly messages
- Performance monitoring (page load, chat latency)
- Health checks via API Gateway

### IX. Security and Secrets Management

**Status**: COMPLIANT

- API tokens stored in environment variables (.env.local)
- No secrets hardcoded
- JWT token handling for authentication
- .env.local in .gitignore

### X. Simplicity and YAGNI

**Status**: COMPLIANT

- Using proven libraries (Zustand, TanStack Query)
- No premature abstraction
- Component-based architecture
- Minimal state management

**Overall Gate Result**: ✅ PASS - Ready for Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/9-learnflow-frontend/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output
    └── api-contracts.ts # TypeScript interfaces for API
```

### Source Code (repository root)

```text
frontend/
├── app/                      # Next.js App Router
│   ├── (auth)/              # Auth route group
│   │   ├── login/
│   │   └── register/
│   ├── (public)/            # Public route group
│   │   └── landing/
│   ├── (student)/           # Student route group
│   │   ├── dashboard/
│   │   ├── modules/
│   │   │   └── [id]/
│   │   │       └── topics/
│   │   │           └── [id]/
│   │   ├── code-lab/
│   │   └── profile/
│   ├── (teacher)/           # Teacher route group
│   │   ├── dashboard/
│   │   ├── students/
│   │   │   └── [id]/
│   │   ├── exercise-generator/
│   │   └── settings/
│   ├── api/                 # API routes (if needed)
│   ├── layout.tsx
│   └── page.tsx
├── components/              # React components
│   ├── ui/                 # Reusable UI components
│   ├── student/            # Student-specific components
│   ├── teacher/            # Teacher-specific components
│   └── layout/             # Layout components
├── lib/                    # Utilities
│   ├── hooks/              # Custom React hooks
│   ├── api/                # API client
│   ├── store/              # Zustand stores
│   └── utils/              # Helper functions
├── public/                 # Static assets
├── tests/                  # Tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
└── .env.local              # Environment variables (gitignored)
```

**Structure Decision**: Next.js App Router with route groups for logical separation (auth, public, student, teacher). Components organized by type (ui, student-specific, teacher-specific, layout).

## Complexity Tracking

> **No violations to justify.** All user stories are independent and follow YAGNI principles.
