'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import MasteryRing from '@/components/shared/mastery-ring'
import { Progress } from '@/components/ui/progress'
import ExerciseCard from '@/components/student/exercise-card'
import { Avatar } from '@/components/ui/avatar'
import { mockModules, mockExercises, mockStudentProgress, mockQuiz } from '@/lib/mock-data'
import { useAuthStore } from '@/lib/stores/auth-store'
import {
  Code2,
  ArrowLeft,
  BookOpen,
  Play,
  FileText,
  CheckCircle2,
  Lock,
  Clock,
  Target,
} from 'lucide-react'

export default function ModuleDetailPage() {
  const { user } = useAuthStore()
  const params = useParams()
  const moduleId = Number(params.moduleId)

  const module = mockModules.find((m) => m.id === moduleId)
  const moduleProgress = mockStudentProgress.modules.find((m) => m.moduleId === moduleId)

  const [activeTab, setActiveTab] = useState<'topics' | 'exercises' | 'quiz'>('topics')
  const [selectedExercise, setSelectedExercise] = useState<typeof mockExercises[0] | null>(null)
  const [selectedTopic, setSelectedTopic] = useState<number | null>(null)

  if (!module) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950">
        <p className="text-slate-400">Module not found</p>
      </div>
    )
  }

  const moduleExercises = mockExercises.filter((e) =>
    module.topics.some((t) => t.id === e.topicId)
  )

  const topicQuiz = mockQuiz

  const handleExerciseComplete = (success: boolean) => {
    if (success) {
      setSelectedExercise(null)
    }
  }

  if (selectedExercise) {
    return (
      <div className="min-h-screen bg-slate-950 p-4">
        <div className="mx-auto max-w-4xl">
          <ExerciseCard
            exercise={selectedExercise}
            onBack={() => setSelectedExercise(null)}
            onComplete={handleExerciseComplete}
            className="h-full"
          />
        </div>
      </div>
    )
  }

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
            <Link href="/app/student/dashboard" className="text-sm text-slate-400 hover:text-white transition-colors">
              Dashboard
            </Link>
            <Link href="/app/student/learn" className="text-sm text-slate-400 hover:text-white transition-colors">
              Learn
            </Link>
            <Link href="/app/student/profile" className="text-sm text-slate-400 hover:text-white transition-colors">
              Profile
            </Link>
          </nav>

          <Avatar name={user?.username || 'Student'} size="md" />
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Back Button */}
        <Link href="/app/student/dashboard">
          <Button variant="ghost" size="sm" className="mb-6">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Dashboard
          </Button>
        </Link>

        {/* Module Header */}
        <Card className="mb-8 border-slate-800 bg-slate-900/50">
          <CardContent className="p-6">
            <div className="flex items-start gap-6">
              <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary-500 to-primary-700">
                <BookOpen className="h-10 w-10 text-white" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-3">
                  <h1 className="text-3xl font-bold text-white">{module.title}</h1>
                  <Badge variant="primary" size="sm">
                    Module {module.order}
                  </Badge>
                </div>
                <p className="mt-2 text-slate-400">{module.description}</p>
                <div className="mt-4 flex items-center gap-6 text-sm text-slate-400">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    <span>{module.estimatedHours} hours</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Target className="h-4 w-4" />
                    <span>{module.topics.length} topics</span>
                  </div>
                </div>
              </div>

              {/* Mastery */}
              {moduleProgress && (
                <div className="text-center">
                  <MasteryRing
                    mastery={moduleProgress.mastery}
                    level={moduleProgress.level}
                    size="xl"
                    showLabel
                  />
                </div>
              )}
            </div>

            {/* Progress Bar */}
            {moduleProgress && (
              <div className="mt-6">
                <div className="mb-2 flex items-center justify-between text-sm">
                  <span className="text-slate-400">Progress</span>
                  <span className="text-white font-medium">
                    {moduleProgress.topicsCompleted}/{moduleProgress.topicsTotal} topics
                  </span>
                </div>
                <Progress value={moduleProgress.mastery} />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Tabs */}
        <div className="mb-6 border-b border-slate-800">
          <div className="flex gap-6">
            <button
              onClick={() => setActiveTab('topics')}
              className={`pb-3 text-sm font-medium transition-colors ${
                activeTab === 'topics'
                  ? 'border-b-2 border-primary-500 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Topics
            </button>
            <button
              onClick={() => setActiveTab('exercises')}
              className={`pb-3 text-sm font-medium transition-colors ${
                activeTab === 'exercises'
                  ? 'border-b-2 border-primary-500 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Exercises
            </button>
            <button
              onClick={() => setActiveTab('quiz')}
              className={`pb-3 text-sm font-medium transition-colors ${
                activeTab === 'quiz'
                  ? 'border-b-2 border-primary-500 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Quiz
            </button>
          </div>
        </div>

        {/* Topics Tab */}
        {activeTab === 'topics' && (
          <div className="space-y-4">
            {module.topics.map((topic, index) => {
              const isLocked = index > 0 && moduleProgress && moduleProgress.topicsCompleted < index
              const isCompleted = moduleProgress && moduleProgress.topicsCompleted > index

              return (
                <Card
                  key={topic.id}
                  className={`border-slate-800 bg-slate-900/50 transition-all ${
                    !isLocked && 'hover:border-slate-700 cursor-pointer'
                  }`}
                  onClick={() =>
                    !isLocked && setSelectedTopic(topic.id)
                  }
                >
                  <CardContent className="p-4">
                    <div className="flex items-center gap-4">
                      <div
                        className={`flex h-10 w-10 items-center justify-center rounded-full ${
                          isCompleted
                            ? 'bg-success-500/10 text-success-500'
                            : isLocked
                              ? 'bg-slate-800 text-slate-600'
                              : 'bg-primary-500/10 text-primary-400'
                        }`}
                      >
                        {isCompleted ? (
                          <CheckCircle2 className="h-5 w-5" />
                        ) : isLocked ? (
                          <Lock className="h-5 w-5" />
                        ) : (
                          <Play className="h-5 w-5" />
                        )}
                      </div>

                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-medium text-white">{topic.title}</h3>
                          <Badge
                            variant={
                              topic.difficulty === 'beginner'
                                ? 'success'
                                : topic.difficulty === 'intermediate'
                                  ? 'warning'
                                  : 'error'
                            }
                            size="sm"
                          >
                            {topic.difficulty}
                          </Badge>
                        </div>
                        <p className="mt-1 text-sm text-slate-400">{topic.description}</p>
                      </div>

                      <div className="flex items-center gap-3">
                        <span className="text-sm text-slate-500">Topic {index + 1}</span>
                        {!isLocked && (
                          <Button size="sm" variant="ghost">
                            {isCompleted ? 'Review' : 'Start'}
                          </Button>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        )}

        {/* Exercises Tab */}
        {activeTab === 'exercises' && (
          <div className="space-y-4">
            {moduleExercises.length > 0 ? (
              moduleExercises.map((exercise) => (
                <Card
                  key={exercise.id}
                  className="border-slate-800 bg-slate-900/50 hover:border-slate-700 transition-all cursor-pointer"
                  onClick={() => setSelectedExercise(exercise)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center gap-4">
                      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-500/10">
                        <Target className="h-6 w-6 text-primary-400" />
                      </div>

                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-medium text-white">{exercise.title}</h3>
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
                        </div>
                        <p className="mt-1 text-sm text-slate-400">{exercise.description}</p>
                        <div className="mt-2 flex items-center gap-4 text-xs text-slate-500">
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {exercise.estimatedMinutes} min
                          </div>
                          <div className="flex items-center gap-1">
                            <FileText className="h-3 w-3" />
                            {exercise.testCases.length} test cases
                          </div>
                        </div>
                      </div>

                      <Button size="sm">Start</Button>
                    </div>
                  </CardContent>
                </Card>
              ))
            ) : (
              <Card className="border-slate-800 bg-slate-900/50">
                <CardContent className="p-8 text-center">
                  <p className="text-slate-400">No exercises available for this module yet.</p>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Quiz Tab */}
        {activeTab === 'quiz' && (
          <Card className="border-slate-800 bg-slate-900/50">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-white">{topicQuiz.title}</CardTitle>
                <Badge variant="primary" size="sm">
                  {topicQuiz.questions.length} questions
                </Badge>
              </div>
              <p className="text-slate-400">
                Test your knowledge of {module.title} concepts.
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {topicQuiz.questions.map((q, index) => (
                  <div
                    key={q.id}
                    className="rounded-lg border border-slate-800 bg-slate-900/50 p-4"
                  >
                    <p className="text-sm text-white">
                      <span className="font-medium text-primary-400">Q{index + 1}.</span> {q.question}
                    </p>
                    <div className="mt-2 grid grid-cols-2 gap-2">
                      {q.options?.slice(0, 2).map((option, i) => (
                        <div
                          key={i}
                          className="rounded border border-slate-700 px-3 py-2 text-sm text-slate-400"
                        >
                          {option}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
              <Button className="mt-6 w-full">Start Quiz</Button>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  )
}
