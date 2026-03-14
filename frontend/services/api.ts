import axios from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export type Difficulty = "easy" | "medium" | "hard";
export type QuestionType = "MCQ" | "TF" | "FIB";

export type QuizQuestion = {
  id: number;
  question_id: string;
  question: string;
  type: QuestionType;
  options: string[] | null;
  difficulty: Difficulty;
  source_chunk_id: string;
};

export async function uploadPDF(params: {
  file: File;
  grade: number;
  subject: string;
  topic: string;
  generate_quiz?: boolean;
}) {
  const form = new FormData();
  form.append("file", params.file);
  form.append("grade", String(params.grade));
  form.append("subject", params.subject);
  form.append("topic", params.topic);
  form.append("generate_quiz", String(params.generate_quiz ?? true));

  const res = await axios.post(`${BASE_URL}/ingest`, form, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return res.data as {
    source_id: string;
    chunks_stored: number;
    source_document: { id: number; filename: string; grade: number; subject: string; created_at: string };
  };
}

export async function getQuiz(params: { topic: string; difficulty: Difficulty; limit?: number; auto_generate?: boolean }) {
  const res = await axios.get(`${BASE_URL}/quiz`, {
    params: {
      topic: params.topic,
      difficulty: params.difficulty,
      limit: params.limit ?? 5,
      auto_generate: params.auto_generate ?? true
    }
  });
  return res.data as { topic: string; difficulty: Difficulty; questions: QuizQuestion[] };
}

export async function submitAnswer(params: {
  student_id: string;
  question_id: string;
  selected_answer: string;
  current_difficulty: Difficulty;
}) {
  const res = await axios.post(`${BASE_URL}/submit-answer`, params);
  return res.data as {
    is_correct: boolean;
    correct_answer: string;
    recommended_difficulty: Difficulty;
    stored_answer_id: number;
  };
}

