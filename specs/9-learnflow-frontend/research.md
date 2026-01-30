# Research: LearnFlow Frontend

**Feature**: 9-learnflow-frontend
**Date**: 2025-01-31
**Status**: Phase 0 Complete

## Overview

This document captures research findings for implementing the LearnFlow frontend with Next.js 16, Monaco Editor, and real-time WebSocket integration.

## Technology Choices

### Frontend Framework: Next.js 16 with App Router

**Decision**: Use Next.js 16.1.6 with App Router and Turbopack

**Rationale**:
- React Server Components for performance
- Built-in routing and optimization
- Excellent TypeScript support
- App Router provides modern React patterns
- Turbopack enables fast development builds

**Alternatives Considered**:
- Vite + React: Faster dev builds but requires more setup
- CRA: Deprecated and less performant

### State Management: Zustand

**Decision**: Use Zustand for client state, TanStack Query for server state

**Rationale**:
- Zustand: Simple, lightweight, no boilerplate
- TanStack Query: Excellent caching, refetching, background updates
- Separation of concerns (client vs server state)

**Alternatives Considered**:
- Redux: Too complex for this use case
- Jotai: Good but less popular

### Code Editor: Monaco Editor

**Decision**: Use @monaco-editor/react with Python configuration

**Rationale**:
- Same editor as VS Code (familiar to users)
- Excellent Python syntax highlighting
- Built-in autocomplete and IntelliSense
- 5-second execution timeout via backend

**Configuration**:
```typescript
{
  language: 'python',
  theme: 'vs-dark',
  options: {
    minimap: { enabled: false },
    fontSize: 14,
    tabSize: 4,
    automaticLayout: true
  }
}
```

### Real-Time Communication: WebSocket

**Decision**: Native WebSocket API with custom React hook

**Rationale**:
- Direct connection to WebSocket service (port 8108)
- Full control over reconnection logic
- Lightweight compared to Socket.io

**Implementation**:
- Custom `useChatWebSocket` hook
- Automatic reconnection with exponential backoff
- Message queuing during disconnection

### Testing: Vitest + Playwright

**Decision**:
- Unit/Integration: Vitest + React Testing Library
- E2E: Playwright

**Rationale**:
- Vitest: Fast, native ESM, Jest-compatible
- Playwright: Cross-browser, reliable, modern API
- Both have excellent TypeScript support

## Performance Optimization

### Code Splitting

- Route-based splitting via App Router
- Dynamic imports for large components (Monaco)
- Lazy loading for teacher dashboard charts

### Asset Optimization

- Next.js Image optimization
- Static asset caching
- CDN for production deployment

### Data Fetching

- TanStack Query for caching
- Optimistic updates for chat
- Prefetch for dashboard data

## UI/UX Considerations

### Mastery Level Colors

```typescript
const MASTERY_COLORS = {
  beginner: 'bg-red-500',      // 0-40%
  learning: 'bg-yellow-500',    // 41-70%
  proficient: 'bg-green-500',   // 71-90%
  mastered: 'bg-blue-500'       // 91-100%
}
```

### Responsive Breakpoints

```typescript
const BREAKPOINTS = {
  tablet: '768px',   // Minimum supported
  desktop: '1024px', // Target
  wide: '1280px'     // Optimal
}
```

### Loading States

- Skeleton screens for dashboard
- Spinner for code execution
- Progressive loading for chat history

## API Integration

### Endpoints

```
Base URL: http://localhost:8180 (API Gateway)

Authentication:
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout

Student:
GET    /api/v1/student/{id}/progress
GET    /api/v1/student/{id}/modules
GET    /api/v1/concepts
POST   /api/v1/concepts/explain
POST   /api/v1/execute

Teacher:
GET    /api/v1/teacher/{id}/students
GET    /api/v1/teacher/{id}/alerts
POST   /api/v1/exercises/generate
```

### WebSocket

```
URL: ws://localhost:8108/ws/chat/{student_id}
Message Format:
{
  message_id: string
  student_id: string
  timestamp: string
  type: 'ai_response' | 'chat' | 'progress' | 'alert'
  agent?: string
  content: string
}
```

## Security Considerations

### Authentication

- JWT tokens in httpOnly cookies
- Token refresh mechanism
- Protected route middleware

### Code Execution

- Sandboxed execution on backend
- 5-second timeout enforced server-side
- Output size limits

### XSS Prevention

- React auto-escaping
- Sanitized markdown for chat
- CSP headers via Next.js

## Accessibility

- Semantic HTML (nav, main, article)
- ARIA labels for interactive elements
- Keyboard navigation (Tab, Enter, Escape)
- Focus indicators (Tailwind focus:ring)
- Color contrast ratios (WCAG AA)

## Browser Compatibility

### Supported Browsers

- Chrome 120+ (primary)
- Firefox 120+
- Safari 17+
- Edge 120+

### Progressive Enhancement

- Core features work without JavaScript (basic auth)
- WebSocket fallback to polling (if needed)
- Monaco degrades gracefully (textarea fallback)

## Deployment Strategy

### Development

```bash
npm install
npm run dev    # http://localhost:3000
```

### Production

1. Build: `npm run build`
2. Start: `npm start`
3. K8s manifests via `nextjs-k8s-deploy` skill

### Environment Variables

```env
NEXT_PUBLIC_WS_URL=ws://localhost:8108
NEXT_PUBLIC_API_URL=http://localhost:8180
NEXT_PUBLIC_DEMO_MODE=false
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Open Questions

### Resolved

1. **WebSocket reconnection strategy**: Exponential backoff with max retries
2. **Monaco bundle size**: Use dynamic import to reduce initial load
3. **State management**: Zustand for client, TanStack Query for server

### No Blocking Issues

All technical decisions made. Ready for Phase 1 (design & contracts).
