#!/usr/bin/env python3

"""
AI Chat → Project JSON Converter

Purpose:
Convert raw copied AI/software-engineering chats into structured JSON
usable for:
- project reconstruction
- RAG ingestion
- fine-tuning datasets
- prompt engineering pipelines
- debugging archives

Features:
- Uses OpenAI-compatible API
- Handles huge chats via chunking
- Preserves code/errors/commands
- Outputs structured project JSON
- Merges chunk results automatically

Usage:
    python project_chat_converter.py raw_chat.txt output.json

Install:
    pip install openai

Environment:
    export OPENAI_API_KEY="YOUR-API-KEY-HERE"

Optional:
    export OPENAI_BASE_URL="https://api.openai.com/v1"
"""

import os
import re
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any

from openai import OpenAI


# =========================================================
# CONFIG
# =========================================================

MODEL = "gpt-5-mini"

# Safe chunk size
MAX_CHARS = 12000

# Delay between requests
REQUEST_DELAY = 1


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = r"""
You are a dataset normalization engine.

Your task:
Convert raw copied AI conversations into structured JSON suitable
for reconstructing software engineering projects.

CRITICAL RULES:
- Do NOT summarize
- Do NOT shorten
- Preserve technical details exactly
- Preserve code blocks exactly
- Preserve indentation
- Preserve shell commands exactly
- Preserve architecture reasoning
- Preserve filenames
- Preserve stack traces
- Preserve dependency names
- Preserve API endpoints
- Preserve chronological debugging flow

Return ONLY valid JSON.

OUTPUT FORMAT:

{
  "project_context": {
    "title": "",
    "technologies": [],
    "summary": ""
  },
  "messages": [
    {
      "role": "user",
      "content": ""
    },
    {
      "role": "assistant",
      "content": ""
    }
  ],
  "artifacts": {
    "files": [],
    "commands": [],
    "dependencies": [],
    "errors": [],
    "routes": [],
    "env_vars": []
  }
}

RULES:
- Never invent data
- Never repair broken code
- Never explain
- Never add markdown
- Output valid JSON only
"""


# =========================================================
# CLIENT
# =========================================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)


# =========================================================
# HELPERS
# =========================================================

def chunk_text(text: str, max_chars: int = MAX_CHARS) -> List[str]:
    """
    Split huge chat into manageable chunks.
    """

    chunks = []

    start = 0

    while start < len(text):
        end = start + max_chars

        if end >= len(text):
            chunks.append(text[start:])
            break

        split_pos = text.rfind("\n", start, end)

        if split_pos == -1:
            split_pos = end

        chunks.append(text[start:split_pos])

        start = split_pos

    return chunks


def safe_json_loads(content: str) -> Dict[str, Any]:
    """
    Attempt to safely parse JSON.
    """

    content = content.strip()

    # Remove accidental markdown fences
    content = re.sub(r"^```json", "", content)
    content = re.sub(r"^```", "", content)
    content = re.sub(r"```$", "", content)

    return json.loads(content)


def unique_extend(target: List, values: List):
    """
    Extend without duplicates.
    """

    existing = set(map(str, target))

    for item in values:
        if str(item) not in existing:
            target.append(item)
            existing.add(str(item))


def merge_results(base: Dict, new: Dict):
    """
    Merge chunk outputs together.
    """

    # Messages
    base["messages"].extend(new.get("messages", []))

    # Technologies
    unique_extend(
        base["project_context"]["technologies"],
        new.get("project_context", {}).get("technologies", [])
    )

    # Artifacts
    for key in base["artifacts"]:
        unique_extend(
            base["artifacts"][key],
            new.get("artifacts", {}).get(key, [])
        )


def ask_model(raw_chunk: str) -> Dict[str, Any]:
    """
    Send chunk to model.
    """

    response = client.chat.completions.create(
    model=MODEL,
    messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": raw_chunk
            }
        ]
    )

    content = response.choices[0].message.content

    return safe_json_loads(content)


def initialize_output() -> Dict[str, Any]:
    """
    Create empty output structure.
    """

    return {
        "project_context": {
            "title": "",
            "technologies": [],
            "summary": ""
        },
        "messages": [],
        "artifacts": {
            "files": [],
            "commands": [],
            "dependencies": [],
            "errors": [],
            "routes": [],
            "env_vars": []
        }
    }


# =========================================================
# MAIN
# =========================================================

def main():

    if len(sys.argv) < 3:
        print(
            "Usage:\n"
            "python project_chat_converter.py raw_chat.txt output.json"
        )
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"[!] File not found: {input_path}")
        sys.exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("[!] OPENAI_API_KEY not set")
        sys.exit(1)

    raw_text = input_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    chunks = chunk_text(raw_text)

    print(f"[+] Total chunks: {len(chunks)}")

    final_output = initialize_output()

    for idx, chunk in enumerate(chunks, start=1):

        print(f"[+] Processing chunk {idx}/{len(chunks)}")

        try:

            result = ask_model(chunk)

            merge_results(final_output, result)

            print(f"[+] Chunk {idx} complete")

        except Exception as e:

            print(f"[!] Chunk {idx} failed")
            print(e)

        time.sleep(REQUEST_DELAY)

    # Auto title if missing
    if not final_output["project_context"]["title"]:
        final_output["project_context"]["title"] = (
            input_path.stem.replace("_", " ").title()
        )

    # Auto summary
    if not final_output["project_context"]["summary"]:
        final_output["project_context"]["summary"] = (
            f"Recovered project conversation with "
            f"{len(final_output['messages'])} messages."
        )

    # Save final JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            final_output,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"[+] Saved JSON to: {output_path}")

    print(f"[+] Messages: {len(final_output['messages'])}")

    print(
        f"[+] Dependencies: "
        f"{len(final_output['artifacts']['dependencies'])}"
    )

    print(
        f"[+] Commands: "
        f"{len(final_output['artifacts']['commands'])}"
    )

    print(
        f"[+] Errors: "
        f"{len(final_output['artifacts']['errors'])}"
    )


if __name__ == "__main__":
    main()
