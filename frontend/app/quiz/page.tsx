"use client";
import ComingSoonPage from "@/components/ComingSoonPage";
import { Award } from "lucide-react";

export default function QuizPage() {
  return (
    <ComingSoonPage
      title="Quiz Generator"
      description="Automatically generate quizzes from your uploaded study material. Choose difficulty, question types, and get instant grading with topic-wise performance analysis."
      phase="Phase 6 — Quiz Generator"
      icon={Award}
      color="bg-emerald-100 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400"
      features={[
        "AI-generated MCQ and True/False questions from your notes",
        "Configurable: number of questions, difficulty (Easy/Medium/Hard)",
        "Instant grading with correct answer explanations",
        "Topic-wise performance breakdown (strong vs. weak areas)",
        "Score history and progress tracking over time",
      ]}
    />
  );
}
