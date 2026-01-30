'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Alert } from '@/components/ui/alert'
import { Progress } from '@/components/ui/progress'
import { cn, getDifficultyColor } from '@/lib/utils'
import { CheckCircle2, XCircle, ArrowRight, ArrowLeft } from 'lucide-react'
import type { Quiz, QuizQuestion } from '@/lib/types'

export interface QuizInterfaceProps {
  quiz: Quiz
  onComplete: (score: number, answers: Record<string, string | number>) => void
  onRetry?: () => void
  className?: string
}

const QuizInterface: React.FC<QuizInterfaceProps> = ({
  quiz,
  onComplete,
  onRetry,
  className,
}) => {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string | number>>({})
  const [showResults, setShowResults] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  const question = quiz.questions[currentQuestion]
  const isLastQuestion = currentQuestion === quiz.questions.length - 1
  const progress = ((currentQuestion + 1) / quiz.questions.length) * 100

  const handleSelect = (value: string | number) => {
    if (submitted) return
    setAnswers((prev) => ({ ...prev, [question.id]: value }))
  }

  const handleNext = () => {
    if (!answers[question.id]) return
    if (isLastQuestion) {
      handleSubmit()
    } else {
      setCurrentQuestion((prev) => prev + 1)
    }
  }

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion((prev) => prev - 1)
    }
  }

  const handleSubmit = () => {
    setSubmitted(true)
    // Calculate score
    let correct = 0
    quiz.questions.forEach((q) => {
      if (answers[q.id] === q.correctAnswer) correct++
    })
    const score = Math.round((correct / quiz.questions.length) * 100)
    setTimeout(() => {
      setShowResults(true)
      onComplete(score, answers)
    }, 1000)
  }

  const handleRetry = () => {
    setCurrentQuestion(0)
    setAnswers({})
    setShowResults(false)
    setSubmitted(false)
    onRetry?.()
  }

  if (showResults) {
    const correctCount = Object.entries(answers).filter(
      ([id, answer]) => {
        const q = quiz.questions.find((q) => q.id === id)
        return q && answer === q.correctAnswer
      }
    ).length
    const score = Math.round((correctCount / quiz.questions.length) * 100)
    const passed = score >= 70

    return (
      <Card className={cn('', className)}>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Quiz Results</span>
            <Badge
              variant={passed ? 'success' : 'warning'}
              size="md"
            >
              {passed ? 'Passed' : 'Needs Practice'}
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Score Circle */}
          <div className="flex justify-center">
            <div className="relative h-40 w-40">
              <svg className="h-full w-full -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="8"
                  className="text-slate-800"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke={passed ? '#22c55e' : '#f59e0b'}
                  strokeWidth="8"
                  strokeDasharray={`${2 * Math.PI * 45}`}
                  strokeDashoffset={`${2 * Math.PI * 45 * (1 - score / 100)}`}
                  strokeLinecap="round"
                  className="transition-all duration-1000"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-4xl font-bold text-white">{score}%</div>
                  <div className="text-sm text-slate-400">{correctCount}/{quiz.questions.length} correct</div>
                </div>
              </div>
            </div>
          </div>

          {/* Question Review */}
          <div className="space-y-3">
            <h3 className="font-semibold text-white">Question Review</h3>
            {quiz.questions.map((q, index) => {
              const userAnswer = answers[q.id]
              const isCorrect = userAnswer === q.correctAnswer

              return (
                <div
                  key={q.id}
                  className={cn(
                    'flex items-start gap-3 rounded-lg border p-3',
                    isCorrect
                      ? 'border-success-500/30 bg-success-500/5'
                      : 'border-error-500/30 bg-error-500/5'
                  )}
                >
                  <div className="mt-0.5">
                    {isCorrect ? (
                      <CheckCircle2 className="h-5 w-5 text-success-500" />
                    ) : (
                      <XCircle className="h-5 w-5 text-error-500" />
                    )}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-white">
                      {index + 1}. {q.question}
                    </p>
                    <div className="mt-2 flex flex-wrap gap-2 text-xs">
                      <span className="text-slate-400">Your answer: </span>
                      <span
                        className={cn(
                          'font-medium',
                          isCorrect ? 'text-success-400' : 'text-error-400'
                        )}
                      >
                        {q.options?.[userAnswer as number] || userAnswer}
                      </span>
                      {!isCorrect && (
                        <>
                          <span className="text-slate-400">• Correct: </span>
                          <span className="font-medium text-success-400">
                            {q.options?.[q.correctAnswer as number] || q.correctAnswer}
                          </span>
                        </>
                      )}
                    </div>
                    {q.explanation && (
                      <p className="mt-2 text-xs text-slate-400">{q.explanation}</p>
                    )}
                  </div>
                </div>
              )
            })}
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <Button onClick={handleRetry} className="flex-1">
              Retry Quiz
            </Button>
            <Button variant="ghost" onClick={() => window.history.back()}>
              Continue Learning
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  const selectedAnswer = answers[question.id]
  const isAnswered = !!selectedAnswer

  return (
    <Card className={cn('', className)}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Quiz: {quiz.title}</CardTitle>
          <Badge variant="primary" size="sm">
            Question {currentQuestion + 1} of {quiz.questions.length}
          </Badge>
        </div>
        <Progress value={progress} showLabel={false} />
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Question */}
        <div>
          <p className="text-lg font-medium text-white">{question.question}</p>
          {question.codeSnippet && (
            <pre className="mt-3 overflow-x-auto rounded-lg bg-slate-900 p-4 text-sm text-slate-300">
              {question.codeSnippet}
            </pre>
          )}
        </div>

        {/* Options */}
        <div className="space-y-3">
          {question.options?.map((option, index) => {
            const isSelected = selectedAnswer === index
            const showCorrect = submitted && index === question.correctAnswer
            const showIncorrect = submitted && isSelected && index !== question.correctAnswer

            return (
              <button
                key={index}
                onClick={() => handleSelect(index)}
                disabled={submitted}
                className={cn(
                  'w-full rounded-lg border-2 p-4 text-left transition-all',
                  'hover:border-slate-600 disabled:hover:border-current',
                  isSelected && !submitted && 'border-primary-500 bg-primary-500/10',
                  showCorrect && 'border-success-500 bg-success-500/10',
                  showIncorrect && 'border-error-500 bg-error-500/10',
                  !isSelected && !showCorrect && !showIncorrect && 'border-slate-800 bg-slate-900/50'
                )}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={cn(
                      'flex h-6 w-6 items-center justify-center rounded-full border-2 text-xs font-semibold',
                      isSelected && !submitted && 'border-primary-500 bg-primary-500 text-white',
                      showCorrect && 'border-success-500 bg-success-500 text-white',
                      showIncorrect && 'border-error-500 bg-error-500 text-white',
                      !isSelected && !showCorrect && !showIncorrect && 'border-slate-700 text-slate-500'
                    )}
                  >
                    {String.fromCharCode(65 + index)}
                  </div>
                  <span className="flex-1 text-white">{option}</span>
                  {showCorrect && (
                    <CheckCircle2 className="h-5 w-5 text-success-500" />
                  )}
                  {showIncorrect && (
                    <XCircle className="h-5 w-5 text-error-500" />
                  )}
                </div>
              </button>
            )
          })}
        </div>

        {/* Explanation */}
        {submitted && question.explanation && (
          <Alert variant="info" title="Explanation">
            {question.explanation}
          </Alert>
        )}

        {/* Navigation */}
        <div className="flex items-center justify-between">
          <Button
            variant="ghost"
            onClick={handlePrevious}
            disabled={currentQuestion === 0 || submitted}
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Previous
          </Button>

          {submitted ? (
            <Button onClick={handleSubmit} disabled>
              Submitted
            </Button>
          ) : isLastQuestion ? (
            <Button onClick={handleSubmit} disabled={!isAnswered}>
              Submit Quiz
            </Button>
          ) : (
            <Button onClick={handleNext} disabled={!isAnswered}>
              Next
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          )}
        </div>

        {/* Question Dots */}
        <div className="flex justify-center gap-2">
          {quiz.questions.map((_, index) => (
            <button
              key={index}
              onClick={() => !submitted && setCurrentQuestion(index)}
              disabled={submitted}
              className={cn(
                'h-2 w-2 rounded-full transition-all',
                index === currentQuestion && 'bg-primary-500 w-6',
                index !== currentQuestion && 'bg-slate-700',
                answers[quiz.questions[index].id] && !submitted && 'bg-primary-500/50'
              )}
            />
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

export default QuizInterface
