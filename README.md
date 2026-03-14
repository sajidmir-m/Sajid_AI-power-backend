## Mini Content Ingestion + Adaptive Quiz Engine

Full-stack prototype that ingests educational PDFs, chunks extracted text, generates quizzes with an LLM, and serves them via APIs to a minimal Next.js frontend.

### Architecture (high level)

- **Frontend (Next.js + Tailwind)**  
  Pages: Upload PDF → Quiz flow. Uses Axios to call the backend.

- **Backend (FastAPI)**  
  - `POST /ingest`: PDF upload → PyMuPDF extract → clean → chunk (150–300 words) → store in Postgres (Supabase) → optionally generate questions via LLM.
  - `GET /quiz`: fetch questions by topic + difficulty; can auto-generate if none exist yet.
  - `POST /submit-answer`: validates answer, stores response, returns correct/incorrect + next recommended difficulty.

- **Database (Supabase Postgres + SQLAlchemy)**  
  Tables: `source_documents`, `content_chunks`, `quiz_questions`, `student_answers`.

### “Diagram” explanation (request/flow)

1. **Upload**: Next.js → `POST /ingest` (multipart/form-data)
2. **Ingestion**: FastAPI → PyMuPDF → Chunker → Supabase Postgres
3. **Quiz generation**: FastAPI → LLM provider (`GeminiQuizProvider`) → validate JSON → store questions
4. **Quiz delivery**: Next.js → `GET /quiz?topic=...&difficulty=...`
5. **Answering**: Next.js → `POST /submit-answer` → SQLite → adaptive difficulty recommendation

### Backend setup

From project root:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Create an env file for the backend:

- Copy `env.example` to `backend/.env` (Cursor may hide dotfiles in this workspace, but the backend expects `.env`).
- In your Supabase dashboard, go to **Project settings → Database → Connection strings → SQLAlchemy** and copy that URL into `DATABASE_URL`.
- Set `GEMINI_API_KEY` and (optionally) `GEMINI_MODEL`.

Run the backend:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Backend docs:
- Swagger UI: `http://localhost:8000/docs`

### Database migrations (Alembic)

This project uses **Alembic** for schema migrations, pointed at your Supabase Postgres database.

- The Alembic config lives in `alembic.ini` and `backend/migrations/`.
- The initial schema migration is `backend/migrations/versions/0001_initial_schema.py`.

To create the schema in your Supabase database:

```bash
alembic upgrade head
```

To create a new migration after changing models:

```bash
alembic revision -m "describe change" --autogenerate
alembic upgrade head
```

Alembic reads `DATABASE_URL` from your environment (the same value used by the app).

### Frontend setup

From `frontend/`:

```bash
npm install
npm run dev
```

Frontend env:
- Copy `frontend/env.local.example` to `frontend/.env.local`
- Set `NEXT_PUBLIC_API_BASE_URL` (default is `http://localhost:8000`)

Open:
- `http://localhost:3000`

### Testing APIs (examples)

#### 1) Ingest a PDF

```bash
curl -X POST "http://localhost:8000/ingest" ^
  -F "grade=3" ^
  -F "subject=Science" ^
  -F "topic=Plants" ^
  -F "generate_quiz=true" ^
  -F "file=@sample.pdf;type=application/pdf"
```

Example response:

```json
{
  "source_document": {
    "id": 1,
    "filename": "sample.pdf",
    "grade": 3,
    "subject": "Science",
    "created_at": "2026-03-14T12:34:56.000000"
  },
  "source_id": "SRC_001",
  "chunks_stored": 4
}
```

#### 2) Fetch quiz questions

```bash
curl "http://localhost:8000/quiz?topic=Plants&difficulty=easy&limit=5"
```

Example response:

```json
{
  "topic": "Plants",
  "difficulty": "easy",
  "questions": [
    {
      "id": 12,
      "question_id": "Q12",
      "question": "Which resource do plants need to grow?",
      "type": "MCQ",
      "options": ["Sunlight", "Plastic", "Metal", "Sand"],
      "difficulty": "easy",
      "source_chunk_id": "SRC_001_CH_01"
    }
  ]
}
```

#### 3) Submit an answer (adaptive difficulty)

```bash
curl -X POST "http://localhost:8000/submit-answer" ^
  -H "Content-Type: application/json" ^
  -d "{\"student_id\":\"S001\",\"question_id\":\"Q12\",\"selected_answer\":\"Sunlight\",\"current_difficulty\":\"easy\"}"
```

Example response:

```json
{
  "is_correct": true,
  "correct_answer": "Sunlight",
  "recommended_difficulty": "medium",
  "explanation": null,
  "stored_answer_id": 1
}
```

### Notes / extensibility

- **Swap LLM provider**: implement the `LLMProvider` protocol in `backend/app/services/llm_service.py` and update `get_llm_provider()`.
- **Traceability**: every generated question includes `source_chunk_id` that maps back to a stored chunk.
- **Hallucination minimization**: prompts instruct “use only provided text”; responses are validated as JSON with Pydantic.

