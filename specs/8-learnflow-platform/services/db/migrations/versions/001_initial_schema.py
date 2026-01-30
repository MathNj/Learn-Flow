"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2026-01-31

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("role IN ('student', 'teacher', 'admin')", name='users_role_check'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_role', 'users', ['role'], unique=False)

    # Create modules table
    op.create_table(
        'modules',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create topics table
    op.create_table(
        'topics',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('module_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('difficulty', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("difficulty IN ('beginner', 'intermediate', 'advanced')", name='topics_difficulty_check'),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_topics_module', 'topics', ['module_id'], unique=False)
    op.create_index('idx_topics_difficulty', 'topics', ['difficulty'], unique=False)

    # Create exercises table
    op.create_table(
        'exercises',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('topic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('starter_code', sa.Text(), nullable=True),
        sa.Column('test_cases', postgresql.JSONB(), nullable=False),
        sa.Column('hints', postgresql.JSONB(), nullable=True),
        sa.Column('solution', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("difficulty IN ('easy', 'medium', 'hard')", name='exercises_difficulty_check'),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_exercises_topic', 'exercises', ['topic_id'], unique=False)
    op.create_index('idx_exercises_difficulty', 'exercises', ['difficulty'], unique=False)

    # Create quizzes table
    op.create_table(
        'quizzes',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('topic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('options', postgresql.JSONB(), nullable=False),
        sa.Column('correct_answer', sa.Integer(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("difficulty IN ('easy', 'medium', 'hard')", name='quizzes_difficulty_check'),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_quizzes_topic', 'quizzes', ['topic_id'], unique=False)

    # Create submissions table
    op.create_table(
        'submissions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('exercise_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('output', sa.Text(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('feedback', postgresql.JSONB(), nullable=True),
        sa.Column('submitted_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint('score >= 0 AND score <= 100', name='submissions_score_check'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_submissions_user', 'submissions', ['user_id'], unique=False)
    op.create_index('idx_submissions_exercise', 'submissions', ['exercise_id'], unique=False)
    op.create_index('idx_submissions_score', 'submissions', ['score'], unique=False)

    # Create quiz_attempts table
    op.create_table(
        'quiz_attempts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quiz_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('selected_answer', sa.Integer(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('attempted_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_quiz_attempts_user', 'quiz_attempts', ['user_id'], unique=False)
    op.create_index('idx_quiz_attempts_quiz', 'quiz_attempts', ['quiz_id'], unique=False)

    # Create progress table
    op.create_table(
        'progress',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('topic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('mastery_score', sa.Integer(), nullable=True),
        sa.Column('color_level', sa.String(length=20), nullable=True),
        sa.Column('exercises_completed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('quizzes_completed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('streak_days', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('last_activity_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint('mastery_score >= 0 AND mastery_score <= 100', name='progress_mastery_score_check'),
        sa.CheckConstraint("color_level IN ('red', 'yellow', 'green', 'blue')", name='progress_color_level_check'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'topic_id')
    )
    op.create_index('idx_progress_user', 'progress', ['user_id'], unique=False)
    op.create_index('idx_progress_mastery', 'progress', ['mastery_score'], unique=False)
    op.create_index('idx_progress_level', 'progress', ['color_level'], unique=False)

    # Create code_executions table
    op.create_table(
        'code_executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('stdout', sa.Text(), nullable=True),
        sa.Column('stderr', sa.Text(), nullable=True),
        sa.Column('exit_code', sa.Integer(), nullable=True),
        sa.Column('execution_time_ms', sa.Integer(), nullable=True),
        sa.Column('executed_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_code_executions_user', 'code_executions', ['user_id'], unique=False)
    op.create_index('idx_code_executions_time', 'code_executions', ['executed_at'], unique=False)

    # Create chat_history table
    op.create_table(
        'chat_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('agent_type', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("role IN ('user', 'assistant', 'system')", name='chat_history_role_check'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_chat_history_user', 'chat_history', ['user_id'], unique=False)
    op.create_index('idx_chat_history_created', 'chat_history', ['created_at'], unique=False)

    # Create struggle_patterns table
    op.create_table(
        'struggle_patterns',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('error_type', sa.String(length=255), nullable=True),
        sa.Column('exercise_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('occurrence_count', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('first_seen_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('last_seen_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('resolved_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ondelete='set null'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'error_type', 'exercise_id')
    )
    op.create_index('idx_struggle_patterns_user', 'struggle_patterns', ['user_id'], unique=False)
    op.create_index('idx_struggle_patterns_resolved', 'struggle_patterns', ['resolved_at'], unique=False)

    # Create alerts table
    op.create_table(
        'alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('alert_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("alert_type IN ('struggle', 'streak', 'achievement', 'info')", name='alerts_alert_type_check'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_alerts_user', 'alerts', ['user_id'], unique=False)
    op.create_index('idx_alerts_read', 'alerts', ['is_read'], unique=False)
    op.create_index('idx_alerts_created', 'alerts', ['created_at'], unique=False)

    # Create event_log table
    op.create_table(
        'event_log',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('source_service', sa.String(length=100), nullable=False),
        sa.Column('event_data', postgresql.JSONB(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='set null'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_event_log_type', 'event_log', ['event_type'], unique=False)
    op.create_index('idx_event_log_source', 'event_log', ['source_service'], unique=False)
    op.create_index('idx_event_log_created', 'event_log', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order of creation
    op.drop_index('idx_event_log_created', table_name='event_log')
    op.drop_index('idx_event_log_source', table_name='event_log')
    op.drop_index('idx_event_log_type', table_name='event_log')
    op.drop_table('event_log')

    op.drop_index('idx_alerts_created', table_name='alerts')
    op.drop_index('idx_alerts_read', table_name='alerts')
    op.drop_index('idx_alerts_user', table_name='alerts')
    op.drop_table('alerts')

    op.drop_index('idx_struggle_patterns_resolved', table_name='struggle_patterns')
    op.drop_index('idx_struggle_patterns_user', table_name='struggle_patterns')
    op.drop_table('struggle_patterns')

    op.drop_index('idx_chat_history_created', table_name='chat_history')
    op.drop_index('idx_chat_history_user', table_name='chat_history')
    op.drop_table('chat_history')

    op.drop_index('idx_code_executions_time', table_name='code_executions')
    op.drop_index('idx_code_executions_user', table_name='code_executions')
    op.drop_table('code_executions')

    op.drop_index('idx_progress_level', table_name='progress')
    op.drop_index('idx_progress_mastery', table_name='progress')
    op.drop_index('idx_progress_user', table_name='progress')
    op.drop_table('progress')

    op.drop_index('idx_quiz_attempts_quiz', table_name='quiz_attempts')
    op.drop_index('idx_quiz_attempts_user', table_name='quiz_attempts')
    op.drop_table('quiz_attempts')

    op.drop_index('idx_submissions_score', table_name='submissions')
    op.drop_index('idx_submissions_exercise', table_name='submissions')
    op.drop_index('idx_submissions_user', table_name='submissions')
    op.drop_table('submissions')

    op.drop_index('idx_quizzes_topic', table_name='quizzes')
    op.drop_table('quizzes')

    op.drop_index('idx_exercises_difficulty', table_name='exercises')
    op.drop_index('idx_exercises_topic', table_name='exercises')
    op.drop_table('exercises')

    op.drop_index('idx_topics_difficulty', table_name='topics')
    op.drop_index('idx_topics_module', table_name='topics')
    op.drop_table('topics')

    op.drop_table('modules')

    op.drop_index('idx_users_role', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')

    # Drop UUID extension
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
