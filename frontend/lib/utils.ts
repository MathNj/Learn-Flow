import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(d)
}

export function formatTime(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  }).format(d)
}

export function formatRelativeTime(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date
  const now = new Date()
  const diff = Math.floor((now.getTime() - d.getTime()) / 1000)

  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`
  return formatDate(d)
}

export function getInitials(name: string): string {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

export function getMasteryColor(mastery: number): string {
  if (mastery >= 91) return 'hsl(211, 100%, 50%)' // Blue - Mastered
  if (mastery >= 71) return 'hsl(142, 76%, 36%)' // Green - Proficient
  if (mastery >= 41) return 'hsl(38, 92%, 50%)' // Yellow - Learning
  return 'hsl(0, 84%, 60%)' // Red - Beginner
}

export function getMasteryLevel(mastery: number): string {
  if (mastery >= 91) return 'Mastered'
  if (mastery >= 71) return 'Proficient'
  if (mastery >= 41) return 'Learning'
  return 'Beginner'
}

export function getSeverityColor(severity: 'low' | 'medium' | 'high'): string {
  switch (severity) {
    case 'high': return 'bg-error-500'
    case 'medium': return 'bg-warning-500'
    case 'low': return 'bg-success-500'
  }
}

export function getDifficultyColor(difficulty: string): string {
  switch (difficulty) {
    case 'beginner': return 'bg-success-100 text-success-700 dark:bg-success-900/30 dark:text-success-400'
    case 'intermediate': return 'bg-warning-100 text-warning-700 dark:bg-warning-900/30 dark:text-warning-400'
    case 'advanced': return 'bg-error-100 text-error-700 dark:bg-error-900/30 dark:text-error-400'
    default: return 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300'
  }
}
