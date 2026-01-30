-- LearnFlow Platform Database Schema
-- PostgreSQL 15+ compatible
-- Schema version: 1.0.0

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Users and Authentication
-- ============================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('student', 'teacher', 'admin')),
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ============================================
-- Learning Content
-- ============================================

CREATE TABLE modules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    module_id UUID NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    difficulty VARCHAR(20) CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_topics_module ON topics(module_id);
CREATE INDEX idx_topics_difficulty ON topics(difficulty);

-- ============================================
-- Exercises and Quizzes
-- ============================================

CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    starter_code TEXT,
    test_cases JSONB NOT NULL,
    hints JSONB,
    solution TEXT,
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_exercises_topic ON exercises(topic_id);
CREATE INDEX idx_exercises_difficulty ON exercises(difficulty);

CREATE TABLE quizzes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    options JSONB NOT NULL,
    correct_answer INTEGER NOT NULL,
    explanation TEXT,
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quizzes_topic ON quizzes(topic_id);

-- ============================================
-- Submissions and Progress
-- ============================================

CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exercise_id UUID NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    output TEXT,
    score INTEGER CHECK (score >= 0 AND score <= 100),
    feedback JSONB,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submissions_user ON submissions(user_id);
CREATE INDEX idx_submissions_exercise ON submissions(exercise_id);
CREATE INDEX idx_submissions_score ON submissions(score);

CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quiz_id UUID NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    selected_answer INTEGER NOT NULL,
    is_correct BOOLEAN NOT NULL,
    attempted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quiz_attempts_user ON quiz_attempts(user_id);
CREATE INDEX idx_quiz_attempts_quiz ON quiz_attempts(quiz_id);

-- ============================================
-- Progress Tracking
-- ============================================

CREATE TABLE progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    mastery_score INTEGER CHECK (mastery_score >= 0 AND mastery_score <= 100),
    color_level VARCHAR(20) CHECK (color_level IN ('red', 'yellow', 'green', 'blue')),
    exercises_completed INTEGER DEFAULT 0,
    quizzes_completed INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0,
    last_activity_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, topic_id)
);

CREATE INDEX idx_progress_user ON progress(user_id);
CREATE INDEX idx_progress_mastery ON progress(mastery_score);
CREATE INDEX idx_progress_level ON progress(color_level);

-- ============================================
-- Code Execution
-- ============================================

CREATE TABLE code_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    stdout TEXT,
    stderr TEXT,
    exit_code INTEGER,
    execution_time_ms INTEGER,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_code_executions_user ON code_executions(user_id);
CREATE INDEX idx_code_executions_time ON code_executions(executed_at);

-- ============================================
-- Chat History
-- ============================================

CREATE TABLE chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    agent_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chat_history_user ON chat_history(user_id);
CREATE INDEX idx_chat_history_created ON chat_history(created_at DESC);

-- ============================================
-- Struggle Detection
-- ============================================

CREATE TABLE struggle_patterns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    error_type VARCHAR(255),
    exercise_id UUID REFERENCES exercises(id) ON DELETE SET NULL,
    occurrence_count INTEGER DEFAULT 1,
    first_seen_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, error_type, exercise_id)
);

CREATE INDEX idx_struggle_patterns_user ON struggle_patterns(user_id);
CREATE INDEX idx_struggle_patterns_resolved ON struggle_patterns(resolved_at);

-- ============================================
-- Alerts and Notifications
-- ============================================

CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN ('struggle', 'streak', 'achievement', 'info')),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    metadata JSONB,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alerts_user ON alerts(user_id);
CREATE INDEX idx_alerts_read ON alerts(is_read);
CREATE INDEX idx_alerts_created ON alerts(created_at DESC);

-- ============================================
-- Event Log (for audit trail)
-- ============================================

CREATE TABLE event_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    source_service VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_event_log_type ON event_log(event_type);
CREATE INDEX idx_event_log_source ON event_log(source_service);
CREATE INDEX idx_event_log_created ON event_log(created_at DESC);

-- ============================================
-- Functions and Triggers
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_modules_updated_at BEFORE UPDATE ON modules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_topics_updated_at BEFORE UPDATE ON topics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_exercises_updated_at BEFORE UPDATE ON exercises
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quizzes_updated_at BEFORE UPDATE ON quizzes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_progress_updated_at BEFORE UPDATE ON progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Sample Data (for development)
-- ============================================

-- Insert admin user (password: admin123)
INSERT INTO users (email, password_hash, role, full_name) VALUES
('admin@learnflow.dev', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEmc0i', 'Admin User', 'admin');

-- Insert sample modules
INSERT INTO modules (title, description, order_index) VALUES
('Python Basics', 'Learn the fundamentals of Python programming', 1),
('Control Flow', 'Master if statements, loops, and logical operators', 2),
('Functions', 'Write reusable code with functions', 3),
('Data Structures', 'Work with lists, dictionaries, sets, and tuples', 4),
('Object-Oriented Programming', 'Understand classes and objects', 5),
('File Handling', 'Read and write files', 6),
('Error Handling', 'Manage exceptions gracefully', 7),
('Advanced Topics', 'Decorators, generators, and context managers', 8);

-- ============================================
-- Views for Common Queries
-- ============================================

-- View for user progress summary
CREATE VIEW user_progress_summary AS
SELECT
    u.id AS user_id,
    u.email,
    u.full_name,
    COUNT(DISTINCT p.topic_id) AS topics_started,
    AVG(p.mastery_score) AS avg_mastery,
    SUM(p.streak_days) AS total_streak_days
FROM users u
LEFT JOIN progress p ON u.id = p.user_id
WHERE u.role = 'student'
GROUP BY u.id, u.email, u.full_name;

-- View for struggling students
CREATE VIEW struggling_students AS
SELECT
    sp.user_id,
    u.email,
    u.full_name,
    sp.error_type,
    sp.occurrence_count,
    sp.last_seen_at
FROM struggle_patterns sp
JOIN users u ON sp.user_id = u.id
WHERE sp.resolved_at IS NULL
AND sp.occurrence_count >= 3
ORDER BY sp.occurrence_count DESC, sp.last_seen_at DESC;
