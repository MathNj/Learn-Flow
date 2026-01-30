'use client'

import React from 'react'
import { cn } from '@/lib/utils'

export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'text' | 'circular' | 'rectangular' | 'rounded'
  width?: string | number
  height?: string | number
  count?: number
}

const Skeleton: React.FC<SkeletonProps> = ({
  variant = 'rectangular',
  width,
  height,
  count = 1,
  className,
  ...props
}) => {
  const baseClass = 'animate-pulse bg-slate-800'

  const variants = {
    text: 'h-4 w-full rounded',
    circular: 'rounded-full',
    rectangular: 'rounded-md',
    rounded: 'rounded-lg',
  }

  const skeletons = Array.from({ length: count }).map((_, i) => (
    <div
      key={i}
      className={cn(
        baseClass,
        variants[variant],
        className
      )}
      style={{ width, height }}
      {...props}
    />
  ))

  return count > 1 ? <div className="space-y-2">{skeletons}</div> : skeletons[0]
}

// Named skeleton components for common use cases
export const CardSkeleton: React.FC<{ className?: string }> = ({ className }) => (
  <div className={cn('rounded-lg border border-slate-800 bg-slate-900/50 p-6', className)}>
    <div className="flex items-start gap-4">
      <Skeleton variant="circular" width={48} height={48} />
      <div className="flex-1 space-y-2">
        <Skeleton variant="text" width="60%" />
        <Skeleton variant="text" width="40%" />
      </div>
    </div>
  </div>
)

export const ModuleCardSkeleton: React.FC<{ className?: string }> = ({ className }) => (
  <div className={cn('rounded-lg border border-slate-800 bg-slate-900/50 p-6', className)}>
    <Skeleton variant="rectangular" height={80} />
  </div>
)

export const TableSkeleton: React.FC<{ rows?: number; className?: string }> = ({ rows = 5, className }) => (
  <div className={cn('space-y-3', className)}>
    {Array.from({ length: rows }).map((_, i) => (
      <div key={i} className="flex items-center gap-4">
        <Skeleton variant="circular" width={40} height={40} />
        <Skeleton variant="text" width="30%" />
        <Skeleton variant="text" width="20%" />
        <Skeleton variant="text" width="15%" className="ml-auto" />
      </div>
    ))}
  </div>
)

export const ChatSkeleton: React.FC<{ className?: string }> = ({ className }) => (
  <div className={cn('space-y-4', className)}>
    {Array.from({ length: 3 }).map((_, i) => (
      <div key={i} className={cn('flex gap-3', i % 2 === 0 ? 'justify-start' : 'justify-end')}>
        {i % 2 === 0 && <Skeleton variant="circular" width={32} height={32} />}
        <Skeleton variant="rounded" width={i % 2 === 0 ? '80%' : '60%'} height={40} />
      </div>
    ))}
  </div>
)

export const DashboardSkeleton: React.FC<{ className?: string }> = ({ className }) => (
  <div className={cn('space-y-6', className)}>
    {/* Stats row */}
    <div className="grid grid-cols-4 gap-6">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="h-24 rounded-lg border border-slate-800 bg-slate-900/50 p-4" />
      ))}
    </div>
    {/* Content */}
    <Skeleton variant="rectangular" height={200} />
    <Skeleton variant="rectangular" height={200} />
  </div>
)

export default Skeleton
