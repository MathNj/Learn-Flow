'use client'

import { useEffect, useRef, useCallback, useState } from 'react'
import { useAuthStore } from '@/lib/stores/auth-store'

export type WebSocketMessage = {
  type: 'chat' | 'progress' | 'alert' | 'presence'
  data: any
}

export type WebSocketHookReturn = {
  sendMessage: (message: WebSocketMessage) => void
  lastMessage: WebSocketMessage | null
  readyState: 'connecting' | 'open' | 'closed' | 'error'
}

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8080/ws'

export function useWebSocket(
  onMessage?: (message: WebSocketMessage) => void
): WebSocketHookReturn {
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null)
  const [readyState, setReadyState] = useState<'connecting' | 'open' | 'closed' | 'error'>('connecting')
  const { token } = useAuthStore()

  const connect = useCallback(() => {
    if (!token) {
      setReadyState('closed')
      return
    }

    setReadyState('connecting')

    try {
      const ws = new WebSocket(`${WS_URL}?token=${token}`)
      wsRef.current = ws

      ws.onopen = () => {
        setReadyState('open')
      }

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          setLastMessage(message)
          onMessage?.(message)
        } catch (err) {
          // Non-JSON message (keepalive, etc.)
        }
      }

      ws.onerror = () => {
        setReadyState('error')
      }

      ws.onclose = () => {
        setReadyState('closed')
        // Attempt reconnection after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          connect()
        }, 3000)
      }
    } catch (err) {
      setReadyState('error')
    }
  }, [token, onMessage])

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message))
    }
  }, [])

  useEffect(() => {
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

  return { sendMessage, lastMessage, readyState }
}

// Demo fallback hook for when WebSocket is unavailable
export function useChatWebSocket(studentId: string, onMessage: (message: any) => void) {
  const [isConnected, setIsConnected] = useState(false)

  // For demo purposes, we'll simulate a connection
  // In production, this would use the real WebSocket hook above
  useEffect(() => {
    setIsConnected(true)
  }, [studentId])

  const sendMessage = useCallback((message: any) => {
    // Simulate sending a message
    // In production, this would send via WebSocket
  }, [])

  // Simulate receiving messages for demo
  useEffect(() => {
    if (!isConnected) return

    const handler = (event: MessageEvent) => {
      // Check if this is a chat message from another tab (for demo coordination)
      if (event.origin === window.location.origin && event.data.type === 'chat') {
        onMessage(event.data)
      }
    }

    window.addEventListener('message', handler)
    return () => window.removeEventListener('message', handler)
  }, [isConnected, onMessage])

  return { sendMessage, isConnected }
}
