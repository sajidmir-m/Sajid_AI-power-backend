import UploadPDF from "@/components/UploadPDF";

export default function UploadPage() {
  return (
    <div className="grid gap-6">
      <UploadPDF />
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6 text-sm text-slate-300">
        Tip: After upload, go to <span className="font-semibold text-slate-100">Quiz</span> and use the same topic to
        fetch generated questions.
      </div>
    </div>
  );
}

