'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Avatar } from '@/components/ui/avatar'
import { cn, formatRelativeTime, getSeverityColor } from '@/lib/utils'
import type { StruggleAlert } from '@/lib/types'
import { mockStruggleAlerts } from '@/lib/mock-data'
import { AlertTriangle, Clock, RefreshCw, Check, XCircle, Code, CheckCircle2, Timer, TrendingDown, MessageCircle } from 'lucide-react'

export interface AlertsFeedProps {
  alerts?: StruggleAlert[]
  onAcknowledge?: (alertId: string) => void
  className?: string
}

const AlertsFeed: React.FC<AlertsFeedProps> = ({
  alerts = mockStruggleAlerts,
  onAcknowledge,
  className,
}) => {
  const [filter, setFilter] = useState<'all' | 'high' | 'medium' | 'low'>('all')
  const [acknowledged, setAcknowledged] = useState<Set<string>>(new Set())

  const filteredAlerts = alerts.filter((alert) =>
    filter === 'all' ? true : alert.severity === filter
  )

  const handleAcknowledge = (alertId: string) => {
    setAcknowledged((prev) => new Set(prev).add(alertId))
    onAcknowledge?.(alertId)
  }

  const getAlertIcon = (triggerType: string) => {
    switch (triggerType) {
      case 'repeated_error':
        return <RefreshCw className="h-4 w-4" />
      case 'time_exceeded':
        return <Timer className="h-4 w-4" />
      case 'low_quiz_score':
        return <TrendingDown className="h-4 w-4" />
      case 'keyword_phrase':
        return <MessageCircle className="h-4 w-4" />
      case 'failed_executions':
        return <XCircle className="h-4 w-4" />
      default:
        return <AlertTriangle className="h-4 w-4" />
    }
  }

  const getAlertDescription = (alert: StruggleAlert): string => {
    switch (alert.triggerType) {
      case 'repeated_error':
        return `encountered "${alert.context.errorType}" ${alert.context.errorCount} times`
      case 'time_exceeded':
        return `spent ${alert.context.timeSpentMinutes} minutes on this exercise`
      case 'low_quiz_score':
        return `scored ${alert.context.quizScore}% on the quiz`
      case 'keyword_phrase':
        return `said: "${alert.context.keyword}"`
      case 'failed_executions':
        return `had ${alert.context.failedExecutionCount} failed code runs`
      default:
        return 'needs assistance'
    }
  }

  return (
    <Card className={cn('', className)}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-warning-500" />
            Student Alerts
            {filteredAlerts.length > 0 && (
              <Badge variant="warning" size="sm">
                {filteredAlerts.length}
              </Badge>
            )}
          </CardTitle>

          {/* Filter tabs */}
          <div className="flex gap-1">
            {(['all', 'high', 'medium', 'low'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={cn(
                  'rounded-md px-2.5 py-1 text-xs font-medium capitalize transition-colors',
                  filter === f
                    ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400'
                    : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
                )}
              >
                {f}
              </button>
            ))}
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-0">
        {filteredAlerts.length === 0 ? (
          <div className="py-12 text-center">
            <CheckCircle2 className="mx-auto h-12 w-12 text-success-500" />
            <p className="mt-2 text-sm text-slate-500">No alerts at this time</p>
          </div>
        ) : (
          <div className="divide-y divide-slate-200 dark:divide-slate-700">
            {filteredAlerts.map((alert) => {
              const isAcknowledged = acknowledged.has(alert.id)

              return (
                <div
                  key={alert.id}
                  className={cn(
                    'p-4 transition-colors',
                    isAcknowledged && 'bg-slate-50/50 dark:bg-slate-800/50'
                  )}
                >
                  <div className="flex gap-3">
                    {/* Severity indicator */}
                    <div className={cn('w-1 rounded-full', getSeverityColor(alert.severity))} />

                    <div className="flex-1">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <Avatar name={alert.studentName} size="sm" />
                          <div>
                            <p className="font-medium text-slate-900 dark:text-slate-100">
                              {alert.studentName}
                            </p>
                            <p className="text-xs text-slate-500">
                              {formatRelativeTime(alert.createdAt)}
                            </p>
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          <Badge
                            variant={alert.severity === 'high' ? 'error' : alert.severity === 'medium' ? 'warning' : 'success'}
                            size="sm"
                          >
                            {alert.severity}
                          </Badge>
                        </div>
                      </div>

                      <div className="mt-2 rounded-lg bg-slate-100 p-3 dark:bg-slate-800">
                        <div className="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                          {getAlertIcon(alert.triggerType)}
                          <span className="font-medium capitalize">{alert.triggerType.replace('_', ' ')}</span>
                          <span className="text-slate-400">•</span>
                          <span>{getAlertDescription(alert)}</span>
                        </div>
                        {alert.context.lastCodeAttempt && (
                          <pre className="mt-2 overflow-x-auto rounded bg-slate-900 p-2 text-xs text-slate-300">
                            {alert.context.lastCodeAttempt}
                          </pre>
                        )}
                      </div>

                      {!isAcknowledged && (
                        <div className="mt-3 flex justify-end">
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleAcknowledge(alert.id)}
                            className="h-7"
                          >
                            <Check className="mr-1.5 h-3.5 w-3.5" />
                            Acknowledge
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default AlertsFeed
