import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import {
  Code2,
  Brain,
  TrendingUp,
  Zap,
  MessageSquare,
  CheckCircle2,
  ArrowRight,
} from 'lucide-react'

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-primary-700">
              <Code2 className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold text-white">LearnFlow</span>
          </div>

          <nav className="hidden items-center gap-6 sm:flex">
            <a href="#features" className="text-sm text-slate-400 hover:text-white transition-colors">
              Features
            </a>
            <a href="#how-it-works" className="text-sm text-slate-400 hover:text-white transition-colors">
              How It Works
            </a>
            <a href="#pricing" className="text-sm text-slate-400 hover:text-white transition-colors">
              Pricing
            </a>
          </nav>

          <div className="flex items-center gap-3">
            <Link href="/auth/sign-in">
              <Button variant="ghost" size="sm" className="text-slate-300">
                Sign In
              </Button>
            </Link>
            <Link href="/auth/sign-up">
              <Button size="sm">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-primary-950/50 to-slate-950">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10" />
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-primary-500/10 px-4 py-2 text-sm text-primary-400">
              <Zap className="h-4 w-4" />
              <span>AI-Powered Python Learning</span>
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl md:text-6xl">
              Master Python with{' '}
              <span className="bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                Personalized AI Tutors
              </span>
            </h1>
            <p className="mt-6 text-lg text-slate-400">
              Learn Python at your own pace with intelligent tutoring, real-time code execution,
              and adaptive exercises that match your skill level.
            </p>
            <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-center">
              <Link href="/auth/sign-up">
                <Button size="lg" className="min-w-[160px]">
                  Start Learning Free
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
              <Link href="/auth/sign-in">
                <Button size="lg" variant="secondary" className="min-w-[160px]">
                  Try Demo
                </Button>
              </Link>
            </div>
          </div>

          {/* Preview */}
          <div className="mt-16">
            <Card className="mx-auto max-w-4xl border-slate-800 bg-slate-900/50 backdrop-blur">
              <CardContent className="p-0">
                <div className="flex items-center gap-2 border-b border-slate-800 px-4 py-3">
                  <div className="flex gap-1.5">
                    <div className="h-3 w-3 rounded-full bg-red-500" />
                    <div className="h-3 w-3 rounded-full bg-yellow-500" />
                    <div className="h-3 w-3 rounded-full bg-green-500" />
                  </div>
                  <span className="ml-2 text-sm text-slate-500">learning-workspace.py</span>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-2">
                  <div className="border-r border-slate-800 p-4">
                    <div className="mb-3 flex items-center gap-2 text-sm text-slate-400">
                      <MessageSquare className="h-4 w-4" />
                      <span>AI Tutor</span>
                    </div>
                    <div className="space-y-3 text-sm">
                      <div className="rounded-lg bg-slate-800 p-3 text-slate-300">
                        How do I write a for loop in Python?
                      </div>
                      <div className="rounded-lg bg-primary-500/10 p-3 text-slate-300">
                        <div className="mb-1 flex items-center gap-1 text-xs text-primary-400">
                          <Brain className="h-3 w-3" />
                          <span>Concepts Agent</span>
                        </div>
                        Here's how to write a for loop in Python:
                        <code className="mt-2 block rounded bg-slate-900 p-2 text-xs">
                          for i in range(5):{'\n'}    print(i)
                        </code>
                      </div>
                    </div>
                  </div>
                  <div className="bg-slate-950 p-4">
                    <pre className="text-sm text-slate-300">
                      <span className="text-purple-400">for</span> i <span className="text-purple-400">in</span> <span className="text-blue-400">range</span>(<span className="text-orange-400">5</span>):
                      <br />
                      &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-blue-400">print</span>(i)
                      <br />
                      <br />
                      <span className="text-slate-500"># Output:</span>
                      <br />
                      <span className="text-slate-500"># 0</span>
                      <br />
                      <span className="text-slate-500"># 1</span>
                      <br />
                      <span className="text-slate-500"># 2</span>
                      <br />
                      <span className="text-slate-500"># 3</span>
                      <br />
                      <span className="text-slate-500"># 4</span>
                    </pre>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="border-t border-slate-800 bg-slate-950 py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold text-white sm:text-4xl">
              Everything you need to master Python
            </h2>
            <p className="mt-4 text-lg text-slate-400">
              Our AI-powered platform adapts to your learning style and pace
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {[
              {
                icon: Brain,
                title: 'AI Tutors',
                description: 'Get personalized help from specialized AI agents that understand your learning style.',
              },
              {
                icon: Code2,
                title: 'Real-time Execution',
                description: 'Run Python code directly in your browser with instant feedback and output.',
              },
              {
                icon: TrendingUp,
                title: 'Adaptive Learning',
                description: 'Exercises and quizzes that adapt to your skill level and learning pace.',
              },
              {
                icon: MessageSquare,
                title: 'Interactive Chat',
                description: 'Chat with AI tutors who explain concepts, debug errors, and provide hints.',
              },
              {
                icon: Zap,
                title: 'Instant Feedback',
                description: 'Get immediate feedback on your code with detailed explanations and suggestions.',
              },
              {
                icon: CheckCircle2,
                title: 'Progress Tracking',
                description: 'Track your mastery across topics with detailed analytics and streaks.',
              },
            ].map((feature) => (
              <Card key={feature.title} className="border-slate-800 bg-slate-900/50">
                <CardContent className="p-6">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-500/10">
                    <feature.icon className="h-6 w-6 text-primary-400" />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-white">{feature.title}</h3>
                  <p className="mt-2 text-slate-400">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="border-t border-slate-800 bg-slate-950 py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold text-white sm:text-4xl">How it works</h2>
            <p className="mt-4 text-lg text-slate-400">
              Start learning Python in three simple steps
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-8 lg:grid-cols-3">
            {[
              {
                step: '01',
                title: 'Create your account',
                description: 'Sign up for free and tell us about your programming experience.',
              },
              {
                step: '02',
                title: 'Start learning',
                description: 'Work through interactive exercises and get help from AI tutors when stuck.',
              },
              {
                step: '03',
                title: 'Track your progress',
                description: 'Watch your mastery grow as you complete modules and build projects.',
              },
            ].map((item) => (
              <div key={item.step} className="relative">
                <div className="text-8xl font-bold text-slate-800">{item.step}</div>
                <div className="relative -mt-12">
                  <h3 className="text-xl font-semibold text-white">{item.title}</h3>
                  <p className="mt-2 text-slate-400">{item.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-slate-800 bg-gradient-to-b from-slate-950 to-primary-950/30 py-24">
        <div className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to start your Python journey?
          </h2>
          <p className="mt-4 text-lg text-slate-400">
            Join thousands of students learning Python with AI-powered tutors.
          </p>
          <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-center">
            <Link href="/auth/sign-up">
              <Button size="lg">
                Get Started Free
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950 py-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <div className="flex items-center gap-2">
              <Code2 className="h-6 w-6 text-primary-400" />
              <span className="text-lg font-bold text-white">LearnFlow</span>
            </div>
            <p className="text-sm text-slate-500">
              © 2025 LearnFlow. Built for Hackathon III.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
