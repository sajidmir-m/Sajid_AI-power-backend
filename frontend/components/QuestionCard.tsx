"use client";

import { useMemo, useState } from "react";
import type { QuizQuestion } from "@/services/api";

export default function QuestionCard({
  q,
  onSubmit
}: {
  q: QuizQuestion;
  onSubmit: (selected: string) => Promise<void>;
}) {
  const options = useMemo(() => {
    if (q.type === "TF") return ["True", "False"];
    if (q.type === "MCQ") return q.options || [];
    return [];
  }, [q]);

  const [selected, setSelected] = useState<string>("");
  const [busy, setBusy] = useState(false);

  async function submit() {
    if (!selected && q.type !== "FIB") return;
    setBusy(true);
    try {
      await onSubmit(q.type === "FIB" ? selected : selected);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="grid gap-5 rounded-2xl border border-slate-800/80 bg-slate-950/70 p-5">
      <div>
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>
            QID {q.question_id} • {q.type} • {q.difficulty}
          </span>
          <span className="rounded-full bg-slate-900/80 px-2 py-0.5 text-[10px] text-slate-500">Aligned to source text</span>
        </div>
        <div className="mt-3 text-base font-medium leading-relaxed text-slate-50">{q.question}</div>
      </div>

      {q.type === "FIB" ? (
        <div className="grid gap-2">
          <label className="text-sm text-slate-300">Your answer</label>
          <input
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
            className="rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-sm outline-none ring-0 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/60"
            placeholder="Type your answer..."
          />
        </div>
      ) : (
        <div className="grid gap-2">
          {options.map((opt) => (
            <label
              key={opt}
              className={`flex cursor-pointer items-center gap-2 rounded-xl border px-3 py-2 text-sm transition-colors ${
                selected === opt
                  ? "border-sky-500 bg-sky-500/15 text-slate-50"
                  : "border-slate-800 bg-slate-950/40 text-slate-100 hover:border-slate-600"
              }`}
            >
              <input
                type="radio"
                name="opt"
                value={opt}
                checked={selected === opt}
                onChange={() => setSelected(opt)}
                className="h-3 w-3 accent-sky-500"
              />
              <span>{opt}</span>
            </label>
          ))}
        </div>
      )}

      <button
        onClick={submit}
        disabled={busy || (q.type !== "FIB" && !selected) || (q.type === "FIB" && !selected.trim())}
        className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-sky-500 to-cyan-400 px-5 py-2 text-sm font-semibold text-slate-950 shadow-md shadow-sky-500/40 hover:from-sky-400 hover:to-cyan-300 disabled:opacity-60"
      >
        {busy ? "Submitting..." : "Submit answer"}
      </button>
    </div>
  );
}

