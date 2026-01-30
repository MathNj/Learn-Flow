// LearnFlow API Client
// All API calls go through Kong API Gateway with JWT authentication

import type {
  ApiResponse,
  ChatMessage,
  CodeRunRequest,
  CodeRunResult,
  Exercise,
  ExerciseAttempt,
  MasterySnapshot,
  Module,
  ModuleProgress,
  Quiz,
  QuizAttempt,
  StruggleAlert,
  TutorRequest,
  TutorResponse,
  User,
} from './types'

// ============================================================================
// Configuration
// ============================================================================

const KONG_BASE_URL = process.env.NEXT_PUBLIC_KONG_BASE_URL || 'http://localhost:8080'
const API_BASE = `${KONG_BASE_URL}/api/v1`

// ============================================================================
// Error Handling
// ============================================================================

export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Unknown error' }))
    throw new ApiError(
      response.status,
      error.code || 'UNKNOWN_ERROR',
      error.message || response.statusText
    )
  }
  return response.json()
}

// ============================================================================
// Auth Client
// ============================================================================

const getAuthToken = (): string | null => {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('auth_token')
}

const setAuthToken = (token: string): void => {
  if (typeof window === 'undefined') return
  localStorage.setItem('auth_token', token)
}

const clearAuthToken = (): void => {
  if (typeof window === 'undefined') return
  localStorage.removeItem('auth_token')
}

const getAuthHeaders = (): HeadersInit => {
  const token = getAuthToken()
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

// ============================================================================
// API Client
// ============================================================================

export const api = {
  // ========================================================================
  // Auth Endpoints
  // ========================================================================

  async login(email: string, password: string): Promise<{ user: User; token: string }> {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    const data = await handleResponse<{ user: User; token: string }>(response)
    setAuthToken(data.token)
    return data
  },

  async register(data: {
    username: string
    email: string
    password: string
    role: 'student' | 'teacher'
  }): Promise<{ user: User; token: string }> {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    const result = await handleResponse<{ user: User; token: string }>(response)
    setAuthToken(result.token)
    return result
  },

  async logout(): Promise<void> {
    clearAuthToken()
  },

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE}/me`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<User>(response)
  },

  // ========================================================================
  // Module Endpoints
  // ========================================================================

  async getModules(): Promise<Module[]> {
    const response = await fetch(`${API_BASE}/modules`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<Module[]>(response)
  },

  async getModule(moduleId: number): Promise<Module> {
    const response = await fetch(`${API_BASE}/modules/${moduleId}`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<Module>(response)
  },

  async getModuleTopics(moduleId: number): Promise<{ topics: any[] }> {
    const response = await fetch(`${API_BASE}/modules/${moduleId}/topics`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<{ topics: any[] }>(response)
  },

  // ========================================================================
  // Chat & Tutor Endpoints
  // ========================================================================

  async sendChatMessage(request: TutorRequest): Promise<TutorResponse> {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(request),
    })
    return handleResponse<TutorResponse>(response)
  },

  async explainConcept(topic: string, masteryLevel: number): Promise<any> {
    const response = await fetch(`${API_BASE}/concepts/explain`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ topic, mastery_level: masteryLevel }),
    })
    return handleResponse<any>(response)
  },

  async getDebugHint(code: string, error: string, hintLevel: number): Promise<any> {
    const response = await fetch(`${API_BASE}/debug/hint`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ code, error_message: error, hint_level: hintLevel }),
    })
    return handleResponse<any>(response)
  },

  // ========================================================================
  // Code Execution Endpoints
  // ========================================================================

  async runCode(request: CodeRunRequest): Promise<CodeRunResult> {
    const response = await fetch(`${API_BASE}/code/execute`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(request),
    })
    return handleResponse<CodeRunResult>(response)
  },

  // ========================================================================
  // Progress Endpoints
  // ========================================================================

  async getProgress(studentId: string): Promise<MasterySnapshot> {
    const response = await fetch(`${API_BASE}/progress/${studentId}`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<MasterySnapshot>(response)
  },

  async getMastery(studentId: string, topicId: number): Promise<{ mastery: number; level: string }> {
    const response = await fetch(`${API_BASE}/mastery/${studentId}/${topicId}`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<{ mastery: number; level: string }>(response)
  },

  async recordProgressEvent(event: {
    studentId: string
    eventType: string
    data: Record<string, unknown>
  }): Promise<{ status: string }> {
    const response = await fetch(`${API_BASE}/progress/event`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(event),
    })
    return handleResponse<{ status: string }>(response)
  },

  // ========================================================================
  // Exercise Endpoints
  // ========================================================================

  async getExercises(filters?: { topicId?: number; difficulty?: string }): Promise<Exercise[]> {
    const params = new URLSearchParams()
    if (filters?.topicId) params.append('topicId', filters.topicId.toString())
    if (filters?.difficulty) params.append('difficulty', filters.difficulty)

    const response = await fetch(`${API_BASE}/exercises?${params}`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<Exercise[]>(response)
  },

  async generateExercise(request: {
    topicId: number
    difficulty: string
    count?: number
  }): Promise<Exercise[]> {
    const response = await fetch(`${API_BASE}/exercises/generate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(request),
    })
    return handleResponse<Exercise[]>(response)
  },

  async validateExercise(exerciseId: string, code: string): Promise<ExerciseAttempt> {
    const response = await fetch(`${API_BASE}/exercises/validate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ exercise_id: exerciseId, code }),
    })
    return handleResponse<ExerciseAttempt>(response)
  },

  // ========================================================================
  // Quiz Endpoints
  // ========================================================================

  async getQuiz(topicId?: number): Promise<Quiz> {
    const url = topicId ? `${API_BASE}/quiz?topicId=${topicId}` : `${API_BASE}/quiz`
    const response = await fetch(url, {
      headers: getAuthHeaders(),
    })
    return handleResponse<Quiz>(response)
  },

  async submitQuizAttempt(attempt: {
    quizId: string
    answers: Record<string, string | number>
  }): Promise<QuizAttempt> {
    const response = await fetch(`${API_BASE}/quiz/submit`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(attempt),
    })
    return handleResponse<QuizAttempt>(response)
  },

  // ========================================================================
  // Teacher Endpoints
  // ========================================================================

  async getAlerts(filters?: {
    severity?: string
    classId?: string
    acknowledged?: boolean
  }): Promise<StruggleAlert[]> {
    const params = new URLSearchParams()
    if (filters?.severity) params.append('severity', filters.severity)
    if (filters?.classId) params.append('classId', filters.classId)
    if (filters?.acknowledged !== undefined)
      params.append('acknowledged', filters.acknowledged.toString())

    const response = await fetch(`${API_BASE}/teacher/alerts?${params}`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<StruggleAlert[]>(response)
  },

  async acknowledgeAlert(alertId: string): Promise<{ status: string }> {
    const response = await fetch(`${API_BASE}/teacher/alerts/${alertId}/acknowledge`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({}),
    })
    return handleResponse<{ status: string }>(response)
  },

  async getStudents(filters?: {
    classId?: string
    search?: string
    sortBy?: string
  }): Promise<{ students: User[]; total: number }> {
    const params = new URLSearchParams()
    if (filters?.classId) params.append('classId', filters.classId)
    if (filters?.search) params.append('search', filters.search)
    if (filters?.sortBy) params.append('sortBy', filters.sortBy)

    const response = await fetch(`${API_BASE}/teacher/students?${params}`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<{ students: User[]; total: number }>(response)
  },

  async getStudentDetail(studentId: string): Promise<any> {
    const response = await fetch(`${API_BASE}/teacher/students/${studentId}`, {
      headers: getAuthHeaders(),
    })
    return handleResponse<any>(response)
  },

  async generateTeacherExercise(request: {
    studentId: string
    topicId: number
    difficulty: string
  }): Promise<Exercise> {
    const response = await fetch(`${API_BASE}/teacher/exercises/generate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(request),
    })
    return handleResponse<Exercise>(response)
  },

  async assignExercise(request: {
    exerciseId: string
    studentIds: string[]
    dueDate?: string
  }): Promise<{ status: string }> {
    const response = await fetch(`${API_BASE}/teacher/assignments`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(request),
    })
    return handleResponse<{ status: string }>(response)
  },
}

export default api
