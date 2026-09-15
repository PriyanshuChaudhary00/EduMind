# EduMind 🧠

EduMind is an AI-powered personalized study assistant that helps you learn smarter. Upload your course materials and notes, and EduMind uses **Retrieval-Augmented Generation (RAG)** and **Google Gemini AI** to let you chat interactively with your documents, ensuring accurate, hallucination-free answers grounded strictly in your study materials.

## ✨ Features
* **Document Management**: Upload lecture slides, PDFs, and Word documents.
* **Vector Search**: Automatically chunks and embeds your documents using `gemini-embedding-2` and stores them in NeonDB with `pgvector`.
* **AI Study Chat**: Ask questions and get intelligent, formatted answers sourced directly from your notes using `gemini-3.5-flash`.
* **Personalized Dashboard**: Track your uploaded documents, study time, and AI interactions.
* *(Coming Soon)* Adaptive Quizzes, Flashcards, and Personalized Study Plans.

## 🚀 Tech Stack
* **Frontend**: Next.js 14, React, TailwindCSS v4, Lucide Icons.
* **Backend**: FastAPI (Python), SQLAlchemy, Pydantic.
* **Database**: NeonDB (Serverless PostgreSQL) with `pgvector` extension.
* **AI / LLMs**: Google GenAI SDK (Gemini Flash & Embeddings).

## 🛠️ Local Development Setup

### 1. Prerequisites
* [Node.js](https://nodejs.org/) (v18+)
* [Python](https://www.python.org/) (3.9+)
* A [NeonDB](https://neon.tech/) PostgreSQL connection string.
* A [Google Gemini API Key](https://aistudio.google.com/).

### 2. Backend Setup
Navigate to the `backend` directory, create a virtual environment, and install dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory and add your credentials:
```env
DATABASE_URL=postgresql://user:password@hostname/dbname?sslmode=require
GEMINI_API_KEY=your_gemini_api_key
```

Start the FastAPI development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*The backend API will be running at `http://localhost:8000`. You can view the interactive API docs at `http://localhost:8000/docs`.*

### 3. Frontend Setup
Open a new terminal, navigate to the `frontend` directory, and install dependencies:

```bash
cd frontend
npm install
```

Start the Next.js development server:
```bash
npm run dev
```
*The web app will be available at `http://localhost:3000`.*

## 🚢 Deployment
* **Backend**: Ready to be deployed on Render using the provided `Dockerfile` and `Procfile`.
* **Frontend**: Optimized for deployment on Vercel. Ensure to set `NEXT_PUBLIC_API_URL` to your production backend URL.
