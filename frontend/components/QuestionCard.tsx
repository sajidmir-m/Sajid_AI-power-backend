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
    <div className="grid gap-4">
      <div>
        <div className="text-xs text-slate-400">
          {q.question_id} • {q.type} • {q.difficulty} • chunk: {q.source_chunk_id}
        </div>
        <div className="mt-2 text-base font-medium">{q.question}</div>
      </div>

      {q.type === "FIB" ? (
        <div className="grid gap-2">
          <label className="text-sm text-slate-300">Your answer</label>
          <input
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm"
            placeholder="Type your answer..."
          />
        </div>
      ) : (
        <div className="grid gap-2">
          {options.map((opt) => (
            <label
              key={opt}
              className={`flex cursor-pointer items-center gap-2 rounded-lg border px-3 py-2 text-sm ${
                selected === opt ? "border-indigo-500 bg-indigo-950/30" : "border-slate-800 bg-slate-950/30"
              }`}
            >
              <input
                type="radio"
                name="opt"
                value={opt}
                checked={selected === opt}
                onChange={() => setSelected(opt)}
              />
              <span>{opt}</span>
            </label>
          ))}
        </div>
      )}

      <button
        onClick={submit}
        disabled={busy || (q.type !== "FIB" && !selected) || (q.type === "FIB" && !selected.trim())}
        className="inline-flex items-center justify-center rounded-lg bg-indigo-500 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-400 disabled:opacity-60"
      >
        {busy ? "Submitting..." : "Submit Answer"}
      </button>
    </div>
  );
}

