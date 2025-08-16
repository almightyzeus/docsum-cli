# docsum — Document Summarizer CLI

A pip-installable CLI tool to **summarize documents** using OpenAI models.  
Currently supports **PDF**, **DOCX**, and **TXT** files — either individually or in bulk from a folder.

## ✨ Features
- Summarizes a **single file** or **all supported files in a folder**
- Supports `.pdf`, `.docx`, `.txt`
- Token-aware chunking for large documents
- Retries on transient API errors (rate limits, timeouts)
- Configurable OpenAI model via:
  - CLI flag `--model`
  - Environment variable `DOCUMENT_SUMMARIZER_MODEL`
- `.env` file support for storing your API key
- Output either to terminal or saved as `.txt` files

---

## 📦 Installation

Clone and install locally in editable mode:

```bash
git clone https://github.com/almightyzeus/docsum-cli.git
cd docsum
python -m venv venv && source venv/bin/activate
cd ..
pip install -e .
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/almightyzeus/docsum-cli.git
```

---

## ⚙️ Requirements

Set your **OpenAI API key**:

```bash
export OPENAI_API_KEY="sk-..."
```

Optionally set a default model:

```bash
export DOCUMENT_SUMMARIZER_MODEL="gpt-4o"
```

You can also create a `.env` file inside the `docsum` folder:

```env
OPENAI_API_KEY=sk-...
DOCUMENT_SUMMARIZER_MODEL=gpt-4o
```

---

## 🚀 Usage

### Summarize a single document
```bash
docsum myfile.pdf
docsum myfile.docx
docsum myfile.txt
```

### Save summary to a file
```bash
docsum myfile.pdf -o summary.txt
```

### Summarize all supported files in a folder
Outputs `.summary.txt` files into `summaries/` by default:
```bash
docsum ./my_docs
```

### Summarize folder with custom output directory
```bash
docsum ./my_docs -o ./summaries_out
```

### Override model at runtime
```bash
docsum report.pdf --model gpt-3.5-turbo
```

### Adjust chunk size
```bash
docsum large.pdf --max-tokens 800
```

---

## 📂 Supported Formats
- `.pdf`
- `.docx`
- `.txt`

Support for `.md`, `.rtf`, and other formats can be added easily —  
check `docsum/readers.py` and `docsum/utils.py` to extend.

---

## 🛠 Development
- CLI entry point: `docsum/cli.py`
- Document readers: `docsum/readers.py`
- Summarization logic: `docsum/summarize.py`
- Token chunking utilities: `docsum/utils.py`

Run example:
```bash
python examples/example_usage.py
```

---

## 📜 License
MIT License — see [LICENSE](LICENSE) for details.
