# ADR-005: Next.js for Frontend Application Framework

> **Scope**: Frontend web application framework for student and teacher dashboards.

- **Status:** Accepted
- **Date:** 2026-01-31
- **Feature:** learnflow-frontend
- **Context:** LearnFlow platform requires a modern React-based frontend for student and teacher dashboards, real-time AI chat interface, and code editor integration. Need a framework that supports server-side rendering, excellent performance, TypeScript support, and seamless integration with backend microservices.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Defines entire frontend stack
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Remix, Vue + Nuxt, SvelteKit
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects all frontend code
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Use Next.js 16 with App Router as the frontend framework for LearnFlow web application.**

- **Framework**: Next.js 16.1.6 (App Router, not Pages Router)
- **Language**: TypeScript 5+
- **UI Library**: React 19 with Server Components
- **Styling**: Tailwind CSS 4 (inline CSS utility classes)
- **State Management**: Zustand (client state) + TanStack Query (server state)
- **Code Editor**: Monaco Editor (@monaco-editor/react)
- **Real-Time**: Native WebSocket API with custom React hook
- **Deployment**: K8s manifests via `nextjs-k8s-deploy` skill

**Architecture**:
```
┌──────────────────────────────────────────────────────┐
│                  Next.js 16 App                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐ │
│  │Server Comp. │  │Client Comp. │  │API Routes    │ │
│  │(Dashboard)  │  │(Chat UI)    │  │(Websocket)   │ │
│  └─────────────┘  └─────────────┘  └──────────────┘ │
│         │                  │                  │        │
│         ▼                  ▼                  ▼        │
│  ┌──────────────────────────────────────────────┐ │
│  │         API Gateway (port 8180)              │ │
│  └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

## Consequences

### Positive

- **Performance**: Server-side rendering (SSR) for <3s page load (meets SC-001)
- **SEO**: Built-in SEO optimization (meta tags, OpenGraph, sitemaps)
- **Developer Experience**: Excellent TypeScript support, fast refresh, built-in image optimization
- **File-Based Routing**: Intuitive route organization (app/student/dashboard/page.tsx)
- **API Routes**: Backend-for-frontend endpoints in same codebase (/api/*)
- **Streaming**: React Server Components enable progressive rendering
- **Ecosystem**: Largest React ecosystem (Vercel, Turbopack, next-auth)
- **Deployment**: K8s-ready via `nextjs-k8s-deploy` skill (Constitution Principle VII)
- **Monaco Integration**: Well-documented @monaco-editor/react integration
- **Community**: Largest Next.js community (most tutorials, examples, StackOverflow answers)

### Negative

- **Vendor Lock-in**: Next.js opinions (App Router structure, file-system routing) hard to reverse
- **Build Complexity**: Turbopack still in beta, occasional build errors
- **Server Components**: New paradigm (RSC) has learning curve, different from traditional React
- **Client/Server Split**: Need to carefully manage which components run on client vs server
- **Bundle Size**: Next.js adds ~50KB to client bundle (acceptable for SPA)
- **Data Fetching**: Multiple fetching patterns (fetch(), server actions, TanStack Query) can be confusing
- **Turbopack**: Default bundler in Next.js 16, but may have bugs in edge cases

## Alternatives Considered

### Alternative A: Remix

- **Approach**: Use Remix 2 with React Router and nested routes
- **Why Rejected**:
  - Smaller ecosystem (fewer tutorials, examples, integrations)
  - Less opinionated (more architectural decisions required)
  - No built-in image optimization (must implement manually)
  - No Server Components (client-side rendering only, slower initial load)
  - Less mature TypeScript support (more type assertion required)
  - Constitutional alignment: `nextjs-k8s-deploy` skill already exists

### Alternative B: Vue 3 + Nuxt

- **Approach**: Use Vue 3 composition API with Nuxt 3 framework
- **Why Rejected**:
  - Smaller ecosystem (fewer libraries, less hiring pool)
  - Monaco integration: @monaco-editor/vue less mature than React version
  - Less adoption in edtech market (React dominates)
  - Team expertise gap (team more familiar with React)
  - Constitutional alignment: No `nuxt-k8s-deploy` skill exists

### Alternative C: SvelteKit

- **Approach**: Use SvelteKit with Svelte 4 for reactive UI
- **Why Rejected**:
  - Smaller ecosystem (fewer libraries, less tooling support)
  - Monaco integration: No official Svelte Monaco wrapper (must build custom)
  - Less hiring pool (fewer Svelte developers vs React)
  - Newer technology (less battle-tested at scale)
  - TypeScript support: Svelte 4 TS support less mature than React

### Alternative D: Vite + Vanilla React

- **Approach**: Use Vite + React 19 without Next.js framework
- **Why Rejected**:
  - No built-in SSR (must implement server-side rendering manually)
  - No file-based routing (must implement React Router manually)
  - No API routes (must build separate Express/FastAPI backend)
  - No image optimization (must implement manually)
  - More boilerplate (10x more config vs Next.js convention)
  - Constitutional alignment: `nextjs-k8s-deploy` skill wouldn't apply

### Alternative E: Astro + Islands Architecture

- **Approach**: Use Astro for static frontend with React islands for interactivity
- **Why Rejected**:
  - Not suited for highly interactive app (real-time chat, code editor)
  - Islands architecture adds complexity for dynamic content
  - Smaller ecosystem (fewer integrations for real-time features)
  - Less optimal for SPAs (Astro optimized for content sites)
  - No built-in WebSocket API (must implement manually)

## References

- Frontend Spec: [specs/9-learnflow-frontend/spec.md](../specs/9-learnflow-frontend/spec.md)
- Frontend Plan: [specs/9-learnflow-frontend/plan.md](../specs/9-learnflow-frontend/plan.md)
- Next.js Documentation: https://nextjs.org/docs
- Next.js 16 Release Notes: https://nextjs.org/blog/next-16
- React 19 Documentation: https://react.dev
- Constitution Principle VI: [Progressive Disclosure](../.specify/memory/constitution.md#vi-progressive-disclosure)
