import os
import time
from typing import Optional, List
from openai import OpenAI

DEFAULT_MODEL = os.getenv("DOCUMENT_SUMMARIZER_MODEL", "gpt-4o")

class Summarizer:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set. Set env var or pass api_key.")
        self.client = OpenAI(api_key=api_key)
        self.model = model or DEFAULT_MODEL

    def summarize_chunk(self, text_chunk: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a concise, faithful document summarizer. Capture key points, structure, and any action items."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text_chunk}"}
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()


    def summarize_with_retries(self, text_chunk: str, retries: int = 3, backoff_sec: int = 8) -> str:
        for attempt in range(retries):
            try:
                return self.summarize_chunk(text_chunk)
            except Exception as e:
                if attempt == retries - 1:
                    raise
                time.sleep(backoff_sec * (attempt + 1))

    def summarize_chunks(self, chunks: List[str]) -> str:
        parts = []
        for idx, ch in enumerate(chunks, 1):
            print(f"Summarizing chunk {idx}/{len(chunks)}...")
            parts.append(self.summarize_with_retries(ch))
        # optional second-pass synthesis if there are multiple chunks
        if len(parts) == 1:
            return parts[0]
        joined = "\n\n".join(f"- {p}" for p in parts)
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Synthesize multiple partial summaries into one cohesive, non-redundant summary with headings and bullets."},
                {"role": "user", "content": f"Combine these partial summaries into one coherent summary:\n{joined}"}
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
