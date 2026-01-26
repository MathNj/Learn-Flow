---
name: exercise-agent
description: Generates and auto-grades Python coding challenges. Adapts difficulty to student's mastery level and recent struggles.
---

# Exercise Agent

Generates Python coding exercises and auto-grades student submissions.

## Purpose

Provide personalized coding practice that:
1. Matches student's current mastery level
2. Targets topics they're struggling with
3. Progressively increases difficulty
4. Provides immediate, constructive feedback

## Exercise Generation

```python
def generate_exercise(student: dict) -> dict:
    """
    Generate personalized exercise based on student profile
    """
    mastery = student["mastery_by_topic"]
    struggles = student["recent_struggles"]
    level = student["overall_mastery"]

    # Identify focus area
    topic = select_focus_topic(mastery, struggles)

    # Choose difficulty
    difficulty = calculate_difficulty(level, topic)

    return {
        "exercise_id": generate_id(),
        "topic": topic,
        "difficulty": difficulty,  # beginner, intermediate, advanced
        "title": "Exercise title",
        "description": "Clear problem statement",
        "requirements": [
            "Specific requirement 1",
            "Specific requirement 2"
        ],
        "starter_code": "# Optional starter template",
        "hints": ["Hint 1", "Hint 2", "Hint 3"],
        "test_cases": generate_test_cases(topic, difficulty),
        "solution": generate_solution(topic, difficulty),
        "estimated_time": estimate_time(difficulty),
        "learning_objectives": [
            "Objective 1",
            "Objective 2"
        ]
    }
```

## Exercise Templates by Topic

### Loops - For Loops

**Beginner**:
```python
# Exercise: Print Numbers
# Print all numbers from 1 to 10, each on a new line

# Your code here:
```

**Test Cases**:
- Output contains numbers 1 through 10
- Each number on its own line
- No extra output

**Intermediate**:
```python
# Exercise: Sum of Evens
# Calculate the sum of all even numbers from 1 to 100

# Your code here:
```

**Advanced**:
```python
# Exercise: Pattern Printer
# Print this pattern:
# *
# **
# ***
# ****
# *****
# The number of rows should be a variable `n`
```

### Lists

**Beginner**:
```python
# Exercise: List Operations
# Given a list of numbers, find the largest one

numbers = [23, 45, 12, 67, 34, 89, 5]
# Your code here:
```

**Intermediate**:
```python
# Exercise: List Comprehension
# Convert this loop to a list comprehension:
# squares = []
# for i in range(10):
#     squares.append(i ** 2)

# Your list comprehension here:
```

**Advanced**:
```python
# Exercise: Flatten Nested List
# Given a nested list, create a flat list with all elements

nested = [[1, 2], [3, 4], [5, [6, 7]]]
# Expected: [1, 2, 3, 4, 5, 6, 7]

# Your code here:
```

### Functions

**Beginner**:
```python
# Exercise: Simple Function
# Write a function called `greet` that takes a name
# and returns "Hello, [name]!"

def greet(name):
    # Your code here:
    pass
```

**Intermediate**:
```python
# Exercise: Function with Default Parameter
# Write a function that calculates the area of a rectangle.
# Use default values: width=10, height=5

def rectangle_area(width=10, height=5):
    # Your code here:
    pass
```

**Advanced**:
```python
# Exercise: Recursive Function
# Write a recursive function to calculate factorial

def factorial(n):
    # Your code here:
    pass

# Test: factorial(5) should return 120
```

### Dictionaries

**Beginner**:
```python
# Exercise: Dictionary Access
# Given a student's grades, print each subject and grade

grades = {
    "math": 95,
    "science": 88,
    "english": 92,
    "history": 85
}

# Your code here:
```

**Intermediate**:
```python
# Exercise: Word Counter
# Count the frequency of each word in a sentence

text = "the quick brown fox jumps over the lazy dog the"
# Expected: {'the': 3, 'quick': 1, 'brown': 1, ...}

def word_count(text):
    # Your code here:
    pass
```

**Advanced**:
```python
# Exercise: Nested Dictionary Operations
# Given student data, calculate the average grade for each student

students = {
    "Alice": {"math": 90, "science": 85, "english": 92},
    "Bob": {"math": 78, "science": 92, "english": 88},
    "Charlie": {"math": 95, "science": 89, "english": 94}
}

# Return: {'Alice': 89, 'Bob': 86, 'Charlie': 92.33}
```

## Auto-Grading

```python
def grade_submission(exercise: dict, student_code: str) -> dict:
    """
    Auto-grade student's exercise submission
    """
    results = {
        "passed": 0,
        "failed": 0,
        "test_results": [],
        "feedback": [],
        "score": 0
    }

    # Run test cases
    for test in exercise["test_cases"]:
        try:
            # Execute student code with test input
            output = execute_code(student_code, test["input"])

            # Check output
            if output == test["expected"]:
                results["passed"] += 1
                results["test_results"].append({
                    "test": test["name"],
                    "status": "PASS"
                })
            else:
                results["failed"] += 1
                results["test_results"].append({
                    "test": test["name"],
                    "status": "FAIL",
                    "expected": test["expected"],
                    "got": output
                })
        except Exception as e:
            results["failed"] += 1
            results["test_results"].append({
                "test": test["name"],
                "status": "ERROR",
                "error": str(e)
            })

    # Calculate score
    total = results["passed"] + results["failed"]
    results["score"] = (results["passed"] / total * 100) if total > 0 else 0

    # Generate feedback
    results["feedback"] = generate_feedback(results)

    return results
```

## Adaptive Difficulty

Adjust next exercise based on performance:

| Current Score | Next Exercise |
|---------------|---------------|
| 0-40% | Decrease difficulty, add more examples |
| 41-70% | Same difficulty, focus on weak areas |
| 71-90% | Increase difficulty slightly |
| 91-100% | Significantly increase difficulty |

## Struggle-Based Generation

When a student struggles with a topic:

1. **Identify the pattern** - What type of errors?
2. **Generate targeted practice** - Focus on that specific sub-topic
3. **Provide more scaffolding** - Starter code, hints, examples
4. **Reduce complexity** - Break into smaller steps

## Feedback Templates

### Success Feedback
```markdown
Excellent work! You scored {score}%.

What you did well:
- {strength1}
- {strength2}

Next steps:
- Try the next exercise on {next_topic}
- Challenge yourself with {advanced_variation}
```

### Needs Work Feedback
```markdown
Good effort! You scored {score}%. Let's improve.

Issues to address:
- {issue1}
- {issue2}

Hints:
- {hint1}
- {hint2}

Would you like to:
1. Try a similar exercise for more practice?
2. Review the concept with the Concepts Agent?
3. See the solution?
```

## Exercise Categories

### Practice Exercises
- Reinforce recently learned concepts
- Immediate feedback available
- Auto-graded

### Challenge Exercises
- Apply multiple concepts together
- Real-world scenarios
- Partial hints available

### Diagnostic Exercises
- Identify knowledge gaps
- Cover multiple topics
- Help generate personalized learning path
