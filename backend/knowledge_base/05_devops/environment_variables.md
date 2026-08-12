# Environment Variables Reference

## Backend `.env` Template
```env
# ─── LLM Provider ───
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxx
NVIDIA_MODEL_NAME=Qwen/Qwen3.5-397b-a17b

# ─── Database ───
DATABASE_URL=postgresql://postgres:<password>@db.<ref>.supabase.co:5432/postgres

# ─── JWT Auth ───
JWT_SECRET_KEY=<64-char-hex-string>
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=480

# ─── Email (SMTP) ───
GMAIL_ADDRESS=notifications@nexusai.dev
GMAIL_APP_PASSWORD=<app-password>

# ─── HR Configuration ───
HR_EMAIL=hr@nexusai.dev

# ─── ChromaDB ───
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=one_knowledge_base

# ─── App Config ───
APP_ENV=development
FRONTEND_URL=http://localhost:5173
```

## Frontend `.env` Template
```env
VITE_API_URL=http://localhost:8000
```

## Security Rules
* **Never** commit `.env` files to Git. Verify `.gitignore` includes
  `.env` and `.env.*`.
* Rotate `JWT_SECRET_KEY` quarterly.
* Use **GitHub Secrets** for CI/CD environment variables.
* Use separate Supabase projects for `development`, `staging`, and
  `production`.

---
*Security: Harshvardhan Patil*
