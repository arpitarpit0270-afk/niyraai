# Niyra AI

A Hindi-first Flask AI assistant with chat, image upload, TXT/PDF summarization, and browser voice input.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="your_google_gemini_key"
python app.py
```

Open <http://localhost:5000>.

## Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `GEMINI_API_KEY` | Yes for AI responses | Demo mode | Google Gemini API key. |
| `GEMINI_TEXT_MODEL` | No | `gemini-1.5-flash` | Text model for chat and summaries. |
| `GEMINI_VISION_MODEL` | No | Same as text model | Vision-capable Gemini model for images. |
| `MAX_UPLOAD_MB` | No | `8` | Upload size limit in MB. |
| `PORT` | No | `5000` | Web server port. |

## Deploy

The included `Procfile` runs the app with Gunicorn:

```bash
web: gunicorn app:app
```
