'use client'

import { useEffect, useRef, useCallback, useState } from 'react'

// ============================================================================
// Types
// ============================================================================

// Backend message format from WebSocket service
export type BackendWebSocketMessage = {
  message_id: string
  student_id: string
  timestamp: string
  type: 'ai_response' | 'chat' | 'progress' | 'alert' | 'presence'
  agent?: string
  content: string
}

// Frontend chat message format
export type ChatMessage = {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  agentType?: 'triage' | 'concepts' | 'code-review' | 'debug' | 'exercise' | 'progress'
}

// Message to send to backend
export type ChatSendMessage = {
  content: string
  student_id: string
  context?: {
    topic_id?: number
    exercise_id?: string
    mastery_level?: number
  }
}

export type WebSocketHookReturn = {
  sendMessage: (message: ChatSendMessage) => void
  lastMessage: BackendWebSocketMessage | null
  readyState: 'connecting' | 'open' | 'closed' | 'error'
  isConnected: boolean
}

// ============================================================================
// Configuration
// ============================================================================

// WebSocket service URL (port 8008 for WebSocket service, or 8080 for API Gateway)
// The backend WebSocket endpoint is: /ws/chat/{student_id}
const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8008'
const WS_PATH = '/ws/chat'

// Enable demo mode if backend is unavailable
const DEMO_MODE = process.env.NEXT_PUBLIC_DEMO_MODE === 'true' || false

// ============================================================================
// WebSocket Hook for Real Backend Integration
// ============================================================================

export function useChatWebSocket(
  studentId: string,
  onMessage?: (message: ChatMessage) => void
): WebSocketHookReturn {
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const reconnectAttemptsRef = useRef(0)
  const [lastMessage, setLastMessage] = useState<BackendWebSocketMessage | null>(null)
  const [readyState, setReadyState] = useState<'connecting' | 'open' | 'closed' | 'error'>('connecting')

  // Convert backend message to frontend format
  const convertBackendMessage = (backendMsg: BackendWebSocketMessage): ChatMessage => {
    // Map agent names to agentType
    const agentMap: Record<string, ChatMessage['agentType']> = {
      'triage-agent': 'triage',
      'concepts-agent': 'concepts',
      'code-review-agent': 'code-review',
      'debug-agent': 'debug',
      'exercise-agent': 'exercise',
      'progress-agent': 'progress',
    }

    return {
      id: backendMsg.message_id,
      role: 'assistant',
      content: backendMsg.content,
      timestamp: backendMsg.timestamp,
      agentType: backendMsg.agent ? agentMap[backendMsg.agent] || 'triage' : undefined,
    }
  }

  const connect = useCallback(() => {
    if (!studentId) {
      setReadyState('closed')
      return
    }

    setReadyState('connecting')

    try {
      // Connect to backend WebSocket service: ws://localhost:8008/ws/chat/{student_id}
      const wsUrl = `${WS_BASE_URL}${WS_PATH}/${studentId}`
      console.log('[WebSocket] Connecting to:', wsUrl)

      const ws = new WebSocket(wsUrl)
      wsRef.current = ws

      ws.onopen = () => {
        console.log('[WebSocket] Connected')
        setReadyState('open')
        reconnectAttemptsRef.current = 0 // Reset reconnect counter on successful connection
      }

      ws.onmessage = (event) => {
        try {
          const backendMessage: BackendWebSocketMessage = JSON.parse(event.data)
          console.log('[WebSocket] Received:', backendMessage)

          setLastMessage(backendMessage)

          // Convert and notify callback
          if (onMessage && backendMessage.type === 'ai_response') {
            const chatMessage = convertBackendMessage(backendMessage)
            onMessage(chatMessage)
          }
        } catch (err) {
          console.error('[WebSocket] Error parsing message:', err)
        }
      }

      ws.onerror = (event) => {
        console.error('[WebSocket] Error:', event)
        setReadyState('error')
      }

      ws.onclose = (event) => {
        console.log('[WebSocket] Closed:', event.code, event.reason)
        setReadyState('closed')

        // Exponential backoff reconnection (max 30 seconds)
        const maxReconnectDelay = 30000
        const reconnectDelay = Math.min(
          1000 * Math.pow(2, reconnectAttemptsRef.current),
          maxReconnectDelay
        )

        reconnectAttemptsRef.current++

        console.log(`[WebSocket] Reconnecting in ${reconnectDelay}ms (attempt ${reconnectAttemptsRef.current})`)

        reconnectTimeoutRef.current = setTimeout(() => {
          connect()
        }, reconnectDelay)
      }
    } catch (err) {
      console.error('[WebSocket] Connection error:', err)
      setReadyState('error')
    }
  }, [studentId, onMessage])

  const sendMessage = useCallback((message: ChatSendMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const payload = JSON.stringify(message)
      console.log('[WebSocket] Sending:', message)
      wsRef.current.send(payload)
    } else {
      console.warn('[WebSocket] Cannot send message, not connected:', readyState)
    }
  }, [readyState])

  useEffect(() => {
    // Skip connection in demo mode
    if (DEMO_MODE) {
      console.log('[WebSocket] Demo mode enabled, skipping connection')
      setReadyState('closed')
      return
    }

    connect()

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [connect])

  return {
    sendMessage,
    lastMessage,
    readyState,
    isConnected: readyState === 'open',
  }
}

// ============================================================================
// Demo fallback hook for when WebSocket backend is unavailable
// ============================================================================

export function useDemoChatWebSocket(
  onMessage?: (message: ChatMessage) => void
): WebSocketHookReturn {
  const [lastMessage, setLastMessage] = useState<BackendWebSocketMessage | null>(null)
  const [readyState, setReadyState] = useState<'connecting' | 'open' | 'closed' | 'error'>('open')

  const sendMessage = useCallback((message: ChatSendMessage) => {
    // Simulate AI response with keyword-based routing (matches backend logic)
    setTimeout(() => {
      const content = message.content.toLowerCase()
      let agent: BackendWebSocketMessage['agent'] = 'triage-agent'
      let response = "I'm here to help! Could you tell me more about what you're working on?"

      // Match the same routing logic as the backend WebSocket service
      if (content.includes('error') || content.includes('exception') || content.includes('bug') || content.includes('not working')) {
        agent = 'debug-agent'
        response = "I see you're having an error. Can you share the error message you're seeing? I'll help you work through it step by step."
      } else if (content.includes('explain') || content.includes('what is') || content.includes('how does') || content.includes('concept')) {
        agent = 'concepts-agent'
        response = "Great question! Let me explain this concept in a way that builds on what you already know. Would you like a code example to help illustrate?"
      } else if (content.includes('exercise') || content.includes('practice') || content.includes('quiz') || content.includes('challenge')) {
        agent = 'exercise-agent'
        response = "Let's practice! I'll find an exercise that matches your current level. Ready to give it a try?"
      } else if (content.includes('review') || content.includes('improve') || content.includes('better')) {
        agent = 'code-review-agent'
        response = "I'd be happy to review your code! Share it with me and I'll provide feedback on PEP 8 style, efficiency, and readability."
      } else if (content.includes('progress') || content.includes('score') || content.includes('mastery') || content.includes('how am i doing')) {
        agent = 'progress-agent'
        response = "Let me check your progress! You're making good progress. Keep practicing consistently and you'll see continued improvement!"
      }

      const aiMessage: BackendWebSocketMessage = {
        message_id: `demo-${Date.now()}`,
        student_id: message.student_id,
        timestamp: new Date().toISOString(),
        type: 'ai_response',
        agent,
        content: response,
      }

      setLastMessage(aiMessage)

      if (onMessage) {
        const chatMessage: ChatMessage = {
          id: aiMessage.message_id,
          role: 'assistant',
          content: aiMessage.content,
          timestamp: aiMessage.timestamp,
          agentType: agent.replace('-agent', '') as ChatMessage['agentType'],
        }
        onMessage(chatMessage)
      }
    }, 1000)
  }, [onMessage])

  return {
    sendMessage,
    lastMessage,
    readyState,
    isConnected: readyState === 'open',
  }
}

// ============================================================================
// Unified hook that auto-selects demo or real WebSocket
// ============================================================================

export function useWebSocket(
  studentId: string,
  onMessage?: (message: ChatMessage) => void
): WebSocketHookReturn {
  // Use demo mode if explicitly enabled or if no studentId
  if (DEMO_MODE || !studentId) {
    return useDemoChatWebSocket(onMessage)
  }

  return useChatWebSocket(studentId, onMessage)
}
