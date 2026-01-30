---
title: Teacher Guide
description: LearnFlow Platform teacher guide
sidebar_position: 2
---

# LearnFlow Teacher Guide

LearnFlow provides educators with powerful tools to create, manage, and track student learning experiences.

## Dashboard Overview

The teacher dashboard shows:

### Class Overview
- Total students enrolled
- Average class mastery
- Students needing attention
- Recent submissions

### Struggle Alerts
Students are flagged when they:
- Repeat the same error 3+ times
- Spend >10 minutes on a topic
- Score below 50% on quizzes
- Request help multiple times

## Creating Exercises

### Exercise Generator

Create custom coding exercises:

1. Navigate to **Exercise Generator**
2. Fill in the exercise details:
   - **Title**: Clear, descriptive name
   - **Difficulty**: Beginner, Intermediate, Advanced
   - **Description**: What students need to do
   - **Starter Code**: Initial code template
   - **Solution**: Your reference solution
   - **Test Cases**: Automated validation

3. Preview the exercise
4. Save or Publish

### Exercise Template

```markdown title="Exercise Example"
# Title: Loop Practice

## Difficulty: Beginner

## Description
Write a loop that prints numbers from 1 to 10.

## Starter Code
for i in range(___, ___):
    print(i)

## Solution
for i in range(1, 11):
    print(i)

## Test Cases
- Output contains 10 lines
- First line is "1"
- Last line is "10"
```

## Managing Classes

### Class Setup

1. Create a new class
2. Set the learning path
3. Configure passing thresholds
4. Invite students

### Progress Tracking

Monitor individual student progress:
- Mastery level per topic
- Quiz scores over time
- Time spent on each module
- Exercises completed

### Exporting Reports

Download class performance data:
- CSV export for spreadsheet analysis
- PDF summary for administrators
- Individual student reports

## AI Tutor Settings

### Hint Levels

Configure how much help the AI provides:

| Level | Behavior |
|-------|----------|
| Minimal | Only points to relevant docs |
| Moderate | Explains concepts, not solutions |
| Generous | Provides detailed explanations |

### Intervention Rules

Auto-escalate to teacher when:
- Student struggles >15 minutes
- Error repeats 5+ times
- Quiz score <40%

## Best Practices

### Exercise Design
- Start simple, increase complexity
- Provide clear, concise instructions
- Include relevant real-world examples
- Test your solution before publishing

### Feedback Strategies
- Use struggle alerts to target help
- Celebrate student progress publicly
- Encourage peer collaboration
- Adjust exercises based on performance

### Assessment
- Mix quiz types (multiple choice, coding)
- Use projects for comprehensive assessment
- Allow multiple submission attempts
- Provide rubrics for subjective grading

## Troubleshooting

### Students Can't Run Code
- Check browser console for errors
- Verify WebSocket connection
- Try clearing browser cache

### Struggle Alerts Not Appearing
- Verify alert thresholds in settings
- Check that students are submitting attempts
- Review intervention rules

## Next Steps

- [User Guide](./user-guide.md) - Student perspective
- [Student Guide](./student-guide.md) - Detailed learning guide
