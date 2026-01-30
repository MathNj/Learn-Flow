'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import MasteryRing from '@/components/shared/mastery-ring'
import StreakDisplay from '@/components/shared/streak-display'
import { Avatar } from '@/components/ui/avatar'
import { Progress } from '@/components/ui/progress'
import { useAuthStore } from '@/lib/stores/auth-store'
import { mockStudentProgress } from '@/lib/mock-data'
import {
  Code2,
  ArrowLeft,
  Mail,
  Calendar,
  TrendingUp,
  Activity,
  Clock,
  CheckCircle2,
  XCircle,
} from 'lucide-react'

// Mock student data
const getMockStudent = (id: string) => ({
  id,
  name: 'Alice Johnson',
  username: 'alice_student',
  email: 'alice@learnflow.com',
  firstName: 'Alice',
  lastName: 'Johnson',
  role: 'student' as const,
  avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alice',
  createdAt: '2025-01-01T00:00:00Z',
  lastLoginAt: new Date().toISOString(),
})

// Mock activity data
const recentActivity = [
  { type: 'exercise', title: 'For Loops Exercise', status: 'passed', time: '2 hours ago' },
  { type: 'quiz', title: 'Variables Quiz', status: 'passed', score: 85, time: '3 hours ago' },
  { type: 'exercise', title: 'List Sum Function', status: 'failed', attempts: 3, time: '5 hours ago' },
  { type: 'code', title: 'Practice: Data Types', status: 'completed', time: 'Yesterday' },
  { type: 'login', title: 'Logged in', status: 'completed', time: 'Yesterday' },
]

// Mock struggle areas
const struggleAreas = [
  { topic: 'List Comprehensions', errorRate: 45, lastError: 'SyntaxError' },
  { topic: 'Classes & Objects', errorRate: 38, lastError: 'AttributeError' },
  { topic: 'File Handling', errorRate: 25, lastError: 'FileNotFoundError' },
]

export default function StudentDetailPage({ params }: { params: { studentId: string } }) {
  const { user } = useAuthStore()
  const student = getMockStudent(params.studentId)
  const progress = mockStudentProgress

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-4">
            <Link href="/app/teacher/dashboard" className="flex items-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-primary-700">
                <Code2 className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">LearnFlow</span>
            </Link>
            <Badge variant="warning" size="sm">Teacher</Badge>
          </div>

          <nav className="flex items-center gap-6">
            <Link href="/app/teacher/dashboard" className="text-sm text-slate-400 hover:text-white transition-colors">
              Dashboard
            </Link>
            <Link href="/app/teacher/students" className="text-sm text-slate-400 hover:text-white transition-colors">
              Students
            </Link>
            <Link href="/app/teacher/exercises" className="text-sm text-slate-400 hover:text-white transition-colors">
              Exercises
            </Link>
          </nav>

          <Avatar name={user?.username || 'Teacher'} size="md" />
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Back Button */}
        <Link href="/app/teacher/dashboard">
          <Button variant="ghost" size="sm" className="mb-6">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Dashboard
          </Button>
        </Link>

        {/* Student Header */}
        <Card className="mb-8 border-slate-800 bg-slate-900/50">
          <CardContent className="p-6">
            <div className="flex items-start gap-6">
              <Avatar name={student.name} size="xl" />
              <div className="flex-1">
                <h1 className="text-2xl font-bold text-white">{student.name}</h1>
                <p className="text-slate-400">@{student.username}</p>
                <div className="mt-3 flex flex-wrap gap-4 text-sm text-slate-400">
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4" />
                    {student.email}
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    Joined {new Date(student.createdAt).toLocaleDateString()}
                  </div>
                  <div className="flex items-center gap-2">
                    <Activity className="h-4 w-4" />
                    Last active {new Date(student.lastLoginAt).toLocaleString()}
                  </div>
                </div>
              </div>

              {/* Mastery Ring */}
              <div className="text-center">
                <MasteryRing
                  mastery={progress.overallMastery}
                  level={progress.level}
                  size="xl"
                  showLabel
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stats Grid */}
        <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-4">
          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-4">
              <p className="text-sm text-slate-400">Current Streak</p>
              <p className="text-2xl font-bold text-white">{progress.currentStreak} days</p>
            </CardContent>
          </Card>

          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-4">
              <p className="text-sm text-slate-400">Exercises Done</p>
              <p className="text-2xl font-bold text-white">32</p>
            </CardContent>
          </Card>

          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-4">
              <p className="text-sm text-slate-400">Quizzes Passed</p>
              <p className="text-2xl font-bold text-white">8/12</p>
            </CardContent>
          </Card>

          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-4">
              <p className="text-sm text-slate-400">Time This Week</p>
              <p className="text-2xl font-bold text-white">4.5h</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {/* Module Progress */}
          <div className="lg:col-span-2">
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Module Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {progress.modules.map((module) => (
                    <div key={module.moduleId} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-white">{module.moduleName}</span>
                        <div className="flex items-center gap-2">
                          <span className="text-sm text-slate-400">{module.mastery}%</span>
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
                      </div>
                      <Progress value={module.mastery} size="sm" />
                      <p className="text-xs text-slate-500">
                        {module.topicsCompleted} of {module.topicsTotal} topics completed
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recent Activity */}
            <Card className="mt-6 border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {recentActivity.map((activity, index) => (
                    <div
                      key={index}
                      className="flex items-center gap-3 border-b border-slate-800 pb-3 last:border-0 last:pb-0"
                    >
                      <div
                        className={`flex h-8 w-8 items-center justify-center rounded-full ${
                          activity.status === 'passed' || activity.status === 'completed'
                            ? 'bg-success-500/10'
                            : activity.status === 'failed'
                              ? 'bg-error-500/10'
                              : 'bg-slate-800'
                        }`}
                      >
                        {activity.status === 'passed' || activity.status === 'completed' ? (
                          <CheckCircle2 className="h-4 w-4 text-success-500" />
                        ) : activity.status === 'failed' ? (
                          <XCircle className="h-4 w-4 text-error-500" />
                        ) : (
                          <Clock className="h-4 w-4 text-slate-500" />
                        )}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-white">{activity.title}</p>
                        <p className="text-xs text-slate-500">
                          {activity.type === 'exercise' && 'Exercise'}
                          {activity.type === 'quiz' && `Quiz - Score: ${activity.score}%`}
                          {activity.type === 'code' && 'Code Practice'}
                          {activity.type === 'login' && 'Login'}
                          {' • ' + activity.time}
                        </p>
                      </div>
                      {activity.attempts && (
                        <Badge variant="warning" size="sm">
                          {activity.attempts} attempts
                        </Badge>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Struggle Areas */}
          <div>
            <StreakDisplay
              currentStreak={progress.currentStreak}
              longestStreak={progress.longestStreak}
            />

            <Card className="mt-6 border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Areas Needing Help</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {struggleAreas.map((area) => (
                    <div
                      key={area.topic}
                      className="rounded-lg border border-error-500/30 bg-error-500/5 p-3"
                    >
                      <div className="flex items-center justify-between">
                        <p className="font-medium text-white">{area.topic}</p>
                        <Badge variant="error" size="sm">
                          {area.errorRate}% error rate
                        </Badge>
                      </div>
                      <p className="mt-1 text-xs text-slate-400">
                        Last error: <span className="text-error-400">{area.lastError}</span>
                      </p>
                      <Button size="sm" variant="ghost" className="mt-2 h-7 text-xs">
                        Send Practice Exercise
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card className="mt-6 border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button variant="outline" size="sm" className="w-full justify-start">
                  <TrendingUp className="mr-2 h-4 w-4" />
                  View Detailed Progress
                </Button>
                <Button variant="outline" size="sm" className="w-full justify-start">
                  <Mail className="mr-2 h-4 w-4" />
                  Send Message
                </Button>
                <Button variant="outline" size="sm" className="w-full justify-start">
                  Generate Custom Exercise
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
