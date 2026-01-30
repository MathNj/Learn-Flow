// LearnFlow Mock Data for Development
// Used for UI development when backend is not fully available

import type {
  User,
  Module,
  Topic,
  MasterySnapshot,
  ModuleProgress,
  Exercise,
  Quiz,
  StruggleAlert,
  ChatMessage,
} from './types'

// ============================================================================
// Mock Users
// ============================================================================

export const mockUsers: User[] = [
  {
    id: 'student-1',
    username: 'alice_student',
    email: 'alice@learnflow.com',
    role: 'student',
    firstName: 'Alice',
    lastName: 'Johnson',
    avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alice',
    createdAt: '2025-01-01T00:00:00Z',
  },
  {
    id: 'teacher-1',
    username: 'msmith',
    email: 'smith@learnflow.com',
    role: 'teacher',
    firstName: 'Maria',
    lastName: 'Smith',
    avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Maria',
    createdAt: '2024-12-01T00:00:00Z',
  },
]

// ============================================================================
// Mock Curriculum (8 Modules)
// ============================================================================

export const mockModules: Module[] = [
  {
    id: 1,
    title: 'Python Basics',
    description: 'Learn the fundamentals of Python programming',
    order: 1,
    estimatedHours: 4,
    topics: [
      { id: 101, moduleId: 1, title: 'Variables & Data Types', description: 'Storing and using data', order: 1, difficulty: 'beginner' },
      { id: 102, moduleId: 1, title: 'Operators', description: 'Math, comparison, and logical operators', order: 2, difficulty: 'beginner' },
      { id: 103, moduleId: 1, title: 'Input/Output', description: 'Getting input and displaying output', order: 3, difficulty: 'beginner' },
    ],
  },
  {
    id: 2,
    title: 'Control Flow',
    description: 'Control the flow of your programs with conditionals and loops',
    order: 2,
    estimatedHours: 6,
    topics: [
      { id: 201, moduleId: 2, title: 'If Statements', description: 'Making decisions in code', order: 1, difficulty: 'beginner' },
      { id: 202, moduleId: 2, title: 'Loops', description: 'For loops and while loops', order: 2, difficulty: 'intermediate' },
    ],
  },
  {
    id: 3,
    title: 'Data Structures',
    description: 'Lists, dictionaries, tuples, and sets',
    order: 3,
    estimatedHours: 8,
    topics: [
      { id: 301, moduleId: 3, title: 'Lists', description: 'Ordered collections', order: 1, difficulty: 'beginner' },
      { id: 302, moduleId: 3, title: 'Dictionaries', description: 'Key-value pairs', order: 2, difficulty: 'intermediate' },
    ],
  },
  {
    id: 4,
    title: 'Functions',
    description: 'Creating reusable code blocks',
    order: 4,
    estimatedHours: 6,
    topics: [
      { id: 401, moduleId: 4, title: 'Defining Functions', description: 'Creating your own functions', order: 1, difficulty: 'intermediate' },
      { id: 402, moduleId: 4, title: 'Parameters & Returns', description: 'Input and output', order: 2, difficulty: 'intermediate' },
    ],
  },
  {
    id: 5,
    title: 'Object-Oriented Programming',
    description: 'Classes, objects, and inheritance',
    order: 5,
    estimatedHours: 10,
    topics: [
      { id: 501, moduleId: 5, title: 'Classes & Objects', description: 'Creating classes', order: 1, difficulty: 'advanced' },
      { id: 502, moduleId: 5, title: 'Inheritance', description: 'Extending classes', order: 2, difficulty: 'advanced' },
    ],
  },
  {
    id: 6,
    title: 'File Handling',
    description: 'Reading and writing files',
    order: 6,
    estimatedHours: 4,
    topics: [
      { id: 601, moduleId: 6, title: 'Reading Files', description: 'Opening and reading', order: 1, difficulty: 'intermediate' },
      { id: 602, moduleId: 6, title: 'Writing Files', description: 'Creating and editing', order: 2, difficulty: 'intermediate' },
    ],
  },
  {
    id: 7,
    title: 'Error Handling',
    description: 'Try, except, and debugging',
    order: 7,
    estimatedHours: 5,
    topics: [
      { id: 701, moduleId: 7, title: 'Try/Except', description: 'Handling errors gracefully', order: 1, difficulty: 'intermediate' },
      { id: 702, moduleId: 7, title: 'Common Exceptions', description: 'Types of errors', order: 2, difficulty: 'intermediate' },
    ],
  },
  {
    id: 8,
    title: 'Working with Libraries',
    description: 'Using external packages and modules',
    order: 8,
    estimatedHours: 6,
    topics: [
      { id: 801, moduleId: 8, title: 'Importing Modules', description: 'Using import statements', order: 1, difficulty: 'intermediate' },
      { id: 802, moduleId: 8, title: 'Popular Libraries', description: 'random, math, datetime', order: 2, difficulty: 'intermediate' },
    ],
  },
]

// ============================================================================
// Mock Progress Data
// ============================================================================

export const mockStudentProgress: MasterySnapshot = {
  studentId: 'student-1',
  overallMastery: 65,
  level: 'Proficient',
  exerciseMastery: 72,
  quizMastery: 60,
  codeQualityMastery: 55,
  consistencyMastery: 80,
  currentStreak: 5,
  longestStreak: 12,
  modules: [
    { moduleId: 1, moduleName: 'Python Basics', mastery: 92, level: 'Mastered', topicsCompleted: 3, topicsTotal: 3 },
    { moduleId: 2, moduleName: 'Control Flow', mastery: 78, level: 'Proficient', topicsCompleted: 1, topicsTotal: 2 },
    { moduleId: 3, moduleName: 'Data Structures', mastery: 65, level: 'Proficient', topicsCompleted: 1, topicsTotal: 2 },
    { moduleId: 4, moduleName: 'Functions', mastery: 50, level: 'Learning', topicsCompleted: 1, topicsTotal: 2 },
    { moduleId: 5, moduleName: 'OOP', mastery: 30, level: 'Beginner', topicsCompleted: 0, topicsTotal: 2 },
    { moduleId: 6, moduleName: 'File Handling', mastery: 15, level: 'Beginner', topicsCompleted: 0, topicsTotal: 2 },
    { moduleId: 7, moduleName: 'Error Handling', mastery: 20, level: 'Beginner', topicsCompleted: 0, topicsTotal: 2 },
    { moduleId: 8, moduleName: 'Libraries', mastery: 10, level: 'Beginner', topicsCompleted: 0, topicsTotal: 2 },
  ],
}

// ============================================================================
// Mock Exercises
// ============================================================================

export const mockExercises: Exercise[] = [
  {
    id: 'ex-001',
    topicId: 101,
    title: 'Create Your First Variable',
    description: 'Create a variable named `message` and assign it the value "Hello, World!"',
    difficulty: 'beginner',
    starterCode: '# Create your variable here\n',
    solutionCode: 'message = "Hello, World!"\nprint(message)',
    testCases: [
      { id: 'tc-001', expectedOutput: 'Hello, World!', isHidden: false },
    ],
    hints: ['Use the assignment operator =', 'Variables store data values'],
    estimatedMinutes: 5,
  },
  {
    id: 'ex-002',
    topicId: 201,
    title: 'Write a For Loop',
    description: 'Write a for loop that prints numbers 0 to 4',
    difficulty: 'beginner',
    starterCode: '# Write your for loop here\n',
    solutionCode: 'for i in range(5):\n    print(i)',
    testCases: [
      { id: 'tc-002', expectedOutput: '0\n1\n2\n3\n4', isHidden: false },
    ],
    hints: ['Use range(5) to get numbers 0-4', 'Don\'t forget the colon after range(5)'],
    estimatedMinutes: 10,
  },
  {
    id: 'ex-003',
    topicId: 301,
    title: 'Sum List Elements',
    description: 'Write a function that returns the sum of all elements in a list',
    difficulty: 'intermediate',
    starterCode: 'def sum_list(numbers):\n    # Your code here\n    pass',
    solutionCode: 'def sum_list(numbers):\n    return sum(numbers)',
    testCases: [
      { id: 'tc-003', input: '[1, 2, 3]', expectedOutput: '6', isHidden: false },
      { id: 'tc-004', input: '[10, 20, 30]', expectedOutput: '60', isHidden: false },
    ],
    hints: ['Use the built-in sum() function', 'You can also iterate with a loop'],
    estimatedMinutes: 15,
  },
]

// ============================================================================
// Mock Quiz
// ============================================================================

export const mockQuiz: Quiz = {
  id: 'quiz-001',
  topicId: 101,
  title: 'Variables and Data Types Quiz',
  questions: [
    {
      id: 'q-001',
      question: 'Which of the following is a valid variable name in Python?',
      type: 'multiple-choice',
      options: ['2things', 'my-var', 'my_var', 'class'],
      correctAnswer: 2, // index of 'my_var'
      explanation: 'Variable names can contain letters, numbers, and underscores, but cannot start with a number or contain hyphens.',
    },
    {
      id: 'q-002',
      question: 'What will be the output of: print(type(3.14))?',
      type: 'multiple-choice',
      options: ['<class \'int\'>', '<class \'float\'>', '<class \'str\'>', '<class \'number\'>'],
      correctAnswer: 1,
      explanation: 'Numbers with decimals are floats in Python.',
    },
    {
      id: 'q-003',
      question: 'Which operator is used for string concatenation?',
      type: 'multiple-choice',
      options: ['+', '&', '.', ','],
      correctAnswer: 0,
      explanation: 'The + operator concatenates strings in Python.',
    },
  ],
}

// ============================================================================
// Mock Struggle Alerts
// ============================================================================

export const mockStruggleAlerts: StruggleAlert[] = [
  {
    id: 'alert-001',
    studentId: 'student-002',
    studentName: 'Bob Smith',
    teacherId: 'teacher-1',
    triggerType: 'repeated_error',
    severity: 'high',
    topicId: 201,
    context: {
      errorType: 'SyntaxError: expected ":"',
      errorCount: 5,
      lastCodeAttempt: 'for i in range(10)\n    print(i)',
      details: 'Student has encountered the same syntax error 5 times while working on loops.',
    },
    createdAt: '2025-01-29T14:30:00Z',
  },
  {
    id: 'alert-002',
    studentId: 'student-003',
    studentName: 'Carol Davis',
    teacherId: 'teacher-1',
    triggerType: 'time_exceeded',
    severity: 'medium',
    topicId: 301,
    context: {
      timeSpentMinutes: 15,
      lastCodeAttempt: 'def sum_list(numbers):\n    # incomplete',
      details: 'Student has spent over 10 minutes on a single exercise without progress.',
    },
    createdAt: '2025-01-29T15:45:00Z',
  },
  {
    id: 'alert-003',
    studentId: 'student-004',
    studentName: 'David Lee',
    teacherId: 'teacher-1',
    triggerType: 'low_quiz_score',
    severity: 'medium',
    topicId: 102,
    context: {
      quizScore: 35,
      details: 'Student scored 35% on the Data Types quiz.',
    },
    createdAt: '2025-01-29T16:20:00Z',
  },
  {
    id: 'alert-004',
    studentId: 'student-002',
    studentName: 'Bob Smith',
    teacherId: 'teacher-1',
    triggerType: 'keyword_phrase',
    severity: 'high',
    topicId: 201,
    context: {
      keyword: "I don't understand loops",
      details: 'Student expressed frustration with loops topic.',
    },
    createdAt: '2025-01-29T17:00:00Z',
  },
]

// ============================================================================
// Mock Chat History
// ============================================================================

export const mockChatMessages: ChatMessage[] = [
  {
    id: 'msg-001',
    role: 'user',
    content: 'What is a variable in Python?',
    timestamp: '2025-01-29T14:00:00Z',
  },
  {
    id: 'msg-002',
    role: 'assistant',
    content: 'A variable is like a container that stores data in Python. You create a variable using the assignment operator (=).\n\nExample:\n```python\nname = "Alice"\nage = 25\n```\n\nIn this example, `name` stores a string and `age` stores an integer.',
    timestamp: '2025-01-29T14:00:01Z',
    agentType: 'concepts',
  },
  {
    id: 'msg-003',
    role: 'user',
    content: 'Can you show me how to write a for loop?',
    timestamp: '2025-01-29T14:05:00Z',
  },
  {
    id: 'msg-004',
    role: 'assistant',
    content: 'Sure! A for loop in Python iterates over a sequence (like a list or range). Here\'s the basic syntax:\n\n```python\nfor i in range(5):\n    print(i)\n```\n\nThis will print numbers 0 through 4. The `range(5)` function generates numbers 0, 1, 2, 3, 4.',
    timestamp: '2025-01-29T14:05:01Z',
    agentType: 'concepts',
  },
]
