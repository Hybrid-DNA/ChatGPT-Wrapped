# ChatGPT Wrapped (Streamlit)

A simple, modern "year-in-review" style dashboard for your ChatGPT conversations.

## What it does
- Accepts a **ChatGPT data export** `conversations.json` (or the export `.zip`).
- Builds a "Wrapped" style report: activity, categories, token counts, highlights, and an archetype title.
- Lets users download:
  - Per-message CSV
  - Per-conversation CSV
  - Summary JSON
  - A shareable HTML "Wrapped" report (single file)

## Privacy
This app processes the uploaded file in memory on the machine/server running Streamlit.
If you deploy it publicly, users are uploading their data to your server.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Input file
Download your ChatGPT data export from ChatGPT settings and either:
- upload the export `.zip`, or
- upload `conversations.json` from inside the export.

## Notes on token counts
ChatGPT exports do **not** include official token counts.
This app uses a lightweight heuristic to estimate tokens directly from the message text.

## Project structure
- `app.py` Streamlit UI
- `src/parse_export.py` robust parser for `conversations.json`
- `src/categorise.py` message category rules (10 buckets)
- `src/analytics.py` metrics and aggregations
- `src/archetypes.py` title assignment
- `src/report_export.py` generates a shareable HTML report
- `src/tokens.py` token estimation helpers

## Licence
MIT
