'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert } from '@/components/ui/alert'
import { useAuthStore } from '@/lib/stores/auth-store'
import { Code2, GraduationCap } from 'lucide-react'

export default function SignInPage() {
  const router = useRouter()
  const { setAuth } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      // Demo login - accept any credentials
      const user = {
        id: 'student-1',
        username: email.split('@')[0],
        email,
        role: 'student' as const,
        firstName: 'Demo',
        lastName: 'User',
        avatarUrl: `https://api.dicebear.com/7.x/avataaars/svg?seed=${email}`,
        createdAt: new Date().toISOString(),
      }

      setAuth(user, 'demo-token-' + Date.now())
      router.push('/app/student/dashboard')
    }, 500)
  }

  const handleDemoLogin = async (role: 'student' | 'teacher') => {
    setError('')
    setIsLoading(true)

    setTimeout(() => {
      const demoUsers = {
        student: {
          id: 'student-1',
          username: 'alice_student',
          email: 'alice@learnflow.com',
          role: 'student' as const,
          firstName: 'Alice',
          lastName: 'Johnson',
          avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alice',
          createdAt: '2025-01-01T00:00:00Z',
        },
        teacher: {
          id: 'teacher-1',
          username: 'msmith',
          email: 'smith@learnflow.com',
          role: 'teacher' as const,
          firstName: 'Maria',
          lastName: 'Smith',
          avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Maria',
          createdAt: '2024-12-01T00:00:00Z',
        },
      }

      setAuth(demoUsers[role], 'demo-token-' + Date.now())
      router.push(role === 'student' ? '/app/student/dashboard' : '/app/teacher/dashboard')
      setIsLoading(false)
    }, 500)
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-primary-900 p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary-500 to-primary-700 shadow-lg">
            <Code2 className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white">LearnFlow</h1>
          <p className="mt-2 text-slate-400">Master Python with AI Tutors</p>
        </div>

        <Card className="border-slate-700 bg-slate-900/50 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-white">Welcome back</CardTitle>
            <CardDescription className="text-slate-400">
              Sign in to continue your learning journey
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="error" title="Sign in failed">
                  {error}
                </Alert>
              )}

              <Input
                type="email"
                label="Email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="bg-slate-800"
              />

              <Input
                type="password"
                label="Password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="bg-slate-800"
              />

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center gap-2 text-slate-400">
                  <input type="checkbox" className="rounded border-slate-600" />
                  Remember me
                </label>
                <Link
                  href="/auth/forgot-password"
                  className="text-primary-400 hover:text-primary-300"
                >
                  Forgot password?
                </Link>
              </div>

              <Button
                type="submit"
                className="w-full"
                isLoading={isLoading}
                disabled={!email || !password}
              >
                Sign In
              </Button>
            </form>

            {/* Demo Accounts */}
            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-slate-700" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="bg-slate-900/50 px-2 text-slate-400">Or try demo accounts</span>
                </div>
              </div>

              <div className="mt-4 grid grid-cols-2 gap-3">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => handleDemoLogin('student')}
                  isLoading={isLoading}
                  className="h-9"
                >
                  <GraduationCap className="mr-2 h-4 w-4" />
                  Student
                </Button>
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => handleDemoLogin('teacher')}
                  isLoading={isLoading}
                  className="h-9"
                >
                  <GraduationCap className="mr-2 h-4 w-4" />
                  Teacher
                </Button>
              </div>
            </div>

            <p className="mt-6 text-center text-sm text-slate-400">
              Don't have an account?{' '}
              <Link href="/auth/sign-up" className="text-primary-400 hover:text-primary-300">
                Sign up
              </Link>
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
