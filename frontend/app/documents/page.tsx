"use client";
import ComingSoonPage from "@/components/ComingSoonPage";
import { Upload } from "lucide-react";

export default function DocumentsPage() {
  return (
    <ComingSoonPage
      title="Document Management"
      description="Upload your lecture notes, PDFs, and study material. EduMind will extract text, chunk it intelligently, and build a searchable vector knowledge base from your content."
      phase="Phase 2 — Coming Next"
      icon={Upload}
      color="bg-blue-100 dark:bg-blue-950/50 text-blue-600 dark:text-blue-400"
      features={[
        "Drag-and-drop upload for PDF, DOCX, and TXT files",
        "Automatic text extraction and cleaning pipeline",
        "Intelligent chunking with configurable overlap",
        "Document list with processing status indicators",
        "Delete and re-process documents",
      ]}
    />
  );
}
