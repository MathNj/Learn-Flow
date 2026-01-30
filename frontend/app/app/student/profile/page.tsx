'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Avatar } from '@/components/ui/avatar'
import MasteryRing from '@/components/shared/mastery-ring'
import StreakDisplay from '@/components/shared/streak-display'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { Alert } from '@/components/ui/alert'
import { useAuthStore } from '@/lib/stores/auth-store'
import { mockStudentProgress, mockModules } from '@/lib/mock-data'
import {
  Code2,
  User,
  Bell,
  Lock,
  Mail,
  Calendar,
  Trophy,
  Target,
  Flame,
  CheckCircle2,
} from 'lucide-react'

export default function ProfilePage() {
  const { user, updateUser } = useAuthStore()
  const [isEditing, setIsEditing] = useState(false)
  const [editedUser, setEditedUser] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
    username: user?.username || '',
  })
  const [saveMessage, setSaveMessage] = useState('')

  const handleSave = () => {
    updateUser(editedUser)
    setIsEditing(false)
    setSaveMessage('Profile updated successfully!')
    setTimeout(() => setSaveMessage(''), 3000)
  }

  const progress = mockStudentProgress

  // Calculate stats
  const totalExercises = 45
  const completedExercises = 32
  const totalQuizzes = 12
  const passedQuizzes = 8

  const achievements = [
    { id: 1, name: 'First Steps', description: 'Complete your first exercise', icon: '👶', earned: true },
    { id: 2, name: 'Code Warrior', description: 'Complete 10 exercises', icon: '⚔️', earned: true },
    { id: 3, name: 'Quiz Master', description: 'Score 100% on a quiz', icon: '🏆', earned: true },
    { id: 4, name: 'Week Warrior', description: '7 day learning streak', icon: '🔥', earned: true },
    { id: 5, name: 'Module Master', description: 'Complete a module', icon: '📚', earned: false },
    { id: 6, name: 'Perfect Score', description: '100% mastery in any topic', icon: '💯', earned: false },
  ]

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
              className="text-sm text-slate-400 hover:text-white transition-colors"
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
              href="/app/student/profile"
              className="text-sm font-medium text-white"
            >
              Profile
            </Link>
            <Link
              href="/auth/sign-in"
              className="text-sm text-slate-400 hover:text-white transition-colors"
            >
              Sign Out
            </Link>
          </nav>

          <Avatar name={user?.username || 'Student'} size="md" />
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Profile Header */}
        <Card className="mb-8 border-slate-800 bg-slate-900/50">
          <CardContent className="p-6">
            <div className="flex items-start gap-6">
              <Avatar name={user?.username || 'Student'} size="xl" />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <div>
                    <h1 className="text-2xl font-bold text-white">
                      {user?.firstName} {user?.lastName}
                    </h1>
                    <p className="text-slate-400">@{user?.username}</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsEditing(!isEditing)}
                  >
                    <User className="mr-2 h-4 w-4" />
                    {isEditing ? 'Cancel' : 'Edit Profile'}
                  </Button>
                </div>

                {isEditing ? (
                  <div className="mt-4 space-y-3">
                    {saveMessage && (
                      <Alert variant="success">{saveMessage}</Alert>
                    )}
                    <div className="grid grid-cols-2 gap-3">
                      <Input
                        label="First Name"
                        value={editedUser.firstName}
                        onChange={(e) => setEditedUser({ ...editedUser, firstName: e.target.value })}
                        className="bg-slate-800"
                      />
                      <Input
                        label="Last Name"
                        value={editedUser.lastName}
                        onChange={(e) => setEditedUser({ ...editedUser, lastName: e.target.value })}
                        className="bg-slate-800"
                      />
                    </div>
                    <Input
                      label="Username"
                      value={editedUser.username}
                      onChange={(e) => setEditedUser({ ...editedUser, username: e.target.value })}
                      className="bg-slate-800"
                    />
                    <Input
                      label="Email"
                      type="email"
                      value={editedUser.email}
                      onChange={(e) => setEditedUser({ ...editedUser, email: e.target.value })}
                      className="bg-slate-800"
                    />
                    <div className="flex gap-2">
                      <Button onClick={handleSave} size="sm">
                        Save Changes
                      </Button>
                      <Button variant="ghost" size="sm" onClick={() => setIsEditing(false)}>
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="mt-4 flex flex-wrap gap-4 text-sm text-slate-400">
                    <div className="flex items-center gap-2">
                      <Mail className="h-4 w-4" />
                      {user?.email}
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4" />
                      Joined {new Date(user?.createdAt || '').toLocaleDateString()}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-500/10">
                  <Target className="h-6 w-6 text-primary-400" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-white">{completedExercises}/{totalExercises}</p>
                  <p className="text-sm text-slate-400">Exercises Done</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-success-500/10">
                  <Trophy className="h-6 w-6 text-success-400" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-white">{passedQuizzes}/{totalQuizzes}</p>
                  <p className="text-sm text-slate-400">Quizzes Passed</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-800 bg-slate-900/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-warning-500/10">
                  <Flame className="h-6 w-6 text-warning-400" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-white">{progress.currentStreak}</p>
                  <p className="text-sm text-slate-400">Day Streak</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="progress" className="mt-8">
          <TabsList>
            <TabsTrigger value="progress">Progress</TabsTrigger>
            <TabsTrigger value="achievements">Achievements</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          <TabsContent value="progress" className="mt-6">
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Learning Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="mb-6 flex items-center justify-center">
                  <MasteryRing
                    mastery={progress.overallMastery}
                    level={progress.level}
                    size="xl"
                  />
                </div>

                <div className="space-y-4">
                  {progress.modules.map((module) => (
                    <div key={module.moduleId} className="flex items-center gap-4">
                      <div className="w-40 text-sm text-slate-300">{module.moduleName}</div>
                      <div className="flex-1">
                        <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                          <div
                            className="h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-400"
                            style={{ width: `${module.mastery}%` }}
                          />
                        </div>
                      </div>
                      <div className="w-12 text-right text-sm font-medium text-white">
                        {module.mastery}%
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="achievements" className="mt-6">
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Achievements</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  {achievements.map((achievement) => (
                    <div
                      key={achievement.id}
                      className={`flex items-center gap-4 rounded-lg border p-4 ${
                        achievement.earned
                          ? 'border-slate-700 bg-slate-800'
                          : 'border-slate-800 bg-slate-900/50 opacity-50'
                      }`}
                    >
                      <div className="text-4xl">{achievement.icon}</div>
                      <div className="flex-1">
                        <p className="font-medium text-white">{achievement.name}</p>
                        <p className="text-sm text-slate-400">{achievement.description}</p>
                      </div>
                      {achievement.earned && (
                        <CheckCircle2 className="h-5 w-5 text-success-500" />
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="settings" className="mt-6">
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Notifications */}
                <div>
                  <h3 className="mb-3 flex items-center gap-2 font-medium text-white">
                    <Bell className="h-4 w-4" />
                    Notifications
                  </h3>
                  <div className="space-y-3">
                    {['Email reminders', 'Weekly progress report', 'New module alerts'].map((label) => (
                      <div key={label} className="flex items-center justify-between">
                        <span className="text-sm text-slate-300">{label}</span>
                        <button className="relative h-6 w-11 rounded-full bg-primary-600 transition-colors">
                          <span className="absolute left-0.5 top-0.5 h-5 w-5 rounded-full bg-white transition-transform translate-x-5" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Security */}
                <div>
                  <h3 className="mb-3 flex items-center gap-2 font-medium text-white">
                    <Lock className="h-4 w-4" />
                    Security
                  </h3>
                  <div className="space-y-3">
                    <Button variant="outline" size="sm" className="w-full justify-start">
                      Change Password
                    </Button>
                    <Button variant="outline" size="sm" className="w-full justify-start">
                      Enable Two-Factor Authentication
                    </Button>
                  </div>
                </div>

                {/* Danger Zone */}
                <div className="border-t border-slate-800 pt-6">
                  <h3 className="mb-3 font-medium text-error-400">Danger Zone</h3>
                  <Button variant="ghost" size="sm" className="text-error-400 hover:text-error-300">
                    Delete Account
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
