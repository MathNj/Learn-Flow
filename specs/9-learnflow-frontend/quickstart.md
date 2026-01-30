# Quick Start: LearnFlow Frontend

**Feature**: 9-learnflow-frontend
**Last Updated**: 2025-01-31

## Prerequisites

- Node.js 18+
- npm or yarn
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Development Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local`:

```env
# WebSocket Service
NEXT_PUBLIC_WS_URL=ws://localhost:8108

# API Gateway
NEXT_PUBLIC_API_URL=http://localhost:8180

# Demo Mode (set to 'true' to use simulated backend)
NEXT_PUBLIC_DEMO_MODE=false

# App URL
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 3. Start Development Server

```bash
npm run dev
```

Visit http://localhost:3000

### 4. Build for Production

```bash
npm run build
npm start
```

## Demo Accounts

For testing without backend:

```
Student: student@demo.com / demo123
Teacher: teacher@demo.com / demo123
```

Set `NEXT_PUBLIC_DEMO_MODE=true` to enable demo mode.

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Public auth pages
│   ├── (public)/          # Landing page
│   ├── (student)/         # Student dashboard & pages
│   ├── (teacher)/         # Teacher dashboard & pages
│   └── layout.tsx         # Root layout
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── student/          # Student-specific components
│   ├── teacher/          # Teacher-specific components
│   └── layout/           # Layout components
├── lib/                   # Utilities
│   ├── hooks/            # Custom React hooks
│   ├── api/              # API client
│   ├── store/            # Zustand stores
│   └── utils/            # Helper functions
└── public/               # Static assets
```

## Key Features

### For Students

1. **Dashboard** (`/student/dashboard`)
   - View progress across 8 modules
   - See color-coded mastery levels
   - Quick access to current topic

2. **Code Lab** (`/student/code-lab`)
   - Monaco editor with Python syntax
   - Execute code (5s timeout)
   - Console output display

3. **AI Chat**
   - Real-time WebSocket connection
   - Ask questions, get explanations
   - Agent responses shown with avatars

4. **Exercises & Quizzes**
   - Coding challenges with test cases
   - Multiple choice quizzes
   - Immediate feedback

### For Teachers

1. **Dashboard** (`/teacher/dashboard`)
   - View all students
   - See struggle alerts
   - Monitor class progress

2. **Student Detail** (`/teacher/students/[id]`)
   - View student progress
   - Review code attempts
   - Check quiz results

3. **Exercise Generator**
   - Create custom exercises
   - Set difficulty levels
   - Add test cases

## Testing

### Unit Tests

```bash
npm run test           # Run tests
npm run test:watch     # Watch mode
npm run test:coverage  # Coverage report
```

### E2E Tests

```bash
npm run test:e2e       # Run Playwright tests
npm run test:e2e:ui    # Playwright UI mode
```

## Common Tasks

### Add a New Page

1. Create page in appropriate route group:
   - Public: `app/(public)/page-name/page.tsx`
   - Student: `app/(student)/page-name/page.tsx`
   - Teacher: `app/(teacher)/page-name/page.tsx`

2. Use existing components from `components/`

3. Export default component:

```typescript
export default function PageName() {
  return <div>Page content</div>
}
```

### Add a New Component

1. Create in appropriate directory:
   - Reusable: `components/ui/component-name.tsx`
   - Student: `components/student/component-name.tsx`
   - Teacher: `components/teacher/component-name.tsx`

2. Use TypeScript interfaces from `contracts/api-contracts.ts`

3. Follow naming convention: PascalCase

### Connect to API

```typescript
import { API_ENDPOINTS } from '@/contracts/api-contracts'
import { apiClient } from '@/lib/api/client'

// GET request
const data = await apiClient.get(API_ENDPOINTS.STUDENT_PROGRESS(studentId))

// POST request
const result = await apiClient.post(API_ENDPOINTS.CODE_EXECUTE, {
  code: 'print("Hello")',
  language: 'python'
})
```

### Use WebSocket Hook

```typescript
import { useChatWebSocket } from '@/lib/hooks/use-websocket'

function ChatComponent({ studentId }) {
  const { sendMessage, lastMessage, readyState, isConnected } =
    useChatWebSocket(studentId, (message) => {
      console.log('Received:', message)
    })

  const handleSend = (content: string) => {
    sendMessage({ content, student_id: studentId })
  }

  return <div>{/* UI */}</div>
}
```

## Performance Tips

1. **Code Splitting**: Use dynamic imports for heavy components
   ```typescript
   const MonacoEditor = dynamic(() => import('@/components/student/MonacoEditor'), {
     loading: () => <Spinner />
   })
   ```

2. **Image Optimization**: Use Next.js Image component
   ```typescript
   import Image from 'next/image'
   ```

3. **Caching**: TanStack Query handles server state caching

4. **Bundle Size**: Run `npm run build` to check bundle size

## Troubleshooting

### WebSocket Not Connecting

- Check `NEXT_PUBLIC_WS_URL` in `.env.local`
- Verify WebSocket service is running on port 8108
- Check browser console for errors

### API Requests Failing

- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify API Gateway is running on port 8180
- Check network tab in browser DevTools

### Monaco Editor Not Loading

- Clear browser cache
- Check browser console for errors
- Verify `@monaco-editor/react` is installed

### Build Errors

- Delete `.next` directory: `rm -rf .next`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check TypeScript errors: `npm run type-check`

## Deployment

### Kubernetes

Use the `nextjs-k8s-deploy` skill to generate K8s manifests:

```bash
npx nextjs-k8s-deploy
```

This creates:
- Deployment with replicas
- Service with load balancer
- Ingress for routing
- HPA for autoscaling

### Docker

```dockerfile
# Dockerfile is generated by Next.js
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Monaco Editor Docs](https://microsoft.github.io/monaco-editor/)
- [Zustand](https://zustand-demo.pmnd.rs/)
- [TanStack Query](https://tanstack.com/query/latest)
- [Tailwind CSS](https://tailwindcss.com/docs)

## Support

For issues or questions:
1. Check this README
2. Check `research.md` for technical decisions
3. Check `data-model.md` for data structures
4. Check `contracts/api-contracts.ts` for API types
