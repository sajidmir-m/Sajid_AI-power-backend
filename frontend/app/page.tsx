import Link from "next/link";

export default function HomePage() {
  return (
    <div className="grid gap-10 md:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] items-start">
      <section className="rounded-2xl border border-slate-800/70 bg-slate-950/80 p-7 shadow-xl shadow-sky-900/25">
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-sky-400">Adaptive learning platform</p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-50 md:text-4xl">
          Turn any lesson PDF into a{" "}
          <span className="bg-gradient-to-r from-sky-400 to-cyan-300 bg-clip-text text-transparent">
            personalised quiz
          </span>
          .
        </h1>
        <p className="mt-4 max-w-xl text-sm leading-relaxed text-slate-300">
          Upload your teaching material once. Aurora Learn extracts the key ideas, generates traceable questions, and adapts
          difficulty in real time as students answer.
        </p>

        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            href="/upload"
            className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-sky-500 to-cyan-400 px-5 py-2.5 text-sm font-semibold text-slate-950 shadow-md shadow-sky-500/40 hover:from-sky-400 hover:to-cyan-300"
          >
            Upload PDF
          </Link>
          <Link
            href="/quiz"
            className="inline-flex items-center justify-center rounded-full border border-slate-700/80 bg-slate-950/60 px-5 py-2.5 text-sm font-semibold text-slate-100 hover:border-sky-500/70"
          >
            Go to Quiz
          </Link>
        </div>
      </section>

      <aside className="grid gap-4">
        <div className="rounded-2xl border border-slate-800/70 bg-slate-950/80 p-5 text-xs text-slate-300">
          <div className="mb-3 text-sm font-semibold text-slate-100">How it works</div>
          <ol className="space-y-2">
            <li>
              <span className="font-semibold text-sky-300">1.</span> Upload a lesson PDF with grade, subject, and topic.
            </li>
            <li>
              <span className="font-semibold text-sky-300">2.</span> The engine reads, cleans, and chunks the content.
            </li>
            <li>
              <span className="font-semibold text-sky-300">3.</span> Quiz questions are generated and tied to the source text.
            </li>
            <li>
              <span className="font-semibold text-sky-300">4.</span> Students answer and difficulty adjusts automatically.
            </li>
          </ol>
        </div>
      </aside>
    </div>
  );
}

