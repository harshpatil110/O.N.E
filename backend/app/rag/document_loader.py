import os
import re
import yaml
import logging
from typing import Any, Tuple, List, Dict

logger = logging.getLogger(__name__)

def parse_markdown_file(filepath: str, relative_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Reads a markdown file, extracts YAML front-matter if present,
    and returns a tuple of (content_text, metadata_dict).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception as e:
        logger.error(f"Failed to read file {filepath}: {str(e)}")
        return "", {}

    # Regex to find YAML front-matter between '---'
    match = re.match(r"^---\n(.*?)\n---\n", raw, re.DOTALL)
    
    metadata: Dict[str, Any] = {}
    content = raw
    
    if match:
        front_matter_str = match.group(1)
        try:
            parsed_yaml = yaml.safe_load(front_matter_str)
            if isinstance(parsed_yaml, dict):
                metadata = parsed_yaml
        except yaml.YAMLError as e:
            logger.warning(f"Error parsing YAML front-matter in {filepath}: {str(e)}")
        
        # Remove the front-matter from the content body
        content = raw[match.end():]
        
    metadata["source"] = relative_path
    
    return content.strip(), metadata

def load_knowledge_base(kb_directory: str) -> List[Dict[str, Any]]:
    """
    Walk the knowledge_base/ directory, read all .md files,
    parse YAML front-matter, and return list of document dicts.
    """
    documents = []
    if not os.path.exists(kb_directory):
        logger.warning(f"Knowledge base directory {kb_directory} does not exist.")
        return []

    for root, _, files in os.walk(kb_directory):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, kb_directory)
                
                # Normalize relative paths to use forward slash
                relative_path = relative_path.replace("\\", "/")

                content, metadata = parse_markdown_file(filepath, relative_path)
                if content:
                    documents.append({"content": content, "metadata": metadata})
    return documents
