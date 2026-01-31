'use client'

import React from 'react'
import { Card } from '@/components/ui/card'
import { Alert } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { CheckCircle2, XCircle, Clock, Terminal } from 'lucide-react'
import type { CodeRunResult } from '@/lib/types'

export interface CodeRunnerProps {
  result?: CodeRunResult | null
  isRunning?: boolean
  onClear?: () => void
  className?: string
}

const CodeRunner: React.FC<CodeRunnerProps> = ({
  result,
  isRunning = false,
  onClear,
  className,
}) => {
  if (isRunning) {
    return (
      <Card variant="default" className={cn('overflow-hidden', className)}>
        <div className="flex items-center gap-2 border-b border-slate-200 bg-slate-50 px-4 py-2 dark:border-slate-700 dark:bg-slate-800">
          <Terminal className="h-4 w-4 text-slate-500" />
          <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Output</span>
          <div className="ml-auto flex items-center gap-2">
            <div className="flex gap-1">
              <div className="h-2 w-2 animate-bounce rounded-full bg-primary-500 [animation-delay:-0.3s]" />
              <div className="h-2 w-2 animate-bounce rounded-full bg-primary-500 [animation-delay:-0.15s]" />
              <div className="h-2 w-2 animate-bounce rounded-full bg-primary-500" />
            </div>
          </div>
        </div>
        <div className="bg-slate-900 p-4">
          <p className="text-sm text-slate-400">Running your code...</p>
        </div>
      </Card>
    )
  }

  if (!result) {
    return (
      <Card variant="ghost" className={cn('overflow-hidden', className)}>
        <div className="flex items-center gap-2 border-b border-slate-200 bg-slate-50 px-4 py-2 dark:border-slate-700 dark:bg-slate-800">
          <Terminal className="h-4 w-4 text-slate-500" />
          <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Output</span>
          {onClear && (
            <Button size="sm" variant="ghost" onClick={onClear} className="ml-auto h-6 px-2">
              Clear
            </Button>
          )}
        </div>
        <div className="min-h-[100px] bg-slate-900 p-4">
          <p className="text-sm text-slate-500">
            Run your code to see the output here...
          </p>
        </div>
      </Card>
    )
  }

  const isSuccess = result.success && !result.error

  return (
    <Card variant="default" className={cn('overflow-hidden', className)}>
      <div className={cn(
        'flex items-center gap-2 border-b px-4 py-2',
        isSuccess
          ? 'bg-success-50 border-success-200 dark:bg-success-900/20 dark:border-success-800'
          : 'bg-error-50 border-error-200 dark:bg-error-900/20 dark:border-error-800'
      )}>
        {isSuccess ? (
          <CheckCircle2 className="h-4 w-4 text-success-600 dark:text-success-400" />
        ) : (
          <XCircle className="h-4 w-4 text-error-600 dark:text-error-400" />
        )}
        <span className={cn(
          'text-sm font-medium',
          isSuccess
            ? 'text-success-700 dark:text-success-300'
            : 'text-error-700 dark:text-error-300'
        )}>
          {isSuccess ? 'Success' : 'Error'}
        </span>
        <div className="ml-auto flex items-center gap-3 text-xs text-slate-500">
          {result.executionTime > 0 && (
            <div className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              <span>{result.executionTime}s</span>
            </div>
          )}
          {result.exitCode !== undefined && (
            <span>Exit: {result.exitCode}</span>
          )}
        </div>
        {onClear && (
          <Button size="sm" variant="ghost" onClick={onClear} className="ml-2 h-6 px-2">
            Clear
          </Button>
        )}
      </div>

      <div className="bg-slate-900 p-4">
        {/* Output */}
        {result.output && (
          <pre className="mb-2 whitespace-pre-wrap break-all text-sm text-slate-100">
            {result.output}
          </pre>
        )}

        {/* Error */}
        {result.error && (
          <Alert variant="error" className="mb-0">
            <pre className="whitespace-pre-wrap break-all text-xs">{result.error}</pre>
          </Alert>
        )}

        {/* Timeout notice */}
        {result.timeoutOccurred && (
          <Alert variant="warning" title="Execution Timeout">
            Your code took too long to run and was terminated. Please check for infinite loops.
          </Alert>
        )}
      </div>
    </Card>
  )
}

export default CodeRunner
