'use client'

import { useState, useEffect } from 'react'
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useAuthStore } from '@/lib/stores/auth-store'
import api from '@/lib/api'

// Create a client instance
let browserQueryClient: QueryClient | undefined

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        gcTime: 5 * 60 * 1000, // 5 minutes
        retry: 1,
        refetchOnWindowFocus: false,
      },
      mutations: {
        retry: 1,
      },
    },
  })
}

function getQueryClient() {
  if (typeof window === 'undefined') {
    // Server: always create a new client
    return makeQueryClient()
  }
  // Browser: create once and reuse
  if (!browserQueryClient) {
    browserQueryClient = makeQueryClient()
  }
  return browserQueryClient
}

export function QueryProvider({ children }: { children: React.ReactNode }) {
  // NOTE: Avoid useState when initializing the query client if you don't
  // have a suspense boundary between this and the children that
  // will render because this will cause the client to be recreated
  // on every render.
  const queryClient = getQueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools
          initialIsOpen={false}
          position="bottom-right"
        />
      )}
    </QueryClientProvider>
  )
}

// Custom hooks for common queries
export function useModules() {
  return useQuery({
    queryKey: ['modules'],
    queryFn: () => api.getModules(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useModule(moduleId: number) {
  return useQuery({
    queryKey: ['module', moduleId],
    queryFn: () => api.getModule(moduleId),
    enabled: !!moduleId,
  })
}

export function useProgress(studentId: string) {
  return useQuery({
    queryKey: ['progress', studentId],
    queryFn: () => api.getProgress(studentId),
    enabled: !!studentId,
    refetchInterval: 30 * 1000, // Refetch every 30 seconds
  })
}

export function useExercises(filters?: { topicId?: number; difficulty?: string }) {
  return useQuery({
    queryKey: ['exercises', filters],
    queryFn: () => api.getExercises(filters),
  })
}

export function useAlerts(filters?: {
  severity?: string
  classId?: string
  acknowledged?: boolean
}) {
  return useQuery({
    queryKey: ['alerts', filters],
    queryFn: () => api.getAlerts(filters),
    refetchInterval: 15 * 1000, // Refetch every 15 seconds for real-time alerts
  })
}

export function useStudents(filters?: {
  classId?: string
  search?: string
  sortBy?: string
}) {
  return useQuery({
    queryKey: ['students', filters],
    queryFn: () => api.getStudents(filters),
  })
}

// Optimistic updates hook
export function useOptimisticMutation<T>(
  mutationFn: (variables: T) => Promise<any>,
  queryKey: any[]
) {
  const queryClient = getQueryClient()

  return {
    mutate: async (variables: T) => {
      // Cancel any outgoing refetches
      await queryClient.cancelQueries({ queryKey })

      // Snapshot the previous value
      const previousData = queryClient.getQueryData(queryKey)

      // Optimistically update to the new value
      queryClient.setQueryData(queryKey, (old: any) => {
        return mutationFn(variables)
      })

      try {
        // Execute the mutation
        const result = await mutationFn(variables)
        return result
      } catch (err) {
        // Rollback on error
        queryClient.setQueryData(queryKey, previousData)
        throw err
      }
    },
  }
}
