# Data Model: LearnFlow Frontend

**Feature**: 9-learnflow-frontend
**Date**: 2025-01-31
**Status**: Phase 1 Complete

## Overview

This document defines the frontend data models for the LearnFlow platform. These are TypeScript interfaces that map to backend API responses and manage client-side state.

## Core Entities

### User

```typescript
interface User {
  id: string
  email: string
  name: string
  role: 'student' | 'teacher'
  created_at: string
  last_login: string
}
```

### Student

```typescript
interface Student extends User {
  role: 'student'
  current_module: number
  current_topic: number
  mastery_level: number  // 0-100
  learning_streak: number
  total_exercises: number
  completed_modules: number
}

interface Teacher extends User {
  role: 'teacher'
  class_id: string
  total_students: number
  struggling_count: number
}
```

## Learning Content

### Module

```typescript
interface Module {
  id: number
  title: string
  description: string
  order: number
  topics: Topic[]
  student_mastery?: number  // 0-100, if logged in
}

interface Topic {
  id: number
  module_id: number
  title: string
  description: string
  order: number
  concept_id: string
  exercises: Exercise[]
  quiz?: Quiz
  completed?: boolean
  mastery?: number
}
```

### Concept

```typescript
interface Concept {
  id: string
  name: string
  category: string
  explanations: {
    beginner: string
    learning: string
    proficient: string
    mastered: string
  }
  related_concepts: string[]
}
```

## Exercises and Quizzes

### Exercise

```typescript
interface Exercise {
  id: string
  topic_id: number
  title: string
  description: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  starter_code: string
  test_cases: TestCase[]
  hints: string[]
  solution?: string  // Only for teachers
}

interface TestCase {
  id: string
  input: string
  expected_output: string
  is_hidden: boolean
}
```

### Quiz

```typescript
interface Quiz {
  id: string
  topic_id: number
  questions: QuizQuestion[]
  passing_score: number
}

interface QuizQuestion {
  id: string
  question: string
  options: string[]
  correct_answer: number
  explanation: string
}
```

### QuizAttempt

```typescript
interface QuizAttempt {
  id: string
  quiz_id: string
  student_id: string
  answers: number[]
  score: number
  passed: boolean
  completed_at: string
  feedback: string
}
```

## Code Execution

### CodeSubmission

```typescript
interface CodeSubmission {
  code: string
  language: 'python'
  exercise_id?: string
}

interface ExecutionResult {
  success: boolean
  output: string
  error?: string
  execution_time: number
  timeout: boolean
}
```

## Chat and AI

### ChatMessage

```typescript
interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  agent_type?: 'triage' | 'concepts' | 'code-review' | 'debug' | 'exercise' | 'progress'
}

interface BackendWebSocketMessage {
  message_id: string
  student_id: string
  timestamp: string
  type: 'ai_response' | 'chat' | 'progress' | 'alert' | 'presence'
  agent?: string
  content: string
}
```

## Progress Tracking

### ModuleProgress

```typescript
interface ModuleProgress {
  module_id: number
  completed_topics: number
  total_topics: number
  mastery_level: number
  last_accessed: string
  status: 'not-started' | 'in-progress' | 'completed'
}

interface OverallProgress {
  modules: ModuleProgress[]
  total_mastery: number
  current_streak: number
  exercises_completed: number
  quizzes_passed: number
}
```

### MasteryLevel

```typescript
type MasteryLevel = 'beginner' | 'learning' | 'proficient' | 'mastered'

interface MasteryBreakdown {
  level: MasteryLevel
  percentage: number
  color: string
  label: string
}

// Helper function
function getMasteryLevel(score: number): MasteryLevel {
  if (score <= 40) return 'beginner'
  if (score <= 70) return 'learning'
  if (score <= 90) return 'proficient'
  return 'mastered'
}

function getMasteryColor(level: MasteryLevel): string {
  const colors = {
    beginner: 'bg-red-500',
    learning: 'bg-yellow-500',
    proficient: 'bg-green-500',
    mastered: 'bg-blue-500'
  }
  return colors[level]
}
```

## Teacher Dashboard

### StudentSummary

```typescript
interface StudentSummary {
  student_id: string
  name: string
  email: string
  mastery_level: number
  current_module: number
  streak: number
  status: 'on-track' | 'struggling' | 'inactive'
  last_active: string
  alerts?: StruggleAlert[]
}

interface StruggleAlert {
  id: string
  student_id: string
  type: 'repeated-errors' | 'stuck-on-topic' | 'low-quiz-score' | 'inactivity'
  severity: 'low' | 'medium' | 'high'
  message: string
  topic?: string
  created_at: string
  resolved: boolean
}
```

### StudentDetail

```typescript
interface StudentDetail extends StudentSummary {
  code_attempts: CodeAttempt[]
  quiz_attempts: QuizAttempt[]
  progress_by_module: ModuleProgress[]
  average_mastery: number
}

interface CodeAttempt {
  id: string
  exercise_id: string
  code: string
  success: boolean
  submitted_at: string
  feedback?: string
}
```

## State Management

### Zustand Store Structure

```typescript
// Auth Store
interface AuthStore {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  register: (data: RegisterData) => Promise<void>
}

// Student Store
interface StudentStore {
  currentModule: Module | null
  currentTopic: Topic | null
  progress: OverallProgress | null
  fetchProgress: () => Promise<void>
  setCurrentTopic: (topic: Topic) => void
}

// Chat Store
interface ChatStore {
  messages: ChatMessage[]
  isConnected: boolean
  sendMessage: (content: string) => void
  clearMessages: () => void
}

// Teacher Store
interface TeacherStore {
  students: StudentSummary[]
  alerts: StruggleAlert[]
  selectedStudent: StudentDetail | null
  fetchStudents: () => Promise<void>
  fetchStudentDetail: (id: string) => Promise<void>
}
```

## API Response Wrappers

### APIResponse

```typescript
interface APIResponse<T> {
  data: T
  error?: boolean
  message?: string
}

interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
  has_next: boolean
}
```

### Error Types

```typescript
interface APIError {
  error: true
  message: string
  code?: string
  details?: Record<string, unknown>
  request_id: string
  timestamp: string
}
```

## Form Data Types

### RegisterData

```typescript
interface RegisterData {
  email: string
  password: string
  name: string
  role: 'student' | 'teacher'
  class_code?: string  // For students joining a class
}
```

### ExerciseGeneratorData

```typescript
interface ExerciseGeneratorData {
  topic_id: number
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  concept: string
  num_test_cases: number
}
```

## Component Props

### Common Props

```typescript
interface PageProps {
  params: { id?: string }
  searchParams: { [key: string]: string | string[] | undefined }
}

interface ProtectedPageProps extends PageProps {
  user: User
}
```

## Relationships

```
User (Student/Teacher)
  ├─ Student
  │   ├─ OverallProgress
  │   │   └─ ModuleProgress[]
  │   ├─ ChatMessage[]
  │   ├─ QuizAttempt[]
  │   └─ CodeAttempt[]
  └─ Teacher
      ├─ StudentSummary[]
      ├─ StruggleAlert[]
      └─ StudentDetail

Module
  └─ Topic[]
      ├─ Exercise
      └─ Quiz
          └─ QuizQuestion
```

## Validation Rules

### Email
- Format: Standard email regex
- Required: Yes
- Unique: Yes

### Password
- Min length: 8 characters
- Required: Yes

### Name
- Min length: 2 characters
- Max length: 100 characters
- Required: Yes

### Code (Monaco)
- Max length: 10,000 characters
- Timeout: 5 seconds execution
- Language: Python only

## State Transitions

### Mastery Level Progression

```
beginner (0-40)
    ↓ [practice needed]
learning (41-70)
    ↓ [more practice]
proficient (71-90)
    ↓ [mastered concepts]
mastered (91-100)
```

### Student Status

```
inactive (7+ days no activity)
    ↓ [logged in]
on-track (active, progressing)
    ↓ [struggle detected]
struggling (repeated errors, low scores)
    ↓ [improving]
on-track
```
