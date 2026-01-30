'use client'

import React, { useCallback, useRef, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import * as monaco from 'monaco-editor'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

export interface CodeEditorProps {
  code: string
  onChange: (code: string) => void
  onRun?: () => void
  language?: string
  readOnly?: boolean
  height?: string | number
  showRunButton?: boolean
  isLoading?: boolean
  className?: string
  placeholder?: string
}

const CodeEditor: React.FC<CodeEditorProps> = ({
  code,
  onChange,
  onRun,
  language = 'python',
  readOnly = false,
  height = '400px',
  showRunButton = true,
  isLoading = false,
  className,
  placeholder = '# Write your Python code here',
}) => {
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null)

  // Configure Python language features
  const handleEditorDidMount = useCallback((editor: monaco.editor.IStandaloneCodeEditor) => {
    editorRef.current = editor

    // Configure Python indentation
    editor.updateOptions({
      tabSize: 4,
      insertSpaces: true,
      detectIndentation: true,
      autoIndent: 'full',
      formatOnPaste: true,
      formatOnType: true,
    })

    // Add keyboard shortcut for running code (Ctrl+Enter)
    if (onRun) {
      editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
        onRun()
      })
    }
  }, [onRun])

  // Restore code from localStorage on mount (autosave)
  useEffect(() => {
    const savedCode = localStorage.getItem('learnflow-draft-code')
    if (savedCode && !code) {
      onChange(savedCode)
    }
  }, [])

  // Autosave to localStorage
  useEffect(() => {
    if (code && code.trim()) {
      localStorage.setItem('learnflow-draft-code', code)
    }
  }, [code])

  const handleRun = useCallback(() => {
    if (onRun && !readOnly && !isLoading) {
      onRun()
    }
  }, [onRun, readOnly, isLoading])

  return (
    <div className={cn('flex flex-col', className)}>
      {/* Toolbar */}
      <div className="flex items-center justify-between rounded-t-lg border border-b-0 border-slate-200 bg-slate-50 px-3 py-2 dark:border-slate-700 dark:bg-slate-800">
        <div className="flex items-center gap-2">
          <div className="flex h-3 w-3 items-center gap-1.5">
            <div className="h-3 w-3 rounded-full bg-error-500" />
            <div className="h-3 w-3 rounded-full bg-warning-500" />
            <div className="h-3 w-3 rounded-full bg-success-500" />
          </div>
          <span className="ml-2 text-sm font-medium text-slate-600 dark:text-slate-400">
            {language === 'python' ? 'Python' : language}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">
            Ctrl+Enter to run
          </span>
          {showRunButton && onRun && (
            <Button
              size="sm"
              onClick={handleRun}
              isLoading={isLoading}
              disabled={readOnly}
              className="h-7"
            >
              <svg className="mr-1.5 h-3.5 w-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
              </svg>
              Run
            </Button>
          )}
        </div>
      </div>

      {/* Editor */}
      <div className="rounded-b-lg border border-t-0 border-slate-200 dark:border-slate-700">
        <Editor
          height={height}
          defaultLanguage="python"
          language={language}
          value={code || placeholder}
          onChange={(value) => onChange(value || '')}
          onMount={handleEditorDidMount}
          theme="vs-dark"
          options={{
            readOnly,
            minimap: { enabled: true },
            fontSize: 14,
            lineHeight: 22,
            fontFamily: "'Fira Code', 'JetBrains Mono', 'Consolas', monospace",
            fontLigatures: true,
            padding: { top: 16, bottom: 16 },
            scrollBeyondLastLine: false,
            renderWhitespace: 'selection',
            guides: {
              indentation: true,
              bracketPairs: true,
            },
            automaticLayout: true,
            suggest: {
              snippetsPreventQuickSuggestions: false,
            },
            quickSuggestions: {
              other: true,
              comments: false,
              strings: false,
            },
          }}
        />
      </div>
    </div>
  )
}

export default CodeEditor
