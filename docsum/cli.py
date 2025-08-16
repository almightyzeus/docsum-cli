#!/usr/bin/env python3
import os
import sys
import argparse
from dotenv import load_dotenv

from .summarize import Summarizer
from .utils import split_text_into_chunks, is_supported_file
from .readers import extract_text_from_pdf, extract_text_from_txt, extract_text_from_docx
from .utils import SUPPORTED_EXTENSIONS

load_dotenv()  # allow .env files

def read_text_by_ext(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext == ".txt":
        return extract_text_from_txt(path)
    elif ext == ".docx":
        return extract_text_from_docx(path)
    raise ValueError(f"Unsupported file type: {ext}")


def build_parser():
    p = argparse.ArgumentParser(prog="docsum", description="Summarize documents or folders using OpenAI models.")
    p.add_argument("path", help="Path to a file or a folder.")
    p.add_argument("--output", "-o", help="Output file (for single file) or directory (for folder).")
    p.add_argument("--model", "-m", help="Model name (overrides DOCUMENT_SUMMARIZER_MODEL env).")
    p.add_argument("--max-tokens", type=int, default=1000, help="Max tokens per chunk before calling the model.")
    return p

def summarize_file(path: str, summarizer: Summarizer, max_tokens: int) -> str:
    text = read_text_by_ext(path)
    chunks = split_text_into_chunks(text, max_tokens=max_tokens)
    return summarizer.summarize_chunks(chunks)

def summarize_folder(folder_path, summarizer, max_tokens, output_dir=None):
    """Summarize all supported files in a folder."""
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            ext = os.path.splitext(file_name)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file_name)
                print(f"\n📄 Processing {file_path} ...")
                try:
                    text = read_text_by_ext(file_path)
                    chunks = split_text_into_chunks(text, max_tokens=max_tokens)
                    summary = summarizer.summarize_chunks(chunks)
                except ValueError as e:
                    print(f"❌ Could not summarize file: {file_path}\n    Reason: {e}", file=sys.stderr)
                    continue

                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                    out_file = os.path.join(
                        output_dir, f"{os.path.splitext(file_name)[0]}.summary.txt"
                    )
                    with open(out_file, "w", encoding="utf-8") as f:
                        f.write(summary)
                    print(f"✅ Saved: {out_file}")
                else:
                    print(summary)


def main():
    args = build_parser().parse_args()
    model = args.model or os.getenv("DOCUMENT_SUMMARIZER_MODEL") or "gpt-4o"
    summarizer = Summarizer(model=model)

    if os.path.isdir(args.path):
        out_dir = args.output or os.path.join(args.path, "summaries")
        summarize_folder(args.path, summarizer, args.max_tokens, out_dir)
        return

    if not os.path.isfile(args.path):
        print(f"Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    if not is_supported_file(args.path):
        print("Unsupported file type. Currently supported: .pdf,.docx,.txt", file=sys.stderr)
        sys.exit(2)

    try:
        summary = summarize_file(args.path, summarizer, args.max_tokens)
    except ValueError as e:
        print(f"❌ Could not summarize file: {args.path}\n    Reason: {e}", file=sys.stderr)
        sys.exit(3)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"✓ Summary saved to {args.output}")
    else:
        print("\n--- Summary ---\n")
        print(summary)

if __name__ == "__main__":
    main()
