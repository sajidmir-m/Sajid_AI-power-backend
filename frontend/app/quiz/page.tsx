"use client";

import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import QuizCard from "@/components/QuizCard";
import QuestionCard from "@/components/QuestionCard";
import { getQuiz, submitAnswer, type Difficulty, type QuizQuestion } from "@/services/api";

const difficulties: Difficulty[] = ["easy", "medium", "hard"];

export default function QuizPage() {
  const searchParams = useSearchParams();
  const initialTopic = searchParams.get("topic") || "Plants";
  const initialDifficulty = (searchParams.get("difficulty") as Difficulty) || "easy";

  const [topic, setTopic] = useState(initialTopic);
  const [studentId, setStudentId] = useState("S001");
  const [difficulty, setDifficulty] = useState<Difficulty>(initialDifficulty);

  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [idx, setIdx] = useState(0);
  const [busy, setBusy] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const current = useMemo(() => questions[idx] || null, [questions, idx]);

  async function fetchQuestions(nextDifficulty: Difficulty) {
    setError(null);
    setBusy(true);
    try {
      const res = await getQuiz({ topic, difficulty: nextDifficulty, limit: 5, auto_generate: true });
      setQuestions(res.questions);
      setIdx(0);
      if (res.questions.length === 0) {
        setFeedback("No questions found yet. Upload a PDF and ensure the topic matches.");
      } else {
        setFeedback(null);
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Failed to fetch quiz.");
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    // On first load, automatically fetch questions for the topic passed from the upload page
    fetchQuestions(initialDifficulty);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function onSubmit(selected: string) {
    if (!current) return;
    setFeedback(null);
    setError(null);
    try {
      const res = await submitAnswer({
        student_id: studentId,
        question_id: current.question_id,
        selected_answer: selected,
        current_difficulty: difficulty
      });

      setFeedback(res.is_correct ? "Correct!" : `Incorrect. Correct answer: ${res.correct_answer}`);

      // Update difficulty adaptively.
      setDifficulty(res.recommended_difficulty);

      // Move to next question if available; otherwise refetch at new difficulty.
      const nextIndex = idx + 1;
      if (nextIndex < questions.length) {
        setIdx(nextIndex);
      } else {
        await fetchQuestions(res.recommended_difficulty);
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Failed to submit answer.");
    }
  }

  return (
    <div className="grid gap-6">
      <QuizCard title={`Quiz for topic: ${topic}`}>
        <div className="grid gap-4">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div className="grid gap-2">
              <label className="text-sm text-slate-300">Topic</label>
              <input
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm"
              />
            </div>
            <div className="grid gap-2">
              <label className="text-sm text-slate-300">Student ID</label>
              <input
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm"
              />
            </div>
            <div className="grid gap-2">
              <label className="text-sm text-slate-300">Difficulty</label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value as Difficulty)}
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm"
              >
                {difficulties.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => fetchQuestions(difficulty)}
              disabled={busy}
              className="rounded-lg bg-indigo-500 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-400 disabled:opacity-60"
            >
              {busy ? "Loading..." : "Fetch Questions"}
            </button>
            <div className="text-xs text-slate-400 self-center">
              Adaptive engine will change difficulty after each submission.
            </div>
          </div>

          {error && <div className="rounded-lg border border-rose-800 bg-rose-950/40 p-3 text-sm">{error}</div>}
          {feedback && (
            <div className="rounded-lg border border-slate-700 bg-slate-950/40 p-3 text-sm text-slate-200">
              {feedback}
            </div>
          )}

          {current ? (
            <QuestionCard q={current} onSubmit={onSubmit} />
          ) : (
            <div className="text-sm text-slate-300">No question loaded yet. Try uploading a PDF for this topic.</div>
          )}
        </div>
      </QuizCard>
    </div>
  );
}

