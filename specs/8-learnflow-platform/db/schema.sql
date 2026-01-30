-- LearnFlow Platform Database Schema
-- PostgreSQL schema for the LearnFlow AI-powered Python tutoring platform
--
-- This schema defines all tables required for:
-- - User management (students and teachers)
-- - Curriculum structure (8 Python modules)
-- - Exercises and submissions
-- - Progress tracking and mastery calculation
-- - Struggle detection and alerts
-- - Chat history

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- USERS
-- ============================================================================
-- Students and teachers who use the platform

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher')),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Index for email lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ============================================================================
-- MODULES
-- ============================================================================
-- 8 Python curriculum modules as specified in the requirements

CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert the 8 curriculum modules
INSERT INTO modules (name, title, description, order_index) VALUES
('basics', 'Module 1: Basics', 'Variables, Data Types, Input/Output, Operators, Type Conversion', 1),
('control-flow', 'Module 2: Control Flow', 'Conditionals (if/elif/else), For Loops, While Loops, Break/Continue', 2),
('data-structures', 'Module 3: Data Structures', 'Lists, Tuples, Dictionaries, Sets', 3),
('functions', 'Module 4: Functions', 'Defining Functions, Parameters, Return Values, Scope', 4),
('oop', 'Module 5: OOP', 'Classes & Objects, Attributes & Methods, Inheritance, Encapsulation', 5),
('files', 'Module 6: Files', 'Reading/Writing Files, CSV Processing, JSON Handling', 6),
('errors', 'Module 7: Errors', 'Try/Except, Exception Types, Custom Exceptions, Debugging', 7),
('libraries', 'Module 8: Libraries', 'Installing Packages, Working with APIs, Virtual Environments', 8);

-- ============================================================================
-- TOPICS
-- ============================================================================
-- Specific learning topics within each module

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(module_id, order_index)
);

CREATE INDEX idx_topics_module ON topics(module_id);

-- ============================================================================
-- EXERCISES
-- ============================================================================
-- Coding challenges and exercises

CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id INTEGER REFERENCES topics(id) ON DELETE SET NULL,
    module_id INTEGER REFERENCES modules(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    starter_code TEXT,
    solution_code TEXT,
    test_cases JSONB NOT NULL,  -- Array of test cases with input/expected_output
    difficulty VARCHAR(20) CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,  -- Teacher who created
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_exercises_topic ON exercises(topic_id);
CREATE INDEX idx_exercises_module ON exercises(module_id);

-- ============================================================================
-- SUBMISSIONS
-- ============================================================================
-- Student code submissions with feedback

CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exercise_id UUID REFERENCES exercises(id) ON DELETE CASCADE,
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    output TEXT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'passed', 'failed', 'error')),
    feedback JSONB,  -- Structured feedback from Code Review Agent
    code_quality_score INTEGER CHECK (code_quality_score >= 0 AND code_quality_score <= 100),
    attempts INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_submissions_student ON submissions(student_id);
CREATE INDEX idx_submissions_exercise ON submissions(exercise_id);
CREATE INDEX idx_submissions_status ON submissions(status);

-- ============================================================================
-- PROGRESS
-- ============================================================================
-- Mastery tracking per topic per student

CREATE TABLE progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,

    -- Mastery components (as per formula)
    exercise_mastery INTEGER DEFAULT 0 CHECK (exercise_mastery >= 0 AND exercise_mastery <= 100),
    quiz_mastery INTEGER DEFAULT 0 CHECK (quiz_mastery >= 0 AND quiz_mastery <= 100),
    code_quality_mastery INTEGER DEFAULT 0 CHECK (code_quality_mastery >= 0 AND code_quality_mastery <= 100),
    consistency_mastery INTEGER DEFAULT 0 CHECK (consistency_mastery >= 0 AND consistency_mastery <= 100),

    -- Overall mastery (weighted average: 40/30/20/10)
    overall_mastery INTEGER GENERATED ALWAYS AS (
        (exercise_mastery * 40 + quiz_mastery * 30 + code_quality_mastery * 20 + consistency_mastery * 10) / 100
    ) STORED,

    -- Learning streak (consecutive days of activity)
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_activity_at DATE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(student_id, topic_id)
);

CREATE INDEX idx_progress_student ON progress(student_id);
CREATE INDEX idx_progress_module ON progress(module_id);
CREATE INDEX idx_progress_mastery ON progress(overall_mastery);

-- ============================================================================
-- STRUGGLE ALERTS
-- ============================================================================
-- Alerts for teachers when students need help

CREATE TABLE struggle_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    teacher_id UUID REFERENCES users(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE SET NULL,
    exercise_id UUID REFERENCES exercises(id) ON DELETE SET NULL,

    -- What triggered the alert
    trigger_type VARCHAR(50) NOT NULL CHECK (trigger_type IN (
        'repeated_error',      -- Same error 3+ times
        'time_exceeded',       -- Stuck >10 minutes
        'low_quiz_score',      -- Quiz score <50%
        'keyword_phrase',      -- "I don't understand"
        'failed_executions'    -- 5+ failed executions
    )),

    -- Context for the teacher
    context JSONB,  -- Includes error messages, code attempts, time spent, etc.

    -- Alert management
    is_acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    resolved_at TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_struggles_student ON struggle_alerts(student_id);
CREATE INDEX idx_struggles_teacher ON struggle_alerts(teacher_id);
CREATE INDEX idx_struggles_acknowledged ON struggle_alerts(is_acknowledged);
CREATE INDEX idx_struggles_created ON struggle_alerts(created_at DESC);

-- ============================================================================
-- CHAT MESSAGES
-- ============================================================================
-- Conversation history between students and AI tutors

CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE SET NULL,

    -- Message content
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,

    -- Which agent handled this
    agent_type VARCHAR(50) CHECK (agent_type IN (
        'triage', 'concepts', 'code-review', 'debug', 'exercise', 'progress'
    )),

    -- Request-response correlation
    correlation_id UUID,
    in_response_to UUID REFERENCES chat_messages(id) ON DELETE SET NULL,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_chat_student ON chat_messages(student_id);
CREATE INDEX idx_chat_correlation ON chat_messages(correlation_id);
CREATE INDEX idx_chat_created ON chat_messages(created_at DESC);

-- ============================================================================
-- QUIZ RESULTS
-- ============================================================================
-- Quiz scores for mastery calculation

CREATE TABLE quiz_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_quiz_student ON quiz_results(student_id);
CREATE INDEX idx_quiz_topic ON quiz_results(topic_id);

-- ============================================================================
-- CLASSES (for teachers)
-- ============================================================================
-- Teacher-student groupings

CREATE TABLE classes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    teacher_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE class_enrollments (
    class_id UUID REFERENCES classes(id) ON DELETE CASCADE,
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (class_id, student_id)
);

-- ============================================================================
-- FUNCTIONS AND TRIGGERS
-- ============================================================================

-- Update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply the trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_submissions_updated_at BEFORE UPDATE ON submissions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_progress_updated_at BEFORE UPDATE ON progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Student dashboard view with progress summary
CREATE VIEW student_progress_summary AS
SELECT
    u.id AS student_id,
    u.first_name,
    u.last_name,
    m.id AS module_id,
    m.title AS module_title,
    COUNT(DISTINCT t.id) AS total_topics,
    COUNT(p.id) AS topics_started,
    AVG(p.overall_mastery) FILTER (WHERE p.overall_mastery IS NOT NULL) AS avg_mastery,
    MAX(p.current_streak) AS current_streak
FROM users u
CROSS JOIN modules m
LEFT JOIN topics t ON t.module_id = m.id
LEFT JOIN progress p ON p.student_id = u.id AND p.module_id = m.id
WHERE u.role = 'student'
GROUP BY u.id, u.first_name, u.last_name, m.id, m.title;

-- Teacher alert queue view
CREATE VIEW teacher_alert_queue AS
SELECT
    sa.id AS alert_id,
    sa.created_at,
    u.first_name AS student_name,
    u.last_name,
    m.title AS module_title,
    t.title AS topic_title,
    sa.trigger_type,
    sa.context
FROM struggle_alerts sa
JOIN users u ON u.id = sa.student_id
JOIN users teacher ON teacher.id = sa.teacher_id
LEFT JOIN topics t ON t.id = sa.topic_id
LEFT JOIN modules m ON m.id = t.module_id
WHERE sa.is_acknowledged = FALSE
ORDER BY sa.created_at DESC;
