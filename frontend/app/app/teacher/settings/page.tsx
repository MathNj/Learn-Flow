'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Alert } from '@/components/ui/alert'
import { Avatar } from '@/components/ui/avatar'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { useAuthStore } from '@/lib/stores/auth-store'
import {
  Code2,
  Users,
  Settings,
  Bell,
  Lock,
  Copy,
  Check,
  Plus,
  Trash2,
  Mail,
  UserPlus,
} from 'lucide-react'

// Mock class data
const classData = {
  name: 'Introduction to Python - Spring 2025',
  code: 'PYTHON-101-S25',
  description: 'Learn the fundamentals of Python programming including variables, data types, control flow, functions, and more.',
  studentCount: 24,
  inviteLink: 'https://learnflow.com/join/PYTHON-101-S25',
}

const mockStudents = [
  { id: 'student-1', name: 'Alice Johnson', email: 'alice@example.com', joinedAt: '2025-01-01' },
  { id: 'student-2', name: 'Bob Smith', email: 'bob@example.com', joinedAt: '2025-01-02' },
  { id: 'student-3', name: 'Carol Davis', email: 'carol@example.com', joinedAt: '2025-01-03' },
  { id: 'student-4', name: 'David Lee', email: 'david@example.com', joinedAt: '2025-01-05' },
  { id: 'student-5', name: 'Eve Wilson', email: 'eve@example.com', joinedAt: '2025-01-08' },
]

export default function ClassSettingsPage() {
  const { user } = useAuthStore()
  const [copied, setCopied] = useState(false)
  const [saveMessage, setSaveMessage] = useState('')

  const [classSettings, setClassSettings] = useState({
    name: classData.name,
    description: classData.description,
    allowGuestAccess: true,
    requireApproval: false,
    maxStudents: 50,
  })

  const [notificationSettings, setNotificationSettings] = useState({
    weeklyProgressReport: true,
    struggleAlerts: true,
    newStudentJoined: true,
    exerciseCompleted: false,
  })

  const handleCopyInvite = () => {
    navigator.clipboard.writeText(classData.inviteLink)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleSaveClass = () => {
    setSaveMessage('Class settings saved successfully!')
    setTimeout(() => setSaveMessage(''), 3000)
  }

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
            <Link href="/app/teacher/settings" className="text-sm font-medium text-white">
              Settings
            </Link>
          </nav>

          <Avatar name={user?.username || 'Teacher'} size="md" />
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-white">Class Settings</h1>
        <p className="mt-2 text-slate-400">
          Manage your class information, students, and preferences.
        </p>

        <Tabs defaultValue="general" className="mt-8">
          <TabsList>
            <TabsTrigger value="general">General</TabsTrigger>
            <TabsTrigger value="students">Students</TabsTrigger>
            <TabsTrigger value="notifications">Notifications</TabsTrigger>
          </TabsList>

          {/* General Settings */}
          <TabsContent value="general" className="mt-6 space-y-6">
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Class Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {saveMessage && (
                  <Alert variant="success">{saveMessage}</Alert>
                )}

                <Input
                  label="Class Name"
                  value={classSettings.name}
                  onChange={(e) => setClassSettings({ ...classSettings, name: e.target.value })}
                  className="bg-slate-800"
                />

                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Description
                  </label>
                  <Textarea
                    value={classSettings.description}
                    onChange={(e) => setClassSettings({ ...classSettings, description: e.target.value })}
                    rows={3}
                    className="bg-slate-800"
                  />
                </div>

                <Input
                  label="Class Code"
                  value={classData.code}
                  readOnly
                  className="bg-slate-800"
                />
              </CardContent>
            </Card>

            {/* Invite Link */}
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Invite Students</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-slate-400">
                  Share this link with students to let them join your class.
                </p>

                <div className="flex gap-2">
                  <Input
                    value={classData.inviteLink}
                    readOnly
                    className="bg-slate-800 font-mono text-sm"
                  />
                  <Button onClick={handleCopyInvite} variant="secondary">
                    {copied ? (
                      <>
                        <Check className="mr-2 h-4 w-4" />
                        Copied
                      </>
                    ) : (
                      <>
                        <Copy className="mr-2 h-4 w-4" />
                        Copy
                      </>
                    )}
                  </Button>
                </div>

                <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-white">Students Enrolled</p>
                      <p className="text-2xl font-bold text-primary-400">
                        {classData.studentCount} / {classSettings.maxStudents}
                      </p>
                    </div>
                    <div className="h-16 w-16">
                      <svg viewBox="0 0 36 36" className="h-full w-full">
                        <path
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none"
                          stroke="#1e293b"
                          strokeWidth="3"
                        />
                        <path
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831"
                          fill="none"
                          stroke="#3b82f6"
                          strokeWidth="3"
                          strokeDasharray={`${(classData.studentCount / classSettings.maxStudents) * 100}, 100`}
                        />
                      </svg>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Access Control */}
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Access Control</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-white">Allow Guest Access</p>
                    <p className="text-sm text-slate-400">
                      Students can preview content before joining
                    </p>
                  </div>
                  <button
                    onClick={() =>
                      setClassSettings({ ...classSettings, allowGuestAccess: !classSettings.allowGuestAccess })
                    }
                    className={`relative h-6 w-11 rounded-full transition-colors ${
                      classSettings.allowGuestAccess ? 'bg-primary-600' : 'bg-slate-700'
                    }`}
                  >
                    <span
                      className={`absolute top-0.5 h-5 w-5 rounded-full bg-white transition-transform ${
                        classSettings.allowGuestAccess ? 'translate-x-5' : 'translate-x-0.5'
                      }`}
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-white">Require Approval</p>
                    <p className="text-sm text-slate-400">
                      Manually approve student join requests
                    </p>
                  </div>
                  <button
                    onClick={() =>
                      setClassSettings({ ...classSettings, requireApproval: !classSettings.requireApproval })
                    }
                    className={`relative h-6 w-11 rounded-full transition-colors ${
                      classSettings.requireApproval ? 'bg-primary-600' : 'bg-slate-700'
                    }`}
                  >
                    <span
                      className={`absolute top-0.5 h-5 w-5 rounded-full bg-white transition-transform ${
                        classSettings.requireApproval ? 'translate-x-5' : 'translate-x-0.5'
                      }`}
                    />
                  </button>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Maximum Students
                  </label>
                  <Input
                    type="number"
                    value={classSettings.maxStudents}
                    onChange={(e) => setClassSettings({ ...classSettings, maxStudents: Number(e.target.value) })}
                    className="bg-slate-800"
                  />
                </div>

                <Button onClick={handleSaveClass} className="w-full">
                  Save Changes
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Students Management */}
          <TabsContent value="students" className="mt-6">
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white">Class Roster</CardTitle>
                  <Button size="sm">
                    <UserPlus className="mr-2 h-4 w-4" />
                    Add Student
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {mockStudents.map((student) => (
                    <div
                      key={student.id}
                      className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-900/50 p-3"
                    >
                      <div className="flex items-center gap-3">
                        <Avatar name={student.name} size="sm" />
                        <div>
                          <p className="font-medium text-white">{student.name}</p>
                          <p className="text-xs text-slate-500">{student.email}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-xs text-slate-500">
                          Joined {new Date(student.joinedAt).toLocaleDateString()}
                        </span>
                        <Link href={`/app/teacher/students/${student.id}`}>
                          <Button size="sm" variant="ghost">
                            View
                          </Button>
                        </Link>
                        <Button size="sm" variant="ghost">
                          <Trash2 className="h-4 w-4 text-error-400" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-4 text-center">
                  <Button variant="outline" size="sm">
                    Load More Students
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Notifications */}
          <TabsContent value="notifications" className="mt-6">
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Bell className="h-5 w-5" />
                  Notification Preferences
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <p className="text-sm text-slate-400">
                  Choose which notifications you want to receive about your class.
                </p>

                <div className="space-y-4">
                  {[
                    {
                      key: 'weeklyProgressReport',
                      title: 'Weekly Progress Report',
                      description: 'Get a summary of class progress every week',
                      icon: '📊',
                    },
                    {
                      key: 'struggleAlerts',
                      title: 'Student Struggle Alerts',
                      description: 'Immediate notifications when students need help',
                      icon: '🚨',
                    },
                    {
                      key: 'newStudentJoined',
                      title: 'New Student Joined',
                      description: 'Notify when a new student joins your class',
                      icon: '👋',
                    },
                    {
                      key: 'exerciseCompleted',
                      title: 'Exercise Completed',
                      description: 'Get notified when students complete exercises',
                      icon: '✅',
                    },
                  ].map((setting) => (
                    <div
                      key={setting.key}
                      className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-900/50 p-4"
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{setting.icon}</span>
                        <div>
                          <p className="font-medium text-white">{setting.title}</p>
                          <p className="text-sm text-slate-400">{setting.description}</p>
                        </div>
                      </div>
                      <button
                        onClick={() =>
                          setNotificationSettings({
                            ...notificationSettings,
                            [setting.key]: !notificationSettings[
                              setting.key as keyof typeof notificationSettings
                            ],
                          })
                        }
                        className={`relative h-6 w-11 rounded-full transition-colors ${
                          notificationSettings[
                            setting.key as keyof typeof notificationSettings
                          ]
                            ? 'bg-primary-600'
                            : 'bg-slate-700'
                        }`}
                      >
                        <span
                          className={`absolute top-0.5 h-5 w-5 rounded-full bg-white transition-transform ${
                            notificationSettings[
                              setting.key as keyof typeof notificationSettings
                            ]
                              ? 'translate-x-5'
                              : 'translate-x-0.5'
                          }`}
                        />
                      </button>
                    </div>
                  ))}
                </div>

                <Button className="w-full">Save Notification Settings</Button>
              </CardContent>
            </Card>

            {/* Email Settings */}
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Mail className="h-5 w-5" />
                  Email Settings
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Input
                  label="Notification Email"
                  value={user?.email || ''}
                  className="bg-slate-800"
                />

                <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
                  <p className="text-sm text-white font-medium">Email Digest</p>
                  <div className="mt-3 space-y-2">
                    {['Daily', 'Weekly', 'Never'].map((freq) => (
                      <label
                        key={freq}
                        className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer"
                      >
                        <input
                          type="radio"
                          name="digest"
                          defaultChecked={freq === 'Weekly'}
                          className="text-primary-500"
                        />
                        {freq}
                      </label>
                    ))}
                  </div>
                </div>

                <Button variant="outline" className="w-full">
                  Update Email Preferences
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
