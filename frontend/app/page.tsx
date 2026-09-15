import Link from "next/link";
import {
  Sparkles,
  BookOpen,
  HelpCircle,
  Award,
  Layers,
  Calendar,
  ShieldCheck,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";

export default function LandingPage() {
  const features = [
    {
      title: "RAG-Powered Grounding",
      desc: "Answers are derived directly from your uploaded textbooks and notes with exact page citations.",
      icon: ShieldCheck,
      color: "text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/50",
    },
    {
      title: "AI Study Chat",
      desc: "ChatGPT-like conversational interface designed for deep concept clarification and revision.",
      icon: HelpCircle,
      color: "text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/50",
    },
    {
      title: "Automated Quiz Generator",
      desc: "Generate MCQs and True/False tests with instant grading and topic weakness analysis.",
      icon: Award,
      color: "text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/50",
    },
    {
      title: "Interactive Flashcards",
      desc: "Master definitions and formulas with digital flip cards and active recall tracking.",
      icon: Layers,
      color: "text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/50",
    },
    {
      title: "Personalized Study Plans",
      desc: "AI timetable generation based on your exam dates, weak topics, and daily study hours.",
      icon: Calendar,
      color: "text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-950/50",
    },
    {
      title: "Instant Summaries",
      desc: "Condense 50-page slides into executive summaries, key concepts, formulas, and definitions.",
      icon: BookOpen,
      color: "text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/50",
    },
  ];

  return (
    <div className="flex-1 flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-16 sm:py-24 bg-gradient-to-b from-white via-indigo-50/30 to-slate-50 dark:from-slate-950 dark:via-indigo-950/20 dark:to-slate-900 border-b border-slate-200/60 dark:border-slate-800/60">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-100/80 dark:bg-indigo-950/70 border border-indigo-200 dark:border-indigo-800 text-xs font-semibold text-indigo-700 dark:text-indigo-300">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Built for College & University Students</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-[1.15]">
            Master Any Course with <br />
            <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              AI Grounded in Your Materials
            </span>
          </h1>

          <p className="max-w-2xl mx-auto text-base sm:text-lg text-slate-600 dark:text-slate-300 leading-relaxed">
            Upload your lecture slides, notes, and PDFs. EduMind uses Retrieval-Augmented Generation (RAG) to provide exact answers with source citations, generate practice quizzes, and build custom study plans.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3.5 pt-4">
            <Link
              href="/register"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm shadow-lg shadow-indigo-600/25 transition-all"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              href="/login"
              className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3.5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-200 font-semibold text-sm shadow-sm transition-all"
            >
              Sign In to Dashboard
            </Link>
          </div>

          <div className="flex items-center justify-center gap-6 pt-6 text-xs text-slate-500 dark:text-slate-400">
            <div className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              <span>No hallucinated answers</span>
            </div>
            <div className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              <span>Exact citations</span>
            </div>
            <div className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              <span>Adaptive quizzes</span>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-16 sm:py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="text-center space-y-2 max-w-2xl mx-auto">
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
            Everything You Need for Exam Success
          </h2>
          <p className="text-sm sm:text-base text-slate-500 dark:text-slate-400">
            A comprehensive, all-in-one AI study platform designed from the ground up to boost student productivity.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f) => {
            const Icon = f.icon;
            return (
              <div
                key={f.title}
                className="p-6 rounded-3xl bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700/80 shadow-sm hover:shadow-md transition-all space-y-3"
              >
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${f.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="font-bold text-slate-900 dark:text-white text-base">
                  {f.title}
                </h3>
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
                  {f.desc}
                </p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
