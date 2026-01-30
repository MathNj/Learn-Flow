'use client'

import React from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { cn } from '@/lib/utils'
import { Flame, TrendingUp, Award } from 'lucide-react'

export interface StreakDisplayProps {
  currentStreak: number
  longestStreak: number
  className?: string
}

const StreakDisplay: React.FC<StreakDisplayProps> = ({
  currentStreak,
  longestStreak,
  className,
}) => {
  const getStreakColor = (streak: number) => {
    if (streak >= 7) return 'text-orange-500'
    if (streak >= 3) return 'text-yellow-500'
    return 'text-slate-400'
  }

  return (
    <Card className={cn('', className)}>
      <CardContent className="p-4">
        <div className="flex items-center justify-around">
          <div className="text-center">
            <div className="flex items-center justify-center">
              <Flame className={cn('h-8 w-8', getStreakColor(currentStreak))} />
            </div>
            <p className="mt-1 text-2xl font-bold text-slate-900 dark:text-slate-100">
              {currentStreak}
            </p>
            <p className="text-xs text-slate-500">Current Streak</p>
          </div>

          <div className="h-10 w-px bg-slate-200 dark:bg-slate-700" />

          <div className="text-center">
            <div className="flex items-center justify-center">
              <Award className="h-6 w-6 text-purple-500" />
            </div>
            <p className="mt-1 text-lg font-semibold text-slate-900 dark:text-slate-100">
              {longestStreak}
            </p>
            <p className="text-xs text-slate-500">Longest Streak</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default StreakDisplay
