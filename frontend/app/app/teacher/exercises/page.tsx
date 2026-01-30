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
import { useAuthStore } from '@/lib/stores/auth-store'
import { mockModules } from '@/lib/mock-data'
import {
  Code2,
  Plus,
  Wand2,
  Save,
  Eye,
  Trash2,
  ArrowLeft,
} from 'lucide-react'

// Mock existing exercises
const existingExercises = [
  {
    id: 'ex-001',
    title: 'Create Your First Variable',
    topic: 'Variables & Data Types',
    difficulty: 'beginner',
  },
  {
    id: 'ex-002',
    title: 'Write a For Loop',
    topic: 'Loops',
    difficulty: 'intermediate',
  },
]

export default function ExerciseGeneratorPage() {
  const { user } = useAuthStore()
  const [mode, setMode] = useState<'list' | 'create' | 'ai'>('list')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedExercise, setGeneratedExercise] = useState<any>(null)

  // Form state
  const [formData, setFormData] = useState({
    topicId: 1,
    difficulty: 'beginner',
    title: '',
    description: '',
    starterCode: '# Write your starter code here\n',
    solutionCode: '',
    hints: ['', ''],
  })

  const [aiPrompt, setAiPrompt] = useState('')

  const difficulties = ['beginner', 'intermediate', 'advanced'] as const

  const handleGenerateAI = () => {
    setIsGenerating(true)
    // Simulate AI generation
    setTimeout(() => {
      setGeneratedExercise({
        id: 'ex-new-' + Date.now(),
        title: 'Calculate List Sum',
        description: 'Write a function that calculates the sum of all elements in a list.',
        starterCode: 'def calculate_sum(numbers):\n    # Your code here\n    pass\n',
        solutionCode: 'def calculate_sum(numbers):\n    return sum(numbers)\n',
        hints: [
          'Use the built-in sum() function',
          'You can also use a for loop to iterate and add',
        ],
      })
      setIsGenerating(false)
      setMode('create')
    }, 2000)
  }

  const handleSave = () => {
    // Simulate save
    alert('Exercise saved successfully!')
    setMode('list')
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
            <Link href="/app/teacher/exercises" className="text-sm font-medium text-white">
              Exercises
            </Link>
            <Link href="/app/teacher/students" className="text-sm text-slate-400 hover:text-white transition-colors">
              Students
            </Link>
          </nav>

          <Avatar name={user?.username || 'Teacher'} size="md" />
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
        {/* List View */}
        {mode === 'list' && (
          <>
            <div className="mb-8 flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white">Exercise Generator</h1>
                <p className="mt-2 text-slate-400">
                  Create custom exercises for your students or let AI generate them for you.
                </p>
              </div>
              <div className="flex gap-3">
                <Button onClick={() => setMode('ai')} variant="secondary">
                  <Wand2 className="mr-2 h-4 w-4" />
                  AI Generate
                </Button>
                <Button onClick={() => setMode('create')}>
                  <Plus className="mr-2 h-4 w-4" />
                  Create Manual
                </Button>
              </div>
            </div>

            {/* Existing Exercises */}
            <Card className="border-slate-800 bg-slate-900/50">
              <CardHeader>
                <CardTitle className="text-white">Existing Exercises</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {existingExercises.map((exercise) => (
                    <div
                      key={exercise.id}
                      className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-900/50 p-4"
                    >
                      <div className="flex-1">
                        <p className="font-medium text-white">{exercise.title}</p>
                        <p className="text-sm text-slate-400">{exercise.topic}</p>
                      </div>
                      <Badge
                        variant={
                          exercise.difficulty === 'beginner'
                            ? 'success'
                            : exercise.difficulty === 'intermediate'
                              ? 'warning'
                              : 'error'
                        }
                        size="sm"
                      >
                        {exercise.difficulty}
                      </Badge>
                      <div className="ml-4 flex gap-2">
                        <Button size="sm" variant="ghost">
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="ghost">
                          <Trash2 className="h-4 w-4 text-error-400" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </>
        )}

        {/* AI Generate View */}
        {mode === 'ai' && (
          <>
            <div className="mb-8 flex items-center gap-4">
              <Button variant="ghost" size="sm" onClick={() => setMode('list')}>
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back
              </Button>
              <div>
                <h1 className="text-3xl font-bold text-white">AI Exercise Generator</h1>
                <p className="mt-2 text-slate-400">
                  Describe the exercise you want and AI will generate it for you.
                </p>
              </div>
            </div>

            <Card className="border-slate-800 bg-slate-900/50">
              <CardContent className="p-6">
                <div className="space-y-4">
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                      What should the exercise be about?
                    </label>
                    <Textarea
                      value={aiPrompt}
                      onChange={(e) => setAiPrompt(e.target.value)}
                      placeholder="e.g., Create an exercise about list comprehensions in Python that filters even numbers..."
                      rows={4}
                      className="bg-slate-800"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="mb-2 block text-sm font-medium text-slate-300">
                        Difficulty
                      </label>
                      <select
                        value={formData.difficulty}
                        onChange={(e) => setFormData({ ...formData, difficulty: e.target.value as any })}
                        className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-white"
                      >
                        {difficulties.map((d) => (
                          <option key={d} value={d} className="capitalize">
                            {d}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="mb-2 block text-sm font-medium text-slate-300">
                        Topic
                      </label>
                      <select
                        value={formData.topicId}
                        onChange={(e) => setFormData({ ...formData, topicId: Number(e.target.value) })}
                        className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-white"
                      >
                        {mockModules.flatMap((m) =>
                          m.topics.map((t) => (
                            <option key={t.id} value={t.id}>
                              {m.title}: {t.title}
                            </option>
                          ))
                        )}
                      </select>
                    </div>
                  </div>

                  <Button
                    onClick={handleGenerateAI}
                    isLoading={isGenerating}
                    disabled={!aiPrompt.trim()}
                    className="w-full"
                  >
                    <Wand2 className="mr-2 h-4 w-4" />
                    Generate Exercise
                  </Button>
                </div>
              </CardContent>
            </Card>

            {isGenerating && (
              <Card className="mt-6 border-slate-800 bg-slate-900/50">
                <CardContent className="p-6">
                  <div className="flex items-center gap-3">
                    <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary-500 border-t-transparent" />
                    <p className="text-slate-300">Generating exercise...</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </>
        )}

        {/* Create/Edit View */}
        {mode === 'create' && (
          <>
            <div className="mb-8 flex items-center gap-4">
              <Button variant="ghost" size="sm" onClick={() => setMode('list')}>
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back
              </Button>
              <div>
                <h1 className="text-3xl font-bold text-white">
                  {generatedExercise ? 'Review Generated Exercise' : 'Create Exercise'}
                </h1>
                <p className="mt-2 text-slate-400">
                  {generatedExercise
                    ? 'Review and edit the AI-generated exercise before saving.'
                    : 'Create a custom exercise for your students.'}
                </p>
              </div>
            </div>

            <Card className="border-slate-800 bg-slate-900/50">
              <CardContent className="p-6 space-y-6">
                {/* Title */}
                <Input
                  label="Exercise Title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="e.g., Calculate List Sum"
                  className="bg-slate-800"
                />

                {/* Description */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Description
                  </label>
                  <Textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Describe what the student needs to do..."
                    rows={3}
                    className="bg-slate-800"
                  />
                </div>

                {/* Topic & Difficulty */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                      Topic
                    </label>
                    <select
                      value={formData.topicId}
                      onChange={(e) => setFormData({ ...formData, topicId: Number(e.target.value) })}
                      className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-white"
                    >
                      {mockModules.flatMap((m) =>
                        m.topics.map((t) => (
                          <option key={t.id} value={t.id}>
                            {m.title}: {t.title}
                          </option>
                        ))
                      )}
                    </select>
                  </div>
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                      Difficulty
                    </label>
                    <select
                      value={formData.difficulty}
                      onChange={(e) => setFormData({ ...formData, difficulty: e.target.value as any })}
                      className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-white"
                    >
                      {difficulties.map((d) => (
                        <option key={d} value={d} className="capitalize">
                          {d}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Starter Code */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Starter Code
                  </label>
                  <Textarea
                    value={formData.starterCode}
                    onChange={(e) => setFormData({ ...formData, starterCode: e.target.value })}
                    placeholder="# Starter code for students..."
                    rows={6}
                    className="bg-slate-800 font-mono text-sm"
                  />
                </div>

                {/* Solution Code */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Solution Code (for reference)
                  </label>
                  <Textarea
                    value={formData.solutionCode}
                    onChange={(e) => setFormData({ ...formData, solutionCode: e.target.value })}
                    placeholder="# Solution code..."
                    rows={6}
                    className="bg-slate-800 font-mono text-sm"
                  />
                </div>

                {/* Hints */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Hints (students can reveal these if stuck)
                  </label>
                  <div className="space-y-2">
                    <Input
                      value={formData.hints[0]}
                      onChange={(e) => {
                        const newHints = [...formData.hints]
                        newHints[0] = e.target.value
                        setFormData({ ...formData, hints: newHints })
                      }}
                      placeholder="First hint..."
                      className="bg-slate-800"
                    />
                    <Input
                      value={formData.hints[1]}
                      onChange={(e) => {
                        const newHints = [...formData.hints]
                        newHints[1] = e.target.value
                        setFormData({ ...formData, hints: newHints })
                      }}
                      placeholder="Second hint..."
                      className="bg-slate-800"
                    />
                  </div>
                </div>

                {/* Test Cases */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Test Cases
                  </label>
                  <div className="space-y-2 rounded-lg border border-slate-800 bg-slate-900/50 p-4">
                    <div className="flex items-center gap-2 text-sm text-slate-400">
                      <span className="font-mono">calculate_sum([1, 2, 3])</span>
                      <span>→</span>
                      <span className="text-white">6</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-slate-400">
                      <span className="font-mono">calculate_sum([10, 20, 30])</span>
                      <span>→</span>
                      <span className="text-white">60</span>
                    </div>
                    <Button size="sm" variant="ghost" className="mt-2">
                      <Plus className="mr-2 h-3 w-3" />
                      Add Test Case
                    </Button>
                  </div>
                </div>

                {/* Preview */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Preview
                  </label>
                  <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
                    <p className="font-medium text-white">{formData.title || 'Exercise Title'}</p>
                    <p className="mt-2 text-sm text-slate-400">{formData.description || 'Exercise description'}</p>
                    <Badge
                      variant={
                        formData.difficulty === 'beginner'
                          ? 'success'
                          : formData.difficulty === 'intermediate'
                            ? 'warning'
                            : 'error'
                      }
                      size="sm"
                      className="mt-2"
                    >
                      {formData.difficulty}
                    </Badge>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-3">
                  <Button onClick={handleSave} className="flex-1">
                    <Save className="mr-2 h-4 w-4" />
                    Save Exercise
                  </Button>
                  <Button variant="ghost" onClick={() => setMode('list')}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </main>
    </div>
  )
}
