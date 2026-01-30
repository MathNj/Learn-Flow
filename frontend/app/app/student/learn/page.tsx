'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import TutorChat from '@/components/shared/tutor-chat'
import CodeEditor from '@/components/shared/monaco-editor'
import CodeRunner from '@/components/shared/code-runner'
import MasteryRing from '@/components/shared/mastery-ring'
import { Avatar } from '@/components/ui/avatar'
import { mockModules, mockExercises, mockStudentProgress } from '@/lib/mock-data'
import { useAuthStore } from '@/lib/stores/auth-store'
import { Code2, Play, ArrowLeft, BookOpen } from 'lucide-react'

export default function LearnPage() {
  const { user } = useAuthStore()
  const [selectedModule, setSelectedModule] = useState(mockModules[0])
  const [selectedTopic, setSelectedTopic] = useState(mockModules[0].topics[0])
  const [code, setCode] = useState('# Write your code here\n\n')
  const [runResult, setRunResult] = useState<any>(null)
  const [isRunning, setIsRunning] = useState(false)

  const handleRunCode = async () => {
    setIsRunning(true)
    setRunResult(null)

    // Simulate code execution
    setTimeout(() => {
      setRunResult({
        success: true,
        output: 'Hello, World!\n0\n1\n2\n3\n4',
        executionTime: 0.15,
        timeoutOccurred: false,
      })
      setIsRunning(false)
    }, 1500)
  }

  const handleClearOutput = () => {
    setRunResult(null)
  }

  const currentProgress = mockStudentProgress.modules.find(
    (m) => m.moduleId === selectedModule.id
  )

  return (
    <div className="flex h-screen flex-col bg-slate-950">
      {/* Header */}
      <header className="flex shrink-0 items-center justify-between border-b border-slate-800 bg-slate-900/50 px-4 py-3">
        <div className="flex items-center gap-4">
          <Link href="/app/student/dashboard">
            <Button size="sm" variant="ghost" className="h-8">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Dashboard
            </Button>
          </Link>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500 to-primary-700">
              <Code2 className="h-4 w-4 text-white" />
            </div>
            <span className="font-semibold text-white">LearnFlow</span>
          </div>
          <div className="ml-4 flex items-center gap-2">
            <span className="rounded-full bg-primary-500/10 px-2.5 py-1 text-xs font-medium text-primary-400">
              {selectedModule.title}
            </span>
            <span className="text-slate-500">›</span>
            <span className="text-sm text-slate-300">{selectedTopic.title}</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {currentProgress && (
            <div className="flex items-center gap-2">
              <span className="text-sm text-slate-400">Mastery:</span>
              <MasteryRing mastery={currentProgress.mastery} level={currentProgress.level} size="sm" showLabel={false} />
              <span className="text-sm font-medium text-white">{currentProgress.mastery}%</span>
            </div>
          )}
          <Avatar name={user?.username || 'Student'} size="sm" />
        </div>
      </header>

      {/* Main Content - Split View */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel - Tutor Chat */}
        <div className="w-96 shrink-0 border-r border-slate-800">
          <TutorChat
            studentId={user?.id || 'student-1'}
            topicId={selectedTopic.id}
          />
        </div>

        {/* Right Panel - Code Editor & Runner */}
        <div className="flex flex-1 flex-col overflow-hidden">
          {/* Toolbar */}
          <div className="flex shrink-0 items-center justify-between border-b border-slate-800 bg-slate-900/30 px-4 py-2">
            <div className="flex items-center gap-4">
              <h2 className="font-semibold text-white">Code Editor</h2>
              <div className="flex items-center gap-2 text-sm text-slate-400">
                <BookOpen className="h-4 w-4" />
                <span>{selectedTopic.title}</span>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button
                size="sm"
                onClick={handleRunCode}
                isLoading={isRunning}
                className="h-8"
              >
                <Play className="mr-2 h-4 w-4" />
                Run
              </Button>
            </div>
          </div>

          {/* Editor and Output */}
          <div className="flex flex-1 flex-col overflow-hidden p-4">
            <div className="mb-4 flex-1">
              <CodeEditor
                code={code}
                onChange={setCode}
                onRun={handleRunCode}
                isLoading={isRunning}
                height="100%"
              />
            </div>

            {/* Output */}
            <div className="h-48 shrink-0">
              <CodeRunner
                result={runResult}
                isRunning={isRunning}
                onClear={handleClearOutput}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
