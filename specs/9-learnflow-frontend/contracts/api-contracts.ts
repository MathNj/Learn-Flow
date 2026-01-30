/**
 * API Contracts for LearnFlow Frontend
 *
 * TypeScript interfaces defining the API contract between frontend and backend.
 * These types ensure type safety across the application.
 */

// ============================================================================
// Common Types
// ============================================================================

export interface APIResponse<T> {
  data: T
  error?: boolean
  message?: string
}

export interface APIError {
  error: true
  message: string
  code?: string
  details?: Record<string, unknown>
  request_id: string
  timestamp: string
}

export type MasteryLevel = 'beginner' | 'learning' | 'proficient' | 'mastered'

// ============================================================================
// Authentication
// ============================================================================

export interface RegisterRequest {
  email: string
  password: string
  name: string
  role: 'student' | 'teacher'
  class_code?: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface AuthResponse {
  user: User
  token: string
  expires_at: string
}

// ============================================================================
// User
// ============================================================================

export interface User {
  id: string
  email: string
  name: string
  role: 'student' | 'teacher'
  created_at: string
  last_login: string
}

export interface Student extends User {
  role: 'student'
  current_module: number
  current_topic: number
  mastery_level: number
  learning_streak: number
  total_exercises: number
  completed_modules: number
}

export interface Teacher extends User {
  role: 'teacher'
  class_id: string
  total_students: number
  struggling_count: number
}

// ============================================================================
// Learning Content
// ============================================================================

export interface Module {
  id: number
  title: string
  description: string
  order: number
  topics: Topic[]
  student_mastery?: number
}

export interface Topic {
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

export interface Concept {
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

export interface ConceptExplainRequest {
  query_id: string
  student_id: string
  concept: string
  mastery_level: number
}

export interface ConceptExplainResponse {
  query_id: string
  concept: string
  explanation: string
  level: MasteryLevel
  related_concepts: string[]
}

// ============================================================================
// Exercises
// ============================================================================

export interface Exercise {
  id: string
  topic_id: number
  title: string
  description: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  starter_code: string
  test_cases: TestCase[]
  hints: string[]
  solution?: string
}

export interface TestCase {
  id: string
  input: string
  expected_output: string
  is_hidden: boolean
}

export interface ExerciseGeneratorRequest {
  topic_id: number
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  concept: string
  num_test_cases: number
}

export interface ExerciseGeneratorResponse {
  exercise: Exercise
}

// ============================================================================
// Quizzes
// ============================================================================

export interface Quiz {
  id: string
  topic_id: number
  questions: QuizQuestion[]
  passing_score: number
}

export interface QuizQuestion {
  id: string
  question: string
  options: string[]
  correct_answer: number
  explanation: string
}

export interface QuizAttempt {
  id: string
  quiz_id: string
  student_id: string
  answers: number[]
  score: number
  passed: boolean
  completed_at: string
  feedback: string
}

export interface QuizSubmitRequest {
  quiz_id: string
  answers: number[]
}

// ============================================================================
// Code Execution
// ============================================================================

export interface CodeExecutionRequest {
  code: string
  language: 'python'
  exercise_id?: string
}

export interface CodeExecutionResponse {
  success: boolean
  output: string
  error?: string
  execution_time: number
  timeout: boolean
}

export interface CodeReviewRequest {
  submission_id: string
  student_id: string
  code: string
  exercise_id?: string
  language: string
}

export interface CodeReviewResponse {
  submission_id: string
  feedback: string
  issues: CodeIssue[]
  score: number
  suggestions: string[]
}

export interface CodeIssue {
  line: number
  severity: 'error' | 'warning' | 'info'
  message: string
  category: 'pep8' | 'efficiency' | 'readability' | 'best-practice'
}

// ============================================================================
// Chat
// ============================================================================

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  agent_type?: 'triage' | 'concepts' | 'code-review' | 'debug' | 'exercise' | 'progress'
}

export interface ChatSendMessage {
  content: string
  student_id: string
  context?: {
    topic_id?: number
    exercise_id?: string
    mastery_level?: number
  }
}

export interface BackendWebSocketMessage {
  message_id: string
  student_id: string
  timestamp: string
  type: 'ai_response' | 'chat' | 'progress' | 'alert' | 'presence'
  agent?: string
  content: string
}

// ============================================================================
// Progress
// ============================================================================

export interface ModuleProgress {
  module_id: number
  completed_topics: number
  total_topics: number
  mastery_level: number
  last_accessed: string
  status: 'not-started' | 'in-progress' | 'completed'
}

export interface OverallProgress {
  modules: ModuleProgress[]
  total_mastery: number
  current_streak: number
  exercises_completed: number
  quizzes_passed: number
}

// ============================================================================
// Teacher Dashboard
// ============================================================================

export interface StudentSummary {
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

export interface StruggleAlert {
  id: string
  student_id: string
  type: 'repeated-errors' | 'stuck-on-topic' | 'low-quiz-score' | 'inactivity'
  severity: 'low' | 'medium' | 'high'
  message: string
  topic?: string
  created_at: string
  resolved: boolean
}

export interface StudentDetail extends StudentSummary {
  code_attempts: CodeAttempt[]
  quiz_attempts: QuizAttempt[]
  progress_by_module: ModuleProgress[]
  average_mastery: number
}

export interface CodeAttempt {
  id: string
  exercise_id: string
  code: string
  success: boolean
  submitted_at: string
  feedback?: string
}

// ============================================================================
// Debug
// ============================================================================

export interface DebugRequest {
  query_id: string
  student_id: string
  code: string
  error_message: string
  context?: string
}

export interface DebugResponse {
  query_id: string
  hint: string
  possible_causes: string[]
  suggestions: string[]
  next_step: string
}

// ============================================================================
// API Endpoint Paths
// ============================================================================

export const API_ENDPOINTS = {
  // Auth
  REGISTER: '/api/v1/auth/register',
  LOGIN: '/api/v1/auth/login',
  LOGOUT: '/api/v1/auth/logout',
  ME: '/api/v1/auth/me',

  // Student
  STUDENT_PROGRESS: (id: string) => `/api/v1/student/${id}/progress`,
  STUDENT_MODULES: (id: string) => `/api/v1/student/${id}/modules`,

  // Concepts
  CONCEPTS_LIST: '/api/v1/concepts',
  CONCEPTS_EXPLAIN: '/api/v1/concepts/explain',

  // Code
  CODE_EXECUTE: '/api/v1/execute',
  CODE_REVIEW: '/api/v1/code/review',

  // Debug
  DEBUG_HELP: '/api/v1/debug',

  // Exercises
  EXERCISES_LIST: '/api/v1/exercises',
  EXERCISES_GENERATE: '/api/v1/exercises/generate',

  // Teacher
  TEACHER_STUDENTS: (id: string) => `/api/v1/teacher/${id}/students`,
  TEACHER_ALERTS: (id: string) => `/api/v1/teacher/${id}/alerts`,
  TEACHER_STUDENT_DETAIL: (teacherId: string, studentId: string) =>
    `/api/v1/teacher/${teacherId}/students/${studentId}`,
} as const
