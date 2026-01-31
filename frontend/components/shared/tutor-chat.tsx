'use client'

import React, { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { Avatar } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Send, Code, CheckCircle2, Lightbulb, WifiOff, Loader2 } from 'lucide-react'
import { cn, formatRelativeTime } from '@/lib/utils'
import type { ChatMessage } from '@/lib/types'
import { mockChatMessages } from '@/lib/mock-data'
import { useWebSocket } from '@/lib/hooks/use-websocket'

export interface TutorChatProps {
  studentId: string
  topicId?: number
  exerciseId?: string
  onCodeRequest?: () => void
  onQuizRequest?: () => void
  className?: string
}

const TutorChat: React.FC<TutorChatProps> = ({
  studentId,
  topicId,
  exerciseId,
  onCodeRequest,
  onQuizRequest,
  className,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>(mockChatMessages)
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // WebSocket connection for real-time AI chat
  const { sendMessage, isConnected, readyState } = useWebSocket(
    studentId,
    (message: ChatMessage) => {
      // Add AI response to messages
      setMessages((prev) => [...prev, message])
      setIsLoading(false)
    }
  )

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])
    const messageContent = input
    setInput('')
    setIsLoading(true)

    // Send message via WebSocket to backend
    sendMessage({
      content: messageContent,
      student_id: studentId,
      context: {
        topic_id: topicId,
        exercise_id: exerciseId,
      },
    })
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const getAgentIcon = (agentType?: string) => {
    switch (agentType) {
      case 'concepts':
        return <Lightbulb className="h-4 w-4" />
      case 'code-review':
        return <CheckCircle2 className="h-4 w-4" />
      case 'debug':
        return <Code className="h-4 w-4" />
      case 'exercise':
        return <Code className="h-4 w-4" />
      case 'progress':
        return <CheckCircle2 className="h-4 w-4" />
      default:
        return <div className="h-4 w-4 rounded-full bg-primary-500" />
    }
  }

  const getConnectionStatus = () => {
    switch (readyState) {
      case 'connecting':
        return (
          <Badge variant="outline" className="gap-1.5 text-xs">
            <Loader2 className="h-3 w-3 animate-spin" />
            Connecting...
          </Badge>
        )
      case 'open':
        return (
          <Badge variant="outline" className="gap-1.5 border-success-500/30 bg-success-500/10 text-success-600 dark:text-success-400">
            <div className="h-2 w-2 rounded-full bg-success-500" />
            Connected
          </Badge>
        )
      case 'error':
      case 'closed':
        return (
          <Badge variant="outline" className="gap-1.5 border-warning-500/30 bg-warning-500/10 text-warning-600 dark:text-warning-400">
            <WifiOff className="h-3 w-3" />
            Demo Mode
          </Badge>
        )
    }
  }

  return (
    <Card className={cn('flex flex-col', className)}>
      <CardContent className="flex flex-col h-full p-0">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-200 p-4 dark:border-slate-700">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900/30">
              <Lightbulb className="h-4 w-4 text-primary-600 dark:text-primary-400" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900 dark:text-slate-100">AI Tutor</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Always here to help</p>
            </div>
          </div>
          {getConnectionStatus()}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                'flex gap-3',
                message.role === 'user' ? 'justify-end' : 'justify-start'
              )}
            >
              {message.role === 'assistant' && (
                <Avatar
                  name="AI Tutor"
                  size="sm"
                  className="mt-1 shrink-0"
                />
              )}
              <div
                className={cn(
                  'max-w-[80%] rounded-lg px-4 py-2.5',
                  message.role === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100'
                )}
              >
                {message.agentType && message.role === 'assistant' && (
                  <div className="mb-1 flex items-center gap-1.5 text-xs text-primary-600 dark:text-primary-400">
                    {getAgentIcon(message.agentType)}
                    <span className="font-medium capitalize">{message.agentType} Agent</span>
                  </div>
                )}
                <div className="whitespace-pre-wrap text-sm leading-relaxed">
                  {message.content}
                </div>
                <div
                  className={cn(
                    'mt-1 text-xs opacity-70',
                    message.role === 'user' ? 'text-primary-100' : 'text-slate-500'
                  )}
                >
                  {formatRelativeTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex gap-3 justify-start">
              <Avatar name="AI Tutor" size="sm" className="mt-1 shrink-0" />
              <div className="rounded-lg bg-slate-100 px-4 py-2.5 dark:bg-slate-800">
                <div className="flex gap-1">
                  <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]" />
                  <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]" />
                  <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400" />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        <div className="border-t border-slate-200 p-3 dark:border-slate-700">
          <div className="mb-2 flex flex-wrap gap-2">
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setInput('Explain this concept with examples')}
              className="h-7 text-xs"
            >
              Explain with examples
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setInput('Give me a practice exercise')}
              className="h-7 text-xs"
            >
              Practice exercise
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setInput("I'm stuck, can you help?")}
              className="h-7 text-xs"
            >
              I'm stuck
            </Button>
          </div>

          {/* Input */}
          <div className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask me anything about Python..."
              className="flex-1"
            />
            <Button
              onClick={handleSend}
              isLoading={isLoading}
              disabled={!input.trim()}
              size="sm"
              className="h-10 px-3"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default TutorChat
