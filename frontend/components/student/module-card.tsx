'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import MasteryRing from '@/components/shared/mastery-ring'
import { cn, getDifficultyColor } from '@/lib/utils'
import type { ModuleProgress } from '@/lib/types'
import { BookOpen, Clock, CheckCircle2, Lock } from 'lucide-react'

export interface ModuleCardProps {
  module: ModuleProgress
  isLocked?: boolean
  onClick?: () => void
  className?: string
}

const ModuleCard: React.FC<ModuleCardProps> = ({
  module,
  isLocked = false,
  onClick,
  className,
}) => {
  const getMasteryColor = (mastery: number): string => {
    if (mastery >= 91) return 'text-blue-600 dark:text-blue-400'
    if (mastery >= 71) return 'text-green-600 dark:text-green-400'
    if (mastery >= 41) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  return (
    <Card
      className={cn(
        'group transition-all hover:shadow-lg',
        isLocked && 'opacity-60',
        onClick && !isLocked && 'cursor-pointer',
        className
      )}
      onClick={!isLocked ? onClick : undefined}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-base">{module.moduleName}</CardTitle>
            <p className="mt-1 text-xs text-slate-500">
              {module.topicsCompleted} of {module.topicsTotal} topics completed
            </p>
          </div>

          {isLocked ? (
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
              <Lock className="h-5 w-5 text-slate-400" />
            </div>
          ) : (
            <MasteryRing
              mastery={module.mastery}
              level={module.level}
              size="sm"
              showLabel={false}
            />
          )}
        </div>
      </CardHeader>

      <CardContent>
        <Progress value={module.mastery} max={100} size="sm" showLabel={false} />

        <div className="mt-4 flex items-center justify-between text-xs text-slate-500">
          <span className={cn('font-semibold', getMasteryColor(module.mastery))}>
            {module.level}
          </span>
          <span>{module.mastery}% mastery</span>
        </div>

        {module.mastery === 100 && (
          <div className="mt-2 flex items-center gap-1 text-xs text-success-600 dark:text-success-400">
            <CheckCircle2 className="h-3.5 w-3.5" />
            <span className="font-medium">Completed</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default ModuleCard
