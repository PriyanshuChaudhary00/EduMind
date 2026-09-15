"use client";
import ComingSoonPage from "@/components/ComingSoonPage";
import { Layers } from "lucide-react";

export default function FlashcardsPage() {
  return (
    <ComingSoonPage
      title="Flashcard Generator"
      description="Turn your study material into interactive digital flashcards. Each card is auto-generated from your notes with a question front and detailed answer back."
      phase="Phase 7 — Flashcards"
      icon={Layers}
      color="bg-amber-100 dark:bg-amber-950/50 text-amber-600 dark:text-amber-400"
      features={[
        "Auto-generated flashcards from document chunks (key terms, definitions, formulas)",
        "3D flip-card animation for active recall practice",
        "Mark cards as Known or Needs Review",
        "Next/Previous navigation with progress tracker",
        "Spaced repetition scheduling for weak cards",
      ]}
    />
  );
}
