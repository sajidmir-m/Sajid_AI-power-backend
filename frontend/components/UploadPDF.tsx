"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { uploadPDF } from "@/services/api";

export default function UploadPDF() {
  const router = useRouter();

  const [file, setFile] = useState<File | null>(null);
  const [grade, setGrade] = useState<number>(3);
  const [subject, setSubject] = useState<string>("Science");
  const [topic, setTopic] = useState<string>("Plants");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);
    if (!file) {
      setError("Please choose a PDF file.");
      return;
    }
    setBusy(true);
    try {
      const res = await uploadPDF({ file, grade, subject, topic, generate_quiz: true });
      setResult(
        `Ingested ${res.source_document.filename}. Stored ${res.chunks_stored} chunks (source_id=${res.source_id}). Redirecting to quiz...`
      );

      // Redirect the user to the quiz page for this topic so they immediately see questions
      router.push(`/quiz?topic=${encodeURIComponent(topic)}&difficulty=easy`);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Upload failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6">
      <h2 className="mb-1 text-lg font-semibold">Upload PDF</h2>
      <p className="mb-6 text-sm text-slate-300">
        Upload a PDF, we&apos;ll read it, extract the content, and auto-generate quiz questions only from that file.
      </p>

      <form onSubmit={onSubmit} className="grid gap-4">
        <div className="grid gap-2">
          <label className="text-sm text-slate-300">PDF file</label>
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm"
          />
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div className="grid gap-2">
            <label className="text-sm text-slate-300">Grade</label>
            <input
              type="number"
              min={1}
              max={12}
              value={grade}
              onChange={(e) => setGrade(Number(e.target.value))}
              className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm"
            />
          </div>
          <div className="grid gap-2">
            <label className="text-sm text-slate-300">Subject</label>
            <input
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm"
            />
          </div>
          <div className="grid gap-2">
            <label className="text-sm text-slate-300">Topic</label>
            <input
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={busy}
          className="inline-flex items-center justify-center rounded-lg bg-indigo-500 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-400 disabled:opacity-60"
        >
          {busy ? "Uploading..." : "Upload & Generate Quiz"}
        </button>

        {result && <div className="rounded-lg border border-emerald-800 bg-emerald-950/40 p-3 text-sm">{result}</div>}
        {error && <div className="rounded-lg border border-rose-800 bg-rose-950/40 p-3 text-sm">{error}</div>}
      </form>
    </div>
  );
}

