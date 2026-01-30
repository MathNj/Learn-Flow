'use client'

import React from 'react'
import { cn, getMasteryColor } from '@/lib/utils'

export interface MasteryRingProps {
  mastery: number
  level?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  showLabel?: boolean
  animated?: boolean
  className?: string
}

const MasteryRing: React.FC<MasteryRingProps> = ({
  mastery,
  level,
  size = 'md',
  showLabel = true,
  animated = true,
  className,
}) => {
  const sizes = {
    sm: { width: 48, strokeWidth: 4 },
    md: { width: 64, strokeWidth: 5 },
    lg: { width: 96, strokeWidth: 6 },
    xl: { width: 128, strokeWidth: 8 },
  }

  const { width, strokeWidth } = sizes[size]
  const radius = (width - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const offset = circumference - (mastery / 100) * circumference
  const color = getMasteryColor(mastery)

  return (
    <div className={cn('flex flex-col items-center', className)}>
      <div className="relative" style={{ width, height: width }}>
        <svg width={width} height={width} className="-rotate-90">
          {/* Background circle */}
          <circle
            cx={width / 2}
            cy={width / 2}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={strokeWidth}
            className="text-slate-200 dark:text-slate-700"
          />
          {/* Progress circle */}
          <circle
            cx={width / 2}
            cy={width / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className={cn('transition-all duration-1000 ease-out', animated && 'animate-pulse')}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span
            className={cn(
              'font-bold',
              size === 'sm' && 'text-sm',
              size === 'md' && 'text-base',
              size === 'lg' && 'text-xl',
              size === 'xl' && 'text-2xl'
            )}
            style={{ color }}
          >
            {mastery}%
          </span>
        </div>
      </div>
      {showLabel && level && (
        <span
          className="mt-1 text-xs font-medium uppercase tracking-wide"
          style={{ color }}
        >
          {level}
        </span>
      )}
    </div>
  )
}

export default MasteryRing
