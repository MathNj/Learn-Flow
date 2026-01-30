'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import MasteryRing from '@/components/shared/mastery-ring'
import StreakDisplay from '@/components/shared/streak-display'
import ModuleCard from '@/components/student/module-card'
import { Avatar } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { mockStudentProgress, mockModules } from '@/lib/mock-data'
import { useAuthStore } from '@/lib/stores/auth-store'
import {
  BookOpen,
  TrendingUp,
  Clock,
  Target,
  Flame,
  ArrowRight,
  Code2,
} from 'lucide-react'

export default function StudentDashboardPage() {
  const { user } = useAuthStore()
  const progress = mockStudentProgress

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-4">
            <Link href="/app/student/dashboard" className="flex items-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-primary-700">
                <Code2 className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">LearnFlow</span>
            </Link>
          </div>

          <nav className="flex items-center gap-6">
            <Link
              href="/app/student/dashboard"
              className="text-sm font-medium text-white"
            >
              Dashboard
            </Link>
            <Link
              href="/app/student/learn"
              className="text-sm text-slate-400 hover:text-white transition-colors"
            >
              Learn
            </Link>
            <Link
              href="/auth/sign-in"
              className="text-sm text-slate-400 hover:text-white transition-colors"
            >
              Sign Out
            </Link>
          </nav>

          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-medium text-white">{user?.username || 'Student'}</p>
              <p className="text-xs text-slate-400">{user?.email || 'alice@learnflow.com'}</p>
            </div>
            <Avatar name={user?.username || 'Alice'} size="md" />
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">
            Welcome back, {user?.firstName || 'Alice'}!
          </h1>
          <p className="mt-2 text-slate-400">
            Continue your Python learning journey. You're making great progress!
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {/* Overall Mastery */}
          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <MasteryRing
                  mastery={progress.overallMastery}
                  level={progress.level}
                  size="lg"
                  showLabel={false}
                />
                <div>
                  <p className="text-sm text-slate-400">Overall Mastery</p>
                  <p className="text-2xl font-bold text-white">{progress.overallMastery}%</p>
                  <Badge variant="primary" size="sm" className="mt-1">
                    {progress.level}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Streak */}
          <StreakDisplay
            currentStreak={progress.currentStreak}
            longestStreak={progress.longestStreak}
          />

          {/* Modules Completed */}
          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-500/10">
                  <BookOpen className="h-6 w-6 text-primary-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">Modules Completed</p>
                  <p className="text-2xl font-bold text-white">
                    {progress.modules.filter((m) => m.mastery === 100).length}/{progress.modules.length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Time Spent */}
          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-success-500/10">
                  <Clock className="h-6 w-6 text-success-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">Time This Week</p>
                  <p className="text-2xl font-bold text-white">4.5h</p>
                  <p className="text-xs text-success-400">+1.2h from last week</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Continue Learning */}
        <div className="mt-8">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold text-white">Continue Learning</h2>
            <Link href="/app/student/learn">
              <Button size="sm" variant="ghost">
                View All
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {progress.modules.slice(0, 3).map((module, index) => (
              <ModuleCard
                key={module.moduleId}
                module={module}
                isLocked={index > 0 && progress.modules[index - 1].mastery < 70}
                onClick={() => {}}
              />
            ))}
          </div>
        </div>

        {/* Mastery Breakdown */}
        <Card className="mt-8 border-slate-800 bg-slate-900/50">
          <CardHeader>
            <CardTitle className="text-white">Mastery Breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {progress.modules.map((module) => (
                <div key={module.moduleId} className="flex items-center gap-4">
                  <div className="w-40 text-sm text-slate-300">{module.moduleName}</div>
                  <div className="flex-1">
                    <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-400 transition-all"
                        style={{ width: `${module.mastery}%` }}
                      />
                    </div>
                  </div>
                  <div className="w-16 text-right text-sm font-medium text-white">
                    {module.mastery}%
                  </div>
                  <Badge
                    variant={
                      module.mastery >= 71
                        ? 'success'
                        : module.mastery >= 41
                          ? 'warning'
                          : 'error'
                    }
                    size="sm"
                  >
                    {module.level}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="mt-8 border-slate-800 bg-slate-900/50">
          <CardHeader>
            <CardTitle className="text-white">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { action: 'Completed exercise', topic: 'For Loops', time: '2 hours ago' },
                { action: 'Started module', topic: 'Control Flow', time: '3 hours ago' },
                { action: 'Passed quiz', topic: 'Variables & Data Types', time: 'Yesterday' },
                { action: 'Earned badge', topic: '3-Day Streak', time: '2 days ago' },
              ].map((activity, index) => (
                <div key={index} className="flex items-center gap-4 border-b border-slate-800 pb-4 last:border-0 last:pb-0">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-500/10">
                    <Target className="h-5 w-5 text-primary-400" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-white">
                      <span className="font-medium">{activity.action}</span> - {activity.topic}
                    </p>
                    <p className="text-xs text-slate-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
