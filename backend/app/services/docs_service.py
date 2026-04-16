import os
from pathlib import Path

# We resolve the absolute path to the knowledge base to ensure safe path operations
KNOWLEDGE_BASE_DIR = Path("c:/Users/harsh/Desktop/Coding/ONE/backend/knowledge_base").resolve()

def _is_safe_path(requested_path: Path) -> bool:
    """Verifies that the requested path sits entirely within KNOWLEDGE_BASE_DIR to prevent directory traversal."""
    try:
        resolved_path = requested_path.resolve()
        common = os.path.commonpath([str(resolved_path), str(KNOWLEDGE_BASE_DIR)])
        return common == str(KNOWLEDGE_BASE_DIR)
    except Exception:
        return False

def get_all_docs() -> list:
    """
    Scans the knowledge_base folder, parses Markdown files, extracts
    a title, an excerpt, and groups them into mock categories.
    """
    if not KNOWLEDGE_BASE_DIR.exists():
        return []

    categories = ["Setup Guides", "Architecture", "Troubleshooting", "General"]
    docs_by_category = {cat: [] for cat in categories}
    
    for md_file in KNOWLEDGE_BASE_DIR.glob("**/*.md"):
        if not _is_safe_path(md_file):
            continue
            
        title = md_file.stem.replace('-', ' ').title()
        excerpt = ""
        
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content_lines = []
                for line in f:
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue
                    # First # heading becomes title
                    if stripped_line.startswith("# ") and title == md_file.stem.replace('-', ' ').title():
                        title = stripped_line[2:].strip()
                    elif not stripped_line.startswith("#"):
                        content_lines.append(stripped_line)
                    
                    if len(content_lines) >= 3:
                        break
                
                if content_lines:
                    excerpt = " ".join(content_lines)
                    excerpt = excerpt[:120] + "..." if len(excerpt) > 120 else excerpt
        except Exception:
            pass # fallback to defaults if unreadable
            
        # Group deterministically based on file name so categories are stable
        cat_index = sum(ord(c) for c in md_file.name) % len(categories)
        deterministic_category = categories[cat_index]
        
        rel_path = md_file.relative_to(KNOWLEDGE_BASE_DIR)
        docs_by_category[deterministic_category].append({
            "id": str(rel_path).replace("\\", "/"),
            "title": title,
            "excerpt": excerpt,
            "filename": str(rel_path).replace("\\", "/") # standardized for URL
        })
        
    return [{"category": k, "articles": v} for k, v in docs_by_category.items() if v]

def get_doc_content(filename: str) -> str:
    """Read and return the raw Markdown text of a specific file."""
    # Build complete path
    target_path = KNOWLEDGE_BASE_DIR / filename
    
    # Security checks (path traversal and file extension limits)
    if not _is_safe_path(target_path):
        raise ValueError("Access Denied: Unsafe path access detected.")
        
    if not target_path.exists() or not target_path.is_file():
        raise FileNotFoundError(f"Markdown file '{filename}' not found in the knowledge base.")
        
    if target_path.suffix.lower() != '.md':
        raise ValueError("Access Denied: Only markdown (.md) documents are allowed.")
        
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()
