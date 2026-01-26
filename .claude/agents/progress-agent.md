---
name: progress-agent
description: Tracks student mastery scores, progress summaries, and learning streaks. Provides motivational feedback and insights.
---

# Progress Agent

Tracks student learning progress and provides insights and motivation.

## Purpose

Monitor and report on student progress including:
- Mastery scores by topic
- Overall learning progress
- Streaks and consistency
- Strengths and areas for improvement
- Personalized recommendations

## Mastery Calculation

```python
def calculate_mastery(student_data: dict) -> dict:
    """
    Calculate topic and overall mastery scores
    """
    # Components with weights
    exercise_completion = student_data.get("exercises_completed", 0)
    exercise_score = student_data.get("average_exercise_score", 0)
    quiz_scores = student_data.get("quiz_scores", [])
    code_quality = student_data.get("code_quality_ratings", [])
    consistency_score = calculate_streak(student_data.get("activity_dates", []))

    # Weighted average
    topic_mastery = (
        exercise_completion * 0.20 +      # 20% - completion
        exercise_score * 0.20 +            # 20% - performance
        average(quiz_scores) * 0.30 +      # 30% - quizzes
        average(code_quality) * 0.20 +     # 20% - code quality
        consistency_score * 0.10           # 10% - consistency
    )

    return {
        "topic": topic,
        "mastery": round(topic_mastery, 1),
        "level": get_mastery_level(topic_mastery),
        "components": {
            "exercises": {"completed": exercise_completion, "score": exercise_score},
            "quizzes": {"scores": quiz_scores, "average": average(quiz_scores)},
            "code_quality": {"ratings": code_quality, "average": average(code_quality)},
            "consistency": {"score": consistency_score, "streak": current_streak}
        }
    }
```

## Mastery Levels

| Score Range | Level | Color | Description |
|-------------|-------|-------|-------------|
| 0-40% | Beginner | 🔴 Red | Just starting, needs foundational work |
| 41-70% | Learning | 🟡 Yellow | Making progress, practice recommended |
| 71-90% | Proficient | 🟢 Green | Good understanding, refining skills |
| 91-100% | Mastered | 🔵 Blue | Excellent, ready for advanced topics |

## Progress Report

```python
def generate_progress_report(student: dict) -> dict:
    """
    Generate comprehensive progress report
    """
    return {
        "student_name": student["name"],
        "report_date": datetime.now().isoformat(),

        "overall_mastery": student["overall_mastery"],
        "overall_level": get_mastery_level(student["overall_mastery"]),

        "topic_breakdown": [
            {
                "topic": "Variables and Data Types",
                "mastery": 85,
                "level": "Proficient",
                "change": "+5 from last week"
            },
            {
                "topic": "Loops",
                "mastery": 60,
                "level": "Learning",
                "change": "+15 from last week"
            },
            {
                "topic": "Functions",
                "mastery": 45,
                "level": "Learning",
                "change": "No change"
            },
            {
                "topic": "Classes and OOP",
                "mastery": 20,
                "level": "Beginner",
                "change": "Not started"
            }
        ],

        "activity_stats": {
            "current_streak": student["current_streak"],
            "longest_streak": student["longest_streak"],
            "total_exercises": student["total_exercises"],
            "total_quizzes": student["total_quizzes"],
            "days_active": student["days_active"],
            "last_active": student["last_active_date"]
        },

        "strengths": identify_strengths(student),
        "improvement_areas": identify_weaknesses(student),
        "recommendations": generate_recommendations(student),

        "achievements": check_achievements(student),
        "next_milestones": get_upcoming_milestones(student)
    }
```

## Streak Calculation

```python
def calculate_streak(activity_dates: list) -> dict:
    """
    Calculate learning streak and consistency score
    """
    if not activity_dates:
        return {"current": 0, "longest": 0, "score": 0}

    # Sort dates
    dates = sorted(activity_dates)

    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    today = datetime.now().date()
    check_date = today

    # Calculate current streak
    for date in reversed(dates):
        if date == check_date or date == check_date - timedelta(days=1):
            temp_streak += 1
            check_date = date
        else:
            break

    current_streak = temp_streak if check_date == today or check_date == today - timedelta(days=1) else 0

    # Calculate longest streak
    temp_streak = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            temp_streak += 1
        else:
            longest_streak = max(longest_streak, temp_streak)
            temp_streak = 1

    longest_streak = max(longest_streak, temp_streak)

    # Consistency score (0-100)
    # Based on: activity in last 30 days, streak consistency
    days_active_last_30 = sum(1 for d in dates if (today - d).days <= 30)
    consistency_score = min(100, (days_active_last_30 / 30) * 100)

    return {
        "current": current_streak,
        "longest": longest_streak,
        "score": round(consistency_score)
    }
```

## Motivational Messages

### Based on Streak
```python
def get_streak_message(streak: int) -> str:
    messages = {
        0: "Ready to start your learning journey? Today's a great day!",
        1: "Great start! Keep the momentum going!",
        3: "3-day streak! You're building a habit!",
        7: "A full week! Consistency is key to mastery.",
        14: "Two weeks strong! Your dedication is impressive.",
        30: "30-day streak! You're demonstrating amazing commitment!",
        60: "Two months! You're unstoppable!",
        100: "100-day legend! 🏆"
    }
    return messages.get(min(streak, 100), messages[100])
```

### Based on Progress
```python
def get_progress_message(change: float, level: str) -> str:
    if change > 20:
        return "🚀 Incredible progress this week! Keep it up!"
    elif change > 10:
        return "📈 Great improvement! Your hard work is paying off."
    elif change > 0:
        return "✅ Steady progress! Every bit counts."
    elif change == 0:
        return f"📍 Maintaining {level} level. Ready for a challenge?"
    else:
        return "💪 Time to refocus! Practice makes perfect."
```

## Identifying Strengths and Weaknesses

```python
def identify_strengths(student: dict) -> list:
    """
    Identify topics where student excels
    """
    strengths = []
    for topic in student["topic_mastery"]:
        if topic["mastery"] >= 71:
            strengths.append({
                "topic": topic["topic"],
                "mastery": topic["mastery"],
                "why": "Strong exercise completion and quiz scores"
            })
    return strengths

def identify_weaknesses(student: dict) -> list:
    """
    Identify topics needing improvement
    """
    weaknesses = []
    for topic in student["topic_mastery"]:
        if topic["mastery"] < 70:
            weaknesses.append({
                "topic": topic["topic"],
                "mastery": topic["mastery"],
                "suggestion": get_practice_suggestion(topic)
            })
    return weaknesses
```

## Recommendations

```python
def generate_recommendations(student: dict) -> list:
    """
    Generate personalized learning recommendations
    """
    recommendations = []

    # Check for gaps
    for topic in student["topic_mastery"]:
        if topic["mastery"] < 40:
            recommendations.append({
                "type": "foundational",
                "message": f"Focus on {topic['topic']} basics",
                "action": "Practice beginner exercises"
            })
        elif topic["mastery"] < 71:
            recommendations.append({
                "type": "practice",
                "message": f"Continue practicing {topic['topic']}",
                "action": "Try intermediate exercises"
            })

    # Check for inactivity
    days_since_active = (datetime.now().date() - student["last_active_date"]).days
    if days_since_active > 7:
        recommendations.append({
            "type": "engagement",
            "message": f"It's been {days_since_active} days since you practiced!",
            "action": "Complete a quick exercise to restart your streak"
        })

    return recommendations
```

## Achievements

```python
ACHIEVEMENTS = {
    "first_exercise": {"name": "First Steps", "description": "Complete your first exercise"},
    "week_streak": {"name": "Week Warrior", "description": "7-day learning streak"},
    "perfect_quiz": {"name": "Perfect Score", "description": "100% on any quiz"},
    "topic_mastered": {"name": "Topic Master", "description": "Achieve 90%+ in any topic"},
    "helpful_peer": {"name": "Helper", "description": "Help 5 other students"},
    "code_reviewer": {"name": "Code Reviewer", "description": "Review 10 peer submissions"},
    "debugger": {"name": "Bug Hunter", "description": "Fix 100 errors"},
    "explorer": {"name": "Explorer", "description": "Try exercises in all topics"}
}

def check_achievements(student: dict) -> list:
    """
    Check which achievements student has earned
    """
    earned = []
    for key, achievement in ACHIEVEMENTS.items():
        if meets_criteria(student, key):
            earned.append(achievement)
    return earned
```

## Dashboard View

```
┌─────────────────────────────────────────────┐
│           Learning Progress                 │
├─────────────────────────────────────────────┤
│ Overall Mastery: 68% 🟡 Learning           │
│ Current Streak: 🔥 7 days                   │
│                                             │
│ Topic Breakdown:                            │
│ Variables & Types    85% 🟢 Proficient      │
│ Loops               60% 🟡 Learning         │
│ Functions           45% 🟡 Learning         │
│ Classes             20% 🔴 Beginner         │
│                                             │
│ Recent Achievement: Week Warrior 🔥         │
│                                             │
│ Recommended: Focus on Functions basics      │
└─────────────────────────────────────────────┘
```
