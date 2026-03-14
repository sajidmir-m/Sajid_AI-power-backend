import "./../styles/globals.css";
import Link from "next/link";
import type { ReactNode } from "react";

export const metadata = {
  title: "Mini Ingestion + Adaptive Quiz",
  description: "Prototype educational platform"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <div className="mx-auto max-w-5xl px-4 py-6">
          <header className="mb-6 flex items-center justify-between">
            <Link href="/" className="text-lg font-semibold tracking-tight">
              Mini Quiz Engine
            </Link>
            <nav className="flex gap-4 text-sm text-slate-300">
              <Link href="/upload" className="hover:text-white">
                Upload
              </Link>
              <Link href="/quiz" className="hover:text-white">
                Quiz
              </Link>
            </nav>
          </header>
          <main>{children}</main>
          <footer className="mt-10 border-t border-slate-800 pt-6 text-xs text-slate-400">
            Backend: FastAPI • Frontend: Next.js • DB: SQLite
          </footer>
        </div>
      </body>
    </html>
  );
}

