'use client'

import React from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { AlertTriangle, RefreshCw } from 'lucide-react'

interface Props {
  children: React.ReactNode
  fallback?: React.ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends React.Component<Props, State> {
  public state: State = {
    hasError: false,
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className="flex min-h-[400px] items-center justify-center p-4">
          <Card className="w-full max-w-md border-error-500/50 bg-error-500/5">
            <CardContent className="p-6">
              <div className="flex flex-col items-center text-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-error-500/10">
                  <AlertTriangle className="h-6 w-6 text-error-500" />
                </div>
                <h2 className="mt-4 text-lg font-semibold text-white">Something went wrong</h2>
                <p className="mt-2 text-sm text-slate-400">
                  {this.state.error?.message || 'An unexpected error occurred'}
                </p>
                <div className="mt-6 flex gap-3">
                  <Button
                    onClick={() => {
                      this.setState({ hasError: false })
                      window.location.reload()
                    }}
                  >
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Reload Page
                  </Button>
                  <Button variant="ghost" onClick={() => window.history.back()}>
                    Go Back
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )
    }

    return this.props.children
  }
}

// Hook-based error boundary for functional components
export function useErrorHandler() {
  return (error: Error, errorInfo: React.ErrorInfo) => {
    // Log error to error reporting service
    console.error('Error caught by error boundary:', error, errorInfo)
  }
}
