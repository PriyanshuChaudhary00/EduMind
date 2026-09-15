"use client";

import { useState, useEffect, useRef } from "react";
import { Send, Loader2, Bot, User, FileText } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { apiRequest } from "@/lib/api";

interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, sending]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const res = await apiRequest<{ messages: ChatMessage[] }>("/chat/history");
      setMessages(res.messages);
    } catch (err) {
      console.error("Failed to load chat history", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || sending) return;

    const userMessage = input.trim();
    setInput("");
    
    // Optimistic UI update
    const tempId = Date.now();
    setMessages((prev) => [
      ...prev,
      { id: tempId, role: "user", content: userMessage, created_at: new Date().toISOString() }
    ]);
    
    setSending(true);
    try {
      const response = await apiRequest<ChatMessage>("/chat/send", {
        method: "POST",
        body: JSON.stringify({ message: userMessage }),
      });
      setMessages((prev) => [...prev, response]);
    } catch (err: any) {
      console.error(err);
      // Optional: add a visual error message inside the chat
    } finally {
      setSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-500" />
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full bg-white dark:bg-slate-900 border-x border-slate-200 dark:border-slate-800 shadow-sm relative h-[calc(100vh-64px)]">
      
      {/* Header */}
      <div className="flex items-center gap-3 px-6 py-4 border-b border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
          <Bot className="w-6 h-6" />
        </div>
        <div>
          <h1 className="font-semibold text-slate-900 dark:text-white">EduMind AI</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Powered by Gemini & your documents</p>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center space-y-4 px-4">
            <div className="w-16 h-16 bg-slate-100 dark:bg-slate-800 rounded-2xl flex items-center justify-center text-slate-400">
              <FileText className="w-8 h-8" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Chat with your notes</h2>
              <p className="text-slate-500 dark:text-slate-400 max-w-md mt-1">
                Ask a question about the documents you've uploaded, and I'll find the exact paragraphs to give you an accurate answer.
              </p>
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className={`flex gap-4 ${msg.role === "user" ? "justify-end" : ""}`}>
              {msg.role === "assistant" && (
                <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400 shrink-0 mt-1">
                  <Bot className="w-4 h-4" />
                </div>
              )}
              
              <div 
                className={`max-w-[80%] rounded-2xl px-5 py-3.5 ${
                  msg.role === "user" 
                    ? "bg-indigo-600 text-white" 
                    : "bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100"
                }`}
              >
                {msg.role === "user" ? (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                ) : (
                  <div className="prose prose-sm dark:prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-slate-900">
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        
        {sending && (
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400 shrink-0 mt-1">
              <Loader2 className="w-4 h-4 animate-spin" />
            </div>
            <div className="max-w-[80%] rounded-2xl px-5 py-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: "0ms" }}></span>
              <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: "150ms" }}></span>
              <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: "300ms" }}></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Box */}
      <div className="p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
        <form 
          onSubmit={handleSend}
          className="relative flex items-end bg-slate-100 dark:bg-slate-800 rounded-3xl border border-transparent focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-500/20 transition-all overflow-hidden p-2"
        >
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about your study materials..."
            className="flex-1 max-h-32 min-h-[44px] bg-transparent border-none focus:ring-0 resize-none px-4 py-3 text-slate-900 dark:text-white placeholder-slate-400 outline-none"
            rows={input.split("\n").length > 1 ? Math.min(input.split("\n").length, 5) : 1}
          />
          <button
            type="submit"
            disabled={!input.trim() || sending}
            className="p-3 mb-1 mr-1 rounded-full bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shrink-0"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <p className="text-center text-[10px] text-slate-400 mt-3 font-medium">
          EduMind can make mistakes. Check your source materials.
        </p>
      </div>
      
    </div>
  );
}
