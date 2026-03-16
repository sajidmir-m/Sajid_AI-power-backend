"use client";

import type { ReactNode } from "react";

export default function QuizCard({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="rounded-2xl border border-slate-800/70 bg-slate-950/85 p-6 shadow-xl shadow-sky-900/25">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold tracking-tight text-slate-50">{title}</h2>
          <p className="mt-1 text-xs text-slate-400">Answer the questions below. Your level will adapt as you progress.</p>
        </div>
      </div>
      <div className="mt-3">{children}</div>
    </section>
  );
}

