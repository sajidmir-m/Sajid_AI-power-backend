import "./../styles/globals.css";
import Link from "next/link";
import type { ReactNode } from "react";

export const metadata = {
  title: "Aurora Learn | Adaptive Quiz",
  description: "Upload learning content and generate adaptive quizzes for your students."
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-50">
        <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-4 py-6">
          <header className="mb-6 flex items-center justify-between rounded-2xl border border-slate-800/60 bg-slate-950/70 px-5 py-3 shadow-lg shadow-sky-900/20 backdrop-blur">
            <Link href="/" className="flex items-center gap-2 text-lg font-semibold tracking-tight">
              <span className="inline-flex h-7 w-7 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-cyan-400 text-xs font-bold text-slate-950 shadow-sm shadow-sky-500/40">
                AL
              </span>
              <span className="bg-gradient-to-r from-sky-300 to-cyan-200 bg-clip-text text-transparent">
                Aurora Learn
              </span>
            </Link>
            <nav className="flex items-center gap-4 text-sm text-slate-300">
              <Link href="/upload" className="rounded-full px-3 py-1 hover:bg-slate-800/70 hover:text-slate-50">
                Upload
              </Link>
              <Link href="/quiz" className="rounded-full px-3 py-1 hover:bg-slate-800/70 hover:text-slate-50">
                Quiz
              </Link>
            </nav>
          </header>

          <main className="flex-1 pb-6">{children}</main>
        </div>
      </body>
    </html>
  );
}

