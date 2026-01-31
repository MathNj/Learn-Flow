// LearnFlow Type Definitions

// ============================================================================
// User & Auth Types
// ============================================================================

export type UserRole = 'student' | 'teacher' | 'admin'

export interface User {
  id: string
  username: string
  email: string
  role: UserRole
  firstName?: string
  lastName?: string
  avatarUrl?: string
  createdAt: string
  lastLoginAt?: string
}

export interface Session {
  user: User
  token: string
  refreshToken: string
  expiresAt: string
}

// ============================================================================
// Module & Curriculum Types
// ============================================================================

export interface Module {
  id: number
  title: string
  description: string
  order: number
  estimatedHours: number
  topics: Topic[]
}

export interface Topic {
  id: number
  moduleId: number
  title: string
  description: string
  order: number
  difficulty: 'beginner' | 'intermediate' | 'advanced'
}

// ============================================================================
// Progress & Mastery Types
// ============================================================================

export type MasteryLevel = 'Beginner' | 'Learning' | 'Proficient' | 'Mastered'

export interface ModuleProgress {
  moduleId: number
  moduleName: string
  mastery: number // 0-100
  level: MasteryLevel
  topicsCompleted: number
  topicsTotal: number
}

export interface MasterySnapshot {
  studentId: string
  overallMastery: number // 0-100
  level: MasteryLevel
  exerciseMastery: number // 40% weight
  quizMastery: number // 30% weight
  codeQualityMastery: number // 20% weight
  consistencyMastery: number // 10% weight
  currentStreak: number
  longestStreak: number
  modules: ModuleProgress[]
}

// ============================================================================
// Chat & Tutor Types
// ============================================================================

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
  agentType?: 'concepts' | 'debug' | 'code-review' | 'exercise' | 'triage' | 'progress'
  metadata?: {
    topicId?: number
    exerciseId?: string
    codeSnippet?: string
    errorType?: string
  }
}

export interface TutorRequest {
  query: string
  studentId: string
  context?: {
    moduleId?: number
    topicId?: number
    exerciseId?: string
    lastError?: string
    codeSnippet?: string
  }
}

export interface TutorResponse {
  messageId: string
  response: string
  agentType: string
  suggestions?: string[]
}

// ============================================================================
// Code Execution Types
// ============================================================================

export interface CodeRunRequest {
  code: string
  studentId: string
  exerciseId?: string
  timeout?: number
}

export interface CodeRunResult {
  success: boolean
  output: string
  error?: string
  executionTime: number // seconds
  timeoutOccurred: boolean
  exitCode?: number
}

// ============================================================================
// Exercise Types
// ============================================================================

export interface Exercise {
  id: string
  topicId: number
  title: string
  description: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  starterCode: string
  solutionCode?: string
  testCases: TestCase[]
  hints?: string[]
  estimatedMinutes: number
}

export interface TestCase {
  id: string
  input?: string
  expectedOutput: string
  isHidden: boolean
}

export interface ExerciseAttempt {
  id: string
  exerciseId: string
  studentId: string
  code: string
  submittedAt: string
  passed: boolean
  score: number // 0-100
  feedback: string
  testResults: TestCaseResult[]
}

export interface TestCaseResult {
  testCaseId: string
  passed: boolean
  actualOutput?: string
  expectedOutput?: string
}

// ============================================================================
// Quiz Types
// ============================================================================

export interface Quiz {
  id: string
  topicId: number
  title: string
  questions: QuizQuestion[]
  timeLimit?: number // seconds
}

export interface QuizQuestion {
  id: string
  question: string
  type: 'multiple-choice' | 'code-output' | 'fill-blank'
  options?: string[]
  correctAnswer: string | number
  explanation?: string
  codeSnippet?: string
}

export interface QuizAttempt {
  id: string
  quizId: string
  studentId: string
  startedAt: string
  completedAt?: string
  answers: Record<string, string | number>
  score: number // 0-100
  passed: boolean
  timeSpent: number // seconds
}

// ============================================================================
// Struggle Alert Types
// ============================================================================

export type StruggleTrigger =
  | 'repeated_error'
  | 'time_exceeded'
  | 'low_quiz_score'
  | 'keyword_phrase'
  | 'failed_executions'

export interface StruggleAlert {
  id: string
  studentId: string
  studentName: string
  teacherId: string
  triggerType: StruggleTrigger
  severity: 'low' | 'medium' | 'high'
  topicId?: number
  context: {
    errorType?: string
    errorCount?: number
    timeSpentMinutes?: number
    quizScore?: number
    keyword?: string
    failedExecutionCount?: number
    lastCodeAttempt?: string
    details?: string
  }
  createdAt: string
  acknowledgedAt?: string
  acknowledgedBy?: string
}

// ============================================================================
// API Response Types
// ============================================================================

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

// ============================================================================
// Component Props Types
// ============================================================================

export interface MasteryRingProps {
  mastery: number
  level: MasteryLevel
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  animated?: boolean
}

export interface CodeEditorProps {
  code: string
  onChange: (code: string) => void
  onRun?: () => void
  language?: string
  readOnly?: boolean
  height?: string
  showRunButton?: boolean
  isLoading?: boolean
}

export interface TutorChatProps {
  studentId: string
  topicId?: number
  exerciseId?: string
  onCodeRequest?: () => void
  onQuizRequest?: () => void
}
