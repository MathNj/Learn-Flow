'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Avatar } from '@/components/ui/avatar'
import AlertsFeed from '@/components/teacher/alerts-feed'
import { mockStruggleAlerts } from '@/lib/mock-data'
import { useAuthStore } from '@/lib/stores/auth-store'
import {
  Users,
  AlertTriangle,
  TrendingUp,
  BookOpen,
  Code2,
  CheckCircle2,
} from 'lucide-react'

// Mock students data
const mockStudents = [
  { id: 'student-1', name: 'Alice Johnson', mastery: 65, streak: 5, status: 'online' },
  { id: 'student-2', name: 'Bob Smith', mastery: 42, streak: 2, status: 'struggling' },
  { id: 'student-3', name: 'Carol Davis', mastery: 78, streak: 8, status: 'online' },
  { id: 'student-4', name: 'David Lee', mastery: 35, streak: 0, status: 'offline' },
  { id: 'student-5', name: 'Eve Wilson', mastery: 88, streak: 12, status: 'online' },
]

export default function TeacherDashboardPage() {
  const { user } = useAuthStore()

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'bg-success-500'
      case 'struggling': return 'bg-error-500'
      default: return 'bg-slate-500'
    }
  }

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-4">
            <Link href="/" className="flex items-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-primary-700">
                <Code2 className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">LearnFlow</span>
            </Link>
            <Badge variant="warning" size="sm">Teacher Dashboard</Badge>
          </div>

          <nav className="flex items-center gap-6">
            <Link
              href="/app/teacher/dashboard"
              className="text-sm font-medium text-white"
            >
              Dashboard
            </Link>
            <Link
              href="/app/teacher/students"
              className="text-sm text-slate-400 hover:text-white transition-colors"
            >
              Students
            </Link>
            <Link
              href="/app/teacher/alerts"
              className="text-sm text-slate-400 hover:text-white transition-colors"
            >
              Alerts
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
              <p className="text-sm font-medium text-white">{user?.username || 'Teacher'}</p>
              <p className="text-xs text-slate-400">{user?.email || 'smith@learnflow.com'}</p>
            </div>
            <Avatar name={user?.username || 'Maria'} size="md" />
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">
            Teacher Dashboard
          </h1>
          <p className="mt-2 text-slate-400">
            Monitor your students' progress and respond to alerts.
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {/* Total Students */}
          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-500/10">
                  <Users className="h-6 w-6 text-primary-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">Total Students</p>
                  <p className="text-2xl font-bold text-white">24</p>
                  <p className="text-xs text-success-400">+3 this week</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Active Alerts */}
          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-error-500/10">
                  <AlertTriangle className="h-6 w-6 text-error-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">Active Alerts</p>
                  <p className="text-2xl font-bold text-white">{mockStruggleAlerts.length}</p>
                  <p className="text-xs text-error-400">Needs attention</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Avg Mastery */}
          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-success-500/10">
                  <TrendingUp className="h-6 w-6 text-success-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">Avg Mastery</p>
                  <p className="text-2xl font-bold text-white">62%</p>
                  <p className="text-xs text-success-400">+5% this week</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Completions */}
          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-warning-500/10">
                  <BookOpen className="h-6 w-6 text-warning-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">Exercises Done</p>
                  <p className="text-2xl font-bold text-white">156</p>
                  <p className="text-xs text-slate-400">This week</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-3">
          {/* Alerts Feed */}
          <div className="lg:col-span-2">
            <AlertsFeed alerts={mockStruggleAlerts} />
          </div>

          {/* Students List */}
          <Card className="border-slate-800 bg-slate-900/50">
            <CardHeader>
              <CardTitle className="text-white">Recent Students</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {mockStudents.map((student) => (
                  <Link
                    key={student.id}
                    href={`/app/teacher/students/${student.id}`}
                    className="block"
                  >
                    <div className="flex items-center gap-3 rounded-lg border border-slate-800 bg-slate-900/50 p-3 transition-colors hover:border-slate-700">
                      <div className="relative">
                        <Avatar name={student.name} size="sm" />
                        <div
                          className={`absolute -bottom-0.5 -right-0.5 h-3 w-3 rounded-full border-2 border-slate-900 ${getStatusColor(student.status)}`}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="truncate text-sm font-medium text-white">{student.name}</p>
                        <p className="text-xs text-slate-500">Mastery: {student.mastery}%</p>
                      </div>
                      <div className="text-right">
                        <p className="text-xs text-slate-400">{student.streak} day streak</p>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
              <Link href="/app/teacher/students">
                <Button variant="ghost" size="sm" className="mt-4 w-full">
                  View All Students
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>

        {/* Class Overview */}
        <Card className="mt-8 border-slate-800 bg-slate-900/50">
          <CardHeader>
            <CardTitle className="text-white">Class Performance Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {[
                { name: 'Python Basics', avg: 85, completed: 22 },
                { name: 'Control Flow', avg: 68, completed: 18 },
                { name: 'Data Structures', avg: 52, completed: 12 },
                { name: 'Functions', avg: 45, completed: 8 },
              ].map((module) => (
                <div key={module.name} className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
                  <p className="text-sm font-medium text-white">{module.name}</p>
                  <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-800">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-400"
                      style={{ width: `${module.avg}%` }}
                    />
                  </div>
                  <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
                    <span>{module.avg}% avg mastery</span>
                    <span>{module.completed} completed</span>
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
