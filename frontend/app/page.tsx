import Link from "next/link";

export default function HomePage() {
  return (
    <div className="grid gap-6">
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6">
        <h1 className="text-2xl font-semibold tracking-tight">Mini Content Ingestion + Adaptive Quiz Engine</h1>
        <p className="mt-2 max-w-2xl text-sm text-slate-300">
          Upload a PDF, the backend extracts and chunks the content, then an LLM generates quiz questions. Students answer
          questions and the system adapts difficulty (easy → medium → hard).
        </p>
        <div className="mt-5 flex gap-3">
          <Link
            href="/upload"
            className="rounded-lg bg-indigo-500 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-400"
          >
            Upload PDF
          </Link>
          <Link
            href="/quiz"
            className="rounded-lg border border-slate-700 bg-slate-950/40 px-4 py-2 text-sm font-semibold text-slate-100 hover:border-slate-500"
          >
            Start Quiz
          </Link>
        </div>
      </div>

      <div className="grid gap-3 text-sm text-slate-300">
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6">
          <div className="font-semibold text-slate-100">Backend endpoints</div>
          <ul className="mt-2 list-disc pl-5">
            <li>POST /ingest</li>
            <li>GET /quiz?topic=...&difficulty=easy</li>
            <li>POST /submit-answer</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

