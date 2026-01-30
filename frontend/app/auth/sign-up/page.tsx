'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert } from '@/components/ui/alert'
import { useAuthStore } from '@/lib/stores/auth-store'
import { Code2, User, GraduationCap } from 'lucide-react'

export default function SignUpPage() {
  const router = useRouter()
  const { setAuth } = useAuthStore()
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'student' as 'student' | 'teacher',
  })
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters')
      return
    }

    setIsLoading(true)

    // Simulate account creation
    setTimeout(() => {
      const user = {
        id: 'user-' + Date.now(),
        username: formData.username,
        email: formData.email,
        role: formData.role,
        firstName: formData.username,
        lastName: '',
        avatarUrl: `https://api.dicebear.com/7.x/avataaars/svg?seed=${formData.username}`,
        createdAt: new Date().toISOString(),
      }

      setAuth(user, 'demo-token-' + Date.now())
      router.push(formData.role === 'student' ? '/app/student/dashboard' : '/app/teacher/dashboard')
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
          <p className="mt-2 text-slate-400">Start your Python learning journey</p>
        </div>

        <Card className="border-slate-700 bg-slate-900/50 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-white">Create an account</CardTitle>
            <CardDescription className="text-slate-400">
              Join thousands of students learning Python
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="error" title="Sign up failed">
                  {error}
                </Alert>
              )}

              <Input
                type="text"
                name="username"
                label="Username"
                placeholder="johndoe"
                value={formData.username}
                onChange={handleChange}
                required
                className="bg-slate-800"
              />

              <Input
                type="email"
                name="email"
                label="Email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                required
                className="bg-slate-800"
              />

              <Input
                type="password"
                name="password"
                label="Password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
                minLength={8}
                className="bg-slate-800"
              />

              <Input
                type="password"
                name="confirmPassword"
                label="Confirm Password"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                className="bg-slate-800"
              />

              {/* Role Selection */}
              <div>
                <label className="mb-1.5 block text-sm font-medium text-slate-300">
                  I am a...
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setFormData((prev) => ({ ...prev, role: 'student' }))}
                    className={`flex flex-col items-center gap-2 rounded-lg border-2 p-4 transition-colors ${
                      formData.role === 'student'
                        ? 'border-primary-500 bg-primary-500/10 text-primary-400'
                        : 'border-slate-700 bg-slate-800 text-slate-400 hover:border-slate-600'
                    }`}
                  >
                    <GraduationCap className="h-6 w-6" />
                    <span className="font-medium">Student</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setFormData((prev) => ({ ...prev, role: 'teacher' }))}
                    className={`flex flex-col items-center gap-2 rounded-lg border-2 p-4 transition-colors ${
                      formData.role === 'teacher'
                        ? 'border-primary-500 bg-primary-500/10 text-primary-400'
                        : 'border-slate-700 bg-slate-800 text-slate-400 hover:border-slate-600'
                    }`}
                  >
                    <User className="h-6 w-6" />
                    <span className="font-medium">Teacher</span>
                  </button>
                </div>
              </div>

              <Button
                type="submit"
                className="w-full"
                isLoading={isLoading}
                disabled={!formData.username || !formData.email || !formData.password}
              >
                Create Account
              </Button>

              <p className="mt-6 text-center text-sm text-slate-400">
                Already have an account?{' '}
                <Link href="/auth/sign-in" className="text-primary-400 hover:text-primary-300">
                  Sign in
                </Link>
              </p>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
