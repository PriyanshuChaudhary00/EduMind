"use client";
import ComingSoonPage from "@/components/ComingSoonPage";
import { Calendar } from "lucide-react";

export default function StudyPlanPage() {
  return (
    <ComingSoonPage
      title="Personalized Study Plan"
      description="Tell EduMind your subjects, exam dates, available study hours, and weak topics. It will generate a custom day-by-day study schedule prioritizing your gaps."
      phase="Phase 8 — Study Planner"
      icon={Calendar}
      color="bg-purple-100 dark:bg-purple-950/50 text-purple-600 dark:text-purple-400"
      features={[
        "Input: subjects, exam date, available hours/day, difficulty rating",
        "AI-generated day-by-day schedule prioritizing weak areas",
        "Balances study, revision, and quiz sessions automatically",
        "Exportable plan with daily topic breakdown",
        "Adapts the schedule as you complete tasks",
      ]}
    />
  );
}
