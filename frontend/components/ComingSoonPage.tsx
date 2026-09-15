// Reusable placeholder for pages that are coming in future phases
"use client";

import React from "react";
import Link from "next/link";
import { LucideIcon, Construction, ArrowLeft } from "lucide-react";

interface ComingSoonPageProps {
  title: string;
  description: string;
  phase: string;
  icon: LucideIcon;
  features: string[];
  color: string;
}

export default function ComingSoonPage({
  title,
  description,
  phase,
  icon: Icon,
  features,
  color,
}: ComingSoonPageProps) {
  return (
    <div className="flex-1 flex items-center justify-center px-4 py-16">
      <div className="max-w-lg w-full text-center space-y-6">
        {/* Icon */}
        <div className={`w-20 h-20 mx-auto rounded-3xl flex items-center justify-center ${color}`}>
          <Icon className="w-10 h-10" />
        </div>

        {/* Phase badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-50 dark:bg-amber-950/50 border border-amber-200 dark:border-amber-800 text-amber-700 dark:text-amber-300 text-xs font-semibold">
          <Construction className="w-3.5 h-3.5" />
          <span>{phase}</span>
        </div>

        <div className="space-y-2">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">{title}</h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">{description}</p>
        </div>

        {/* Features preview */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-left space-y-3">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Coming in this phase:
          </p>
          <ul className="space-y-2">
            {features.map((f) => (
              <li key={f} className="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-300">
                <span className="mt-0.5 w-4 h-4 rounded-full bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400 flex items-center justify-center text-xs font-bold shrink-0">✓</span>
                {f}
              </li>
            ))}
          </ul>
        </div>

        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:underline"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
}
