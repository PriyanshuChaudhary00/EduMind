"use client";
import ComingSoonPage from "@/components/ComingSoonPage";
import { MessageSquare } from "lucide-react";

export default function ChatPage() {
  return (
    <ComingSoonPage
      title="AI Study Chat"
      description="A ChatGPT-like interface where every answer is grounded in your uploaded study materials using Retrieval-Augmented Generation (RAG). No hallucinations — just precise, cited answers."
      phase="Phase 4 — RAG Chatbot"
      icon={MessageSquare}
      color="bg-indigo-100 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400"
      features={[
        "RAG pipeline: query → vector search → context → LLM answer",
        "Source citations with document name and page references",
        "Multi-turn conversation history with streaming responses",
        "Ask about all documents or a specific document",
        "Markdown + code formatting in responses",
      ]}
    />
  );
}
