# O.N.E Knowledge Base

Welcome to the internal engineering Knowledge Base! This folder stores all critical documentation covering the company's technical architecture, developer setup procedures, security compliance, and engineering cultural guidelines. 

This repository of documents serves as the source of truth not only for human engineers but also for the **O.N.E Autonomous Agent**, our internal AI bot which actively scrapes, chunks, and vectorizes these documents into an integrated ChromaDB. This allows developers to query the agent for contextual, rule-based engineering answers.

## How to Add a New Document
The knowledge base continuously evolves. If you architect a new system or overhaul a compliance process, you must document it here.

1. Create a new markdown (`.md`) file in the appropriate technical subdirectory (e.g., `setup/`, `engineering/`, `devops/`, `compliance/`).
2. Add the mandatory YAML Front-Matter Block.
3. Write substantive, accurate, and professional content without placeholder text. 
4. Submit a Pull Request targeting the `main` branch.

## Strict Document Naming Conventions
All files within the knowledge base must adhere strictly to the **kebab-case** naming paradigm. This simplifies our URL parsing rules for the agent interface.
- **Valid:** `api-design-guidelines.md`, `local-dev-python.md`
- **Invalid:** `API_design_guidelines.md`, `localDevPython.md`, `local dev python.md`

## Required YAML Front-Matter Fields
Every document within the subdirectories MUST begin with a standardized YAML front-matter header. The RAG ingestion pipeline strictly requires this metadata to filter vectors optimally. Documents lacking this header will throw an assertion error in CI/CD.

A valid front-matter header must contain:
```yaml
---
title: "The Human-Readable Document Title"
category: "setup | engineering | devops | compliance | team"
applicable_roles: ["backend", "frontend", "fullstack", "devops", "data", "all"]
applicable_stacks: ["python", "node", "all"]
applicable_levels: ["intern", "junior", "mid", "senior", "staff"]
last_updated: "YYYY-MM-DD"
---
```

## Triggering ChromaDB Re-Ingestion
Because the O.N.E RAG pipeline relies on static vector embeddings, updating a document requires the system to regenerate chunk embeddings.
1. Once your PR is merged into the `main` branch, an automated GitHub Action will trigger.
2. The pipeline fires a webhook referencing the `backend/rag/ingest.py` script.
3. The script sweeps the entire `knowledge_base/` tree, parses the markdown, evaluates the front-matter payloads, recalculates the specialized embeddings (via Nvidia NV-EmbedQA), and updates the persistent `chroma_db/` disk configuration natively.

If you are running the agent locally and need to force the re-ingestion, execute the following from the root `backend` directory:
```bash
python -m app.rag.ingest --force-refresh
```
