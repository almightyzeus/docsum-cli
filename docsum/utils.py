import os
import tiktoken

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}

def is_supported_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in SUPPORTED_EXTENSIONS

def split_text_into_chunks(text: str, max_tokens: int = 1000, encoding_model: str = "gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(encoding_model)
    chunks = []
    current_words = []
    for word in text.split():
        current_words.append(word)
        if len(encoding.encode(" ".join(current_words))) > max_tokens:
            chunks.append(" ".join(current_words))
            current_words = []
    if current_words:
        chunks.append(" ".join(current_words))
    return chunks
