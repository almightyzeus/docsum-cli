from docsum.cli import summarize_file
from docsum.summarize import Summarizer

# requires OPENAI_API_KEY in env
summarizer = Summarizer()
print(summarize_file("sample.pdf", summarizer, max_tokens=800))
