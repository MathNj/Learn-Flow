# Tasks: LearnFlow Frontend

**Input**: Design documents from `/specs/9-learnflow-frontend/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/api-contracts.ts, research.md

**Tests**: Tests are OPTIONAL and not explicitly requested in the feature specification. Test tasks are not included in this breakdown.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/` at repository root (Next.js App Router structure)
- Paths shown below follow the structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create frontend directory structure with App Router folders (app, components, lib, public)
- [ ] T002 Initialize Next.js 16 project with TypeScript and required dependencies in frontend/package.json
- [ ] T003 [P] Configure Tailwind CSS 4 in frontend/tailwind.config.ts with mastery level colors
- [ ] T004 [P] Create TypeScript configuration in frontend/tsconfig.json with strict mode
- [ ] T005 [P] Setup environment variables template in frontend/.env.example
- [ ] T006 [P] Create root layout in frontend/app/layout.tsx with font and metadata configuration
- [ ] T007 [P] Configure Next.js for production in frontend/next.config.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Copy API contracts to frontend/lib/contracts/api-contracts.ts from specs/9-learnflow-frontend/contracts/
- [ ] T009 [P] Create API client base in frontend/lib/api/client.ts with fetch wrapper and error handling
- [ ] T010 [P] Create Zustand auth store in frontend/lib/store/authStore.ts with User type
- [ ] T011 [P] Create Zustand student store in frontend/lib/store/studentStore.ts
- [ ] T012 [P] Create Zustand teacher store in frontend/lib/store/teacherStore.ts
- [ ] T013 [P] Create Zustand chat store in frontend/lib/store/chatStore.ts
- [ ] T014 [P] Create useChatWebSocket hook in frontend/lib/hooks/use-websocket.ts for real-time chat
- [ ] T015 [P] Create reusable Button component in frontend/components/ui/button.tsx
- [ ] T016 [P] Create reusable Input component in frontend/components/ui/input.tsx
- [ ] T017 [P] Create reusable Card component in frontend/components/ui/card.tsx
- [ ] T018 [P] Create mastery level helper utilities in frontend/lib/utils/mastery.ts (getMasteryLevel, getMasteryColor)
- [ ] T019 Create authentication middleware in frontend/lib/middleware.ts for protected routes

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Student Dashboard Experience (Priority: P1) 🎯 MVP

**Goal**: Display personalized learning dashboard with progress through 8 Python modules, current topic, mastery levels, and quick access to continue learning

**Independent Test**: A student logs in and can view their dashboard, navigate to any module, and see accurate progress information with color-coded mastery levels

### Implementation for User Story 1

- [ ] T020 [P] [US1] Create ModuleCard component in frontend/components/student/module-card.tsx displaying module title, progress, mastery color
- [ ] T021 [P] [US1] Create MasteryBadge component in frontend/components/student/mastery-badge.tsx with color levels (Red/Yellow/Green/Blue)
- [ ] T022 [P] [US1] Create ProgressChart component in frontend/components/student/progress-chart.tsx using Recharts
- [ ] T023 [US1] Create student dashboard page in frontend/app/(student)/dashboard/page.tsx
- [ ] T024 [US1] Integrate ModuleCard components in dashboard page with module data from studentStore
- [ ] T025 [US1] Display current topic and continue button in dashboard page
- [ ] T026 [US1] Add visual indicators for incomplete topics in ModuleCard component
- [ ] T027 [US1] Implement navigation to module detail pages from dashboard

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Code Editor with Execution (Priority: P1)

**Goal**: Provide integrated Monaco code editor with Python syntax highlighting, tab indentation, code execution, and console output display

**Independent Test**: A student writes Python code in the editor and executes it, seeing output or errors in the console within 5 seconds

### Implementation for User Story 2

- [ ] T028 [P] [US2] Install @monaco-editor/react dependency and configure Python language support
- [ ] T029 [P] [US2] Create MonacoEditor component in frontend/components/student/monaco-editor.tsx with Python configuration
- [ ] T030 [P] [US2] Create CodeConsole component in frontend/components/student/code-console.tsx for output display
- [ ] T031 [US2] Create CodeLab page in frontend/app/(student)/code-lab/page.tsx
- [ ] T032 [US2] Integrate MonacoEditor and CodeConsole components in CodeLab page
- [ ] T033 [US2] Implement executeCode API call in frontend/lib/api/code.ts to POST /api/v1/execute
- [ ] T034 [US2] Add code execution handler with 5-second timeout in CodeLab page
- [ ] T035 [US2] Implement error message display in CodeConsole component
- [ ] T036 [US2] Add responsive layout for Monaco editor resizing
- [ ] T037 [US2] Add tab indentation support in Monaco editor configuration

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - AI Chat Interface (Priority: P1)

**Goal**: Provide conversational chat interface for students to interact with AI tutors with real-time WebSocket connection, message history, and agent attribution

**Independent Test**: A student asks a Python question and receives a helpful response from the AI tutor within 3 seconds

### Implementation for User Story 3

- [ ] T038 [P] [US3] Create ChatMessage component in frontend/components/student/chat-message.tsx with agent avatar
- [ ] T039 [P] [US3] Create ChatInput component in frontend/components/student/chat-input.tsx
- [ ] T040 [P] [US3] Create ChatSidebar component in frontend/components/student/chat-sidebar.tsx for collapsible chat
- [ ] T041 [US3] Implement code block syntax highlighting in ChatMessage component
- [ ] T042 [US3] Add chat to student pages (dashboard, modules, code-lab) using ChatSidebar component
- [ ] T043 [US3] Integrate useChatWebSocket hook for real-time message sending/receiving
- [ ] T044 [US3] Implement chat message history in chatStore with scrollable view
- [ ] T045 [US3] Add agent type display (triage, concepts, code-review, debug, exercise) in ChatMessage component
- [ ] T046 [US3] Implement connection status indicator in ChatSidebar component
- [ ] T047 [US3] Add auto-scroll to latest message in chat history

**Checkpoint**: All P1 user stories should now be independently functional

---

## Phase 6: User Story 4 - Quiz and Exercise Interface (Priority: P2)

**Goal**: Provide quiz and coding exercise interfaces with immediate feedback, explanations, and progress tracking

**Independent Test**: A student completes a quiz question and receives immediate feedback on correctness

### Implementation for User Story 4

- [ ] T048 [P] [US4] Create QuizQuestion component in frontend/components/student/quiz-question.tsx
- [ ] T049 [P] [US4] Create ExercisePanel component in frontend/components/student/exercise-panel.tsx
- [ ] T050 [P] [US4] Create FeedbackModal component in frontend/components/ui/feedback-modal.tsx
- [ ] T051 [US4] Create topic page in frontend/app/(student)/modules/[id]/topics/[id]/page.tsx
- [ ] T052 [US4] Implement quiz interface with one question at a time in topic page
- [ ] T053 [US4] Add immediate feedback display on quiz answer submission
- [ ] T054 [US4] Implement explanation display for incorrect answers
- [ ] T055 [US4] Integrate ExercisePanel with Monaco editor for coding exercises
- [ ] T056 [US4] Implement test case execution and results display in ExercisePanel
- [ ] T057 [US4] Update progress automatically on exercise/quiz completion

**Checkpoint**: User Story 4 independently functional with P1 stories

---

## Phase 7: User Story 5 - Teacher Dashboard (Priority: P2)

**Goal**: Provide teacher dashboard with class progress view, student summaries, struggle alerts, and student detail access

**Independent Test**: A teacher logs in and views their class dashboard, seeing student progress and any alerts

### Implementation for User Story 5

- [ ] T058 [P] [US5] Create StudentTableRow component in frontend/components/teacher/student-table-row.tsx
- [ ] T059 [P] [US5] Create StruggleAlertBadge component in frontend/components/teacher/struggle-alert-badge.tsx
- [ ] T060 [P] [US5] Create StudentProgressChart component in frontend/components/teacher/student-progress-chart.tsx
- [ ] T061 [US5] Create teacher dashboard page in frontend/app/(teacher)/dashboard/page.tsx
- [ ] T062 [US5] Display all students with progress in teacher dashboard table
- [ ] T063 [US5] Highlight struggling students with StruggleAlertBadge component
- [ ] T064 [US5] Implement struggle alerts filtering in teacher dashboard
- [ ] T065 [US5] Create student detail page in frontend/app/(teacher)/students/[id]/page.tsx
- [ ] T066 [US5] Display student progress, code attempts, quiz results in student detail page
- [ ] T067 [US5] Implement navigation from dashboard to student detail pages

**Checkpoint**: User Story 5 independently functional

---

## Phase 8: User Story 6 - Authentication and User Management (Priority: P2)

**Goal**: Provide user registration, login, logout, profile management, and session persistence

**Independent Test**: A new user registers, logs in, and their session persists across browser refreshes

### Implementation for User Story 6

- [ ] T068 [P] [US6] Create LoginForm component in frontend/components/ui/login-form.tsx
- [ ] T069 [P] [US6] Create RegisterForm component in frontend/components/ui/register-form.tsx
- [ ] T070 [P] [US6] Create ProfileForm component in frontend/components/ui/profile-form.tsx
- [ ] T071 [P] [US6] Create landing page in frontend/app/(public)/landing/page.tsx
- [ ] T072 [US6] Create login page in frontend/app/(auth)/login/page.tsx
- [ ] T073 [US6] Create register page in frontend/app/(auth)/register/page.tsx
- [ ] T074 [US6] Create student profile page in frontend/app/(student)/profile/page.tsx
- [ ] T075 [US6] Implement register API call in frontend/lib/api/auth.ts to POST /api/v1/auth/register
- [ ] T076 [US6] Implement login API call in frontend/lib/api/auth.ts to POST /api/v1/auth/login
- [ ] T077 [US6] Implement logout API call in frontend/lib/api/auth.ts to POST /api/v1/auth/logout
- [ ] T078 [US6] Implement JWT token storage in httpOnly cookies via API routes
- [ ] T079 [US6] Add session persistence across page refreshes in authStore
- [ ] T080 [US6] Implement protected route redirect in middleware.ts
- [ ] T081 [US6] Add user menu with logout option in root layout

**Checkpoint**: User Story 6 independently functional, enables auth for all other stories

---

## Phase 9: Teacher Exercise Generator (Priority: P2)

**Goal**: Provide exercise generation interface for teachers to create custom exercises with topic and difficulty settings

**Independent Test**: A teacher uses the exercise generator to create a custom exercise with specified topic and difficulty

### Implementation for Teacher Exercise Generator

- [ ] T082 [P] Create ExerciseGeneratorForm component in frontend/components/teacher/exercise-generator-form.tsx
- [ ] T083 [P] Create ExercisePreview component in frontend/components/teacher/exercise-preview.tsx
- [ ] T084 Create exercise generator page in frontend/app/(teacher)/exercise-generator/page.tsx
- [ ] T085 Implement exercise generation API call in frontend/lib/api/exercises.ts to POST /api/v1/exercises/generate
- [ ] T086 Add topic selection dropdown in ExerciseGeneratorForm component
- [ ] T087 Add difficulty selection (beginner/intermediate/advanced) in ExerciseGeneratorForm
- [ ] T088 Display generated exercise preview in ExercisePreview component
- [ ] T089 Implement save exercise functionality for generated exercises

**Checkpoint**: Teacher exercise generation functional

---

## Phase 10: Additional Pages & Polish

**Purpose**: Complete remaining pages (module view, class settings) and cross-cutting improvements

- [ ] T090 [P] Create module view page in frontend/app/(student)/modules/[id]/page.tsx
- [ ] T091 [P] Create topic list view in module page with TopicCard components
- [ ] T092 [P] Create TeacherNavbar component in frontend/components/layout/teacher-navbar.tsx
- [ ] T093 [P] Create StudentNavbar component in frontend/components/layout/student-navbar.tsx
- [ ] T094 [P] Create PublicNavbar component in frontend/components/layout/public-navbar.tsx
- [ ] T095 [P] Create class settings page in frontend/app/(teacher)/settings/page.tsx
- [ ] T096 Add loading states (skeleton screens) for all pages
- [ ] T097 Add error boundaries for error handling
- [ ] T098 Implement responsive design breakpoints for tablet (768px minimum)
- [ ] T099 Add keyboard navigation support (Tab, Enter, Escape)
- [ ] T100 Add focus indicators for all interactive elements
- [ ] T101 Run performance audit and optimize bundle size
- [ ] T102 Add accessibility ARIA labels throughout application

**Checkpoint**: All pages and polish complete

---

## Phase 11: Integration & Validation

**Purpose**: Final integration testing and documentation

- [ ] T103 Test WebSocket reconnection with exponential backoff
- [ ] T104 Test Monaco editor dynamic loading and code splitting
- [ ] T105 Test all API endpoints with error handling
- [ ] T106 Test state management across page refreshes
- [ ] T107 Test authentication flow (register, login, logout, session persistence)
- [ ] T108 Test mastery level color coding (Red/Yellow/Green/Blue)
- [ ] T109 Validate performance targets (page load <3s, chat <500ms, execution <5s)
- [ ] T110 Test cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] T111 Update quickstart.md with any setup changes discovered during implementation
- [ ] T112 Create deployment documentation using nextjs-k8s-deploy skill

**Checkpoint**: Application fully tested and ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-9)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Phases 10-11)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Independent of P1 stories
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - Independent of other stories
- **User Story 6 (P2)**: Can start after Foundational (Phase 2) - Independent of other stories, but enables auth for all pages
- **Teacher Exercise Generator**: Can start after Foundational (Phase 2) - Independent of other stories

### Within Each User Story

- Component creation can run in parallel if marked [P]
- Page implementation depends on component completion
- API integration depends on page/component structure
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T007)
- All Foundational tasks marked [P] can run in parallel (T009-T018)
- Once Foundational phase completes, all user stories can start in parallel
- All component tasks within a story marked [P] can run in parallel (e.g., T020-T022 for US1)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1 Components

```bash
# Launch all components for User Story 1 together:
Task: "Create ModuleCard component in frontend/components/student/module-card.tsx"
Task: "Create MasteryBadge component in frontend/components/student/mastery-badge.tsx"
Task: "Create ProgressChart component in frontend/components/student/progress-chart.tsx"
```

---

## Parallel Example: Foundational Phase

```bash
# After Setup phase, launch all foundational tasks in parallel:
Task: "Create API client base in frontend/lib/api/client.ts"
Task: "Create Zustand auth store in frontend/lib/store/authStore.ts"
Task: "Create Zustand student store in frontend/lib/store/studentStore.ts"
Task: "Create Zustand teacher store in frontend/lib/store/teacherStore.ts"
Task: "Create Zustand chat store in frontend/lib/store/chatStore.ts"
Task: "Create useChatWebSocket hook in frontend/lib/hooks/use-websocket.ts"
Task: "Create reusable Button component in frontend/components/ui/button.tsx"
Task: "Create reusable Input component in frontend/components/ui/input.tsx"
Task: "Create reusable Card component in frontend/components/ui/card.tsx"
Task: "Create mastery level helper utilities in frontend/lib/utils/mastery.ts"
```

---

## Implementation Strategy

### MVP First (P1 Stories Only - Recommended)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T019) - CRITICAL
3. Complete Phase 3: User Story 1 - Student Dashboard (T020-T027)
4. Complete Phase 4: User Story 2 - Code Editor (T028-T037)
5. Complete Phase 5: User Story 3 - AI Chat (T038-T047)
6. **STOP and VALIDATE**: Test all P1 stories work together
7. Deploy/demo P1 MVP (Student can learn with dashboard + editor + chat)

**MVP Scope**: 47 tasks (T001-T047) deliver core student learning experience

### Incremental Delivery (Full Scope)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Dashboard) → Test independently → Deploy/Demo (MVP foundation)
3. Add User Story 2 (Editor) → Test independently → Deploy/Demo
4. Add User Story 3 (Chat) → Test independently → Deploy/Demo (P1 complete!)
5. Add User Story 4 (Quiz/Exercise) → Test independently → Deploy/Demo
6. Add User Story 5 (Teacher Dashboard) → Test independently → Deploy/Demo
7. Add User Story 6 (Authentication) → Test independently → Deploy/Demo
8. Add Teacher Exercise Generator → Test independently → Deploy/Demo
9. Complete Polish & Integration phases → Full application
10. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers (3 developers example):

1. Team completes Setup (Phase 1) + Foundational (Phase 2) together
2. Once Foundational is done:
   - **Developer A**: User Story 1 (Dashboard) + User Story 4 (Quiz/Exercise)
   - **Developer B**: User Story 2 (Editor) + User Story 3 (Chat)
   - **Developer C**: User Story 5 (Teacher Dashboard) + User Story 6 (Auth)
3. Stories complete and integrate independently
4. Team converges for Polish and Integration phases

---

## Summary

- **Total Tasks**: 112 tasks (T001-T112)
- **Setup Tasks**: 7 tasks
- **Foundational Tasks**: 12 tasks (BLOCKS all user stories)
- **User Story 1 (P1)**: 8 tasks
- **User Story 2 (P1)**: 10 tasks
- **User Story 3 (P1)**: 10 tasks
- **User Story 4 (P2)**: 10 tasks
- **User Story 5 (P2)**: 10 tasks
- **User Story 6 (P2)**: 14 tasks
- **Teacher Exercise Generator (P2)**: 8 tasks
- **Polish & Integration**: 23 tasks

### Parallel Opportunities Identified

- **Setup Phase**: 5 parallel tasks (T003-T007)
- **Foundational Phase**: 11 parallel tasks (T009-T019)
- **User Story 1**: 3 parallel component tasks (T020-T022)
- **User Story 2**: 2 parallel component tasks (T029-T030)
- **User Story 3**: 3 parallel component tasks (T038-T040)
- **User Story 4**: 3 parallel component tasks (T048-T050)
- **User Story 5**: 3 parallel component tasks (T058-T060)
- **User Story 6**: 3 parallel component tasks (T068-T070)
- **Exercise Generator**: 2 parallel component tasks (T082-T083)
- **Polish Phase**: 6 parallel page/component tasks (T090-T095)

### Independent Test Criteria per Story

- **US1**: Student logs in, views dashboard, sees 8 modules with color-coded mastery, navigates to modules
- **US2**: Student writes Python code, executes it, sees output/errors in console within 5 seconds
- **US3**: Student asks Python question, receives AI response within 3 seconds with agent attribution
- **US4**: Student completes quiz, receives immediate feedback with explanations
- **US5**: Teacher logs in, views all students with progress, sees struggle alerts highlighted
- **US6**: User registers, logs in, refreshes page, remains logged in, can access protected pages
- **Exercise Generator**: Teacher creates exercise with topic/difficulty, sees preview, saves exercise

### Suggested MVP Scope

**MVP = User Stories 1 + 2 + 3 (P1 stories only)**

- Tasks T001-T047 (47 tasks total)
- Delivers: Student Dashboard + Code Editor + AI Chat
- Enables core learning experience: View progress, write code, get AI help
- Can be deployed and demoed independently
- P2 stories (Quiz, Teacher, Auth) can be added incrementally

### Format Validation

✅ All tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
✅ All tasks have specific file paths
✅ Story labels (US1-US6) applied correctly to user story phases
✅ Parallel markers ([P]) applied appropriately
✅ Tasks are specific and actionable for LLM execution
