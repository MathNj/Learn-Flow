'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Alert } from '@/components/ui/alert'
import CodeEditor from '@/components/shared/monaco-editor'
import CodeRunner from '@/components/shared/code-runner'
import { cn, getDifficultyColor, formatRelativeTime } from '@/lib/utils'
import type { Exercise, CodeRunResult } from '@/lib/types'
import { Clock, Play, CheckCircle2, Lightbulb, ArrowLeft } from 'lucide-react'

export interface ExerciseCardProps {
  exercise: Exercise
  onComplete?: (success: boolean, code: string) => void
  onBack?: () => void
  className?: string
}

const ExerciseCard: React.FC<ExerciseCardProps> = ({
  exercise,
  onComplete,
  onBack,
  className,
}) => {
  const [code, setCode] = useState(exercise.starterCode)
  const [runResult, setRunResult] = useState<CodeRunResult | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [showHint, setShowHint] = useState(false)
  const [hintIndex, setHintIndex] = useState(0)
  const [submitted, setSubmitted] = useState(false)
  const [passed, setPassed] = useState(false)

  const handleRunCode = async () => {
    setIsRunning(true)
    setRunResult(null)

    // Simulate code execution
    setTimeout(() => {
      // Check against test cases
      const allPassed = exercise.testCases.every((testCase) => {
        // Simple check - in real app, this would run the actual code
        return code.includes('print') && code.length > exercise.starterCode.length
      })

      setRunResult({
        success: allPassed,
        output: allPassed ? 'All tests passed!' : 'Some tests failed. Try again!',
        executionTime: 0.15,
        timeoutOccurred: false,
      })
      setIsRunning(false)
    }, 1500)
  }

  const handleSubmit = () => {
    setSubmitted(true)
    const success = runResult?.success || false
    setPassed(success)
    onComplete?.(success, code)
  }

  const handleNextHint = () => {
    if (hintIndex < (exercise.hints?.length || 0) - 1) {
      setHintIndex(hintIndex + 1)
    } else {
      setShowHint(false)
      setHintIndex(0)
    }
  }

  return (
    <Card className={cn('flex flex-col', className)}>
      {/* Header */}
      <CardHeader className="border-b border-slate-800">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            {onBack && (
              <Button variant="ghost" size="sm" onClick={onBack} className="mb-2 h-7">
                <ArrowLeft className="mr-2 h-3.5 w-3.5" />
                Back
              </Button>
            )}
            <CardTitle className="text-white">{exercise.title}</CardTitle>
            <p className="mt-1 text-sm text-slate-400">{exercise.description}</p>
          </div>
          <div className="flex flex-col items-end gap-2">
            <Badge className={getDifficultyColor(exercise.difficulty)}>
              {exercise.difficulty}
            </Badge>
            <div className="flex items-center gap-1 text-xs text-slate-500">
              <Clock className="h-3.5 w-3.5" />
              <span>{exercise.estimatedMinutes} min</span>
            </div>
          </div>
        </div>

        {passed && (
          <Alert variant="success" title="Exercise Complete!" className="mt-4">
            Great job! You've successfully completed this exercise.
          </Alert>
        )}

        {submitted && !passed && (
          <Alert variant="error" title="Not quite right" className="mt-4">
            Your code doesn't pass all the test cases yet. Keep trying!
          </Alert>
        )}
      </CardHeader>

      <CardContent className="flex flex-1 flex-col p-4">
        {/* Hints */}
        {(exercise.hints?.length || 0) > 0 && (
          <div className="mb-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowHint(!showHint)}
              className="h-7 text-slate-400"
            >
              <Lightbulb className="mr-2 h-3.5 w-3.5" />
              {showHint ? 'Hide Hint' : 'Show Hint'}
            </Button>
            {showHint && (
              <Alert variant="info" className="mt-2">
                <p>{exercise.hints?.[hintIndex]}</p>
                {(exercise.hints?.length || 0) > 1 && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleNextHint}
                    className="mt-2 h-7 text-xs"
                  >
                    {hintIndex < (exercise.hints?.length || 0) - 1 ? 'Next Hint' : 'Hide'}
                  </Button>
                )}
              </Alert>
            )}
          </div>
        )}

        {/* Test Cases */}
        <div className="mb-4">
          <p className="mb-2 text-sm font-medium text-slate-300">Test Cases:</p>
          <div className="space-y-2">
            {exercise.testCases.filter((tc) => !tc.isHidden).map((testCase) => (
              <div
                key={testCase.id}
                className="flex items-center gap-2 rounded-lg border border-slate-800 bg-slate-900/50 px-3 py-2"
              >
                <div className="h-2 w-2 rounded-full bg-slate-600" />
                <span className="text-sm text-slate-400">
                  Input: {testCase.input || 'None'}
                </span>
                <span className="text-slate-600">→</span>
                <span className="text-sm text-slate-300">
                  Output: {testCase.expectedOutput}
                </span>
              </div>
            ))}
            {exercise.testCases.some((tc) => tc.isHidden) && (
              <p className="text-xs text-slate-500">
                + {exercise.testCases.filter((tc) => tc.isHidden).length} hidden test case(s)
              </p>
            )}
          </div>
        </div>

        {/* Editor */}
        <div className="flex-1">
          <CodeEditor
            code={code}
            onChange={setCode}
            onRun={handleRunCode}
            isLoading={isRunning}
            height="300px"
            readOnly={submitted && passed}
          />
        </div>

        {/* Output */}
        <div className="mt-4">
          <CodeRunner
            result={runResult}
            isRunning={isRunning}
            onClear={() => setRunResult(null)}
          />
        </div>

        {/* Submit */}
        {!passed && (
          <Button
            onClick={handleSubmit}
            disabled={!runResult || !runResult.success}
            className="mt-4 w-full"
          >
            <CheckCircle2 className="mr-2 h-4 w-4" />
            Submit Solution
          </Button>
        )}
      </CardContent>
    </Card>
  )
}

export default ExerciseCard
