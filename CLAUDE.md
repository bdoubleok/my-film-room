# CLAUDE.md

## Project Overview

**my-film-room** is a mobile-friendly Streamlit web application for analyzing college football and Madden NFL film room plays. Users upload a CSV of play data and get interactive dashboards showing success rates, scheme efficiency by formation, and play-by-play video review with clip links.

## Tech Stack

- **Python 3** (single-file app)
- **Streamlit** — UI framework (handles page layout, widgets, state)
- **Pandas** — CSV parsing and data manipulation
- **Plotly Express** — interactive bar charts

## Repository Structure

```
my-film-room/
├── app.py              # Entire application (single file, ~127 lines)
├── requirements.txt    # Python dependencies (streamlit, pandas, plotly)
├── stats.csv           # Placeholder data file
├── README.md           # Project readme
└── CLAUDE.md           # This file
```

This is a flat, single-file project. All application logic lives in `app.py`.

## Running the App

```bash
pip install -r requirements.txt
streamlit run app.py
```

No environment variables, database, or external services are required. The app runs entirely in-browser with data uploaded per session.

## How the App Works

1. **CSV Upload** — User uploads a `stats.csv` via `st.file_uploader`
2. **Data Cleaning** — Numeric columns (`Down`, `Distance`, `Yards Gained`) are coerced to proper types; NaN values are filled with safe defaults
3. **Success Calculation** — `check_success()` determines play success based on down:
   - 1st down: gained >= 50% of distance
   - 2nd down: gained >= 70% of distance
   - 3rd/4th down: gained >= 100% of distance
4. **Dashboard Metrics** — Overall success rate, average yards/play, best formation
5. **Formation Chart** — Plotly bar chart of success % by formation
6. **Play-by-Play** — Expandable cards filtered by formation, each showing situation, yards gained, and a video clip link

## Expected CSV Schema

The uploaded CSV must contain these columns:

| Column | Type | Description |
|--------|------|-------------|
| `Formation` | string | Football formation (e.g., "Gun Bunch", "I-Form Pro") |
| `Play Name` | string | Play description (e.g., "Verticals", "Crossers") |
| `Down` | integer | Down number (1-4) |
| `Distance` | numeric | Yards to gain |
| `Yards Gained` | numeric | Actual yards gained on the play |
| `Twitch_Link` | string | URL to video clip of the play |

## Code Conventions

- **Naming**: snake_case for variables and functions; CSV column names are Title Case with spaces
- **Defensive data handling**: Always use `pd.to_numeric(..., errors='coerce')` and `.fillna()` when processing user-uploaded data
- **Safe division**: Use `max(len(df), 1)` to prevent division by zero
- **Streamlit version compatibility**: The `render_link()` function tries `st.link_button()` first, then falls back to HTML markdown, then plain markdown for older Streamlit versions
- **Column access via itertuples**: Use `getattr(r, "Col_Name", getattr(r, "Col Name", ""))` to handle pandas namedtuple field name normalization (spaces become underscores)
- **Page config first**: `st.set_page_config()` must be called before any other Streamlit UI calls

## Key Architecture Decisions

- **No database** — All data is session-scoped via CSV upload; no persistent storage
- **No backend API** — Streamlit handles both frontend and data processing
- **Single-file design** — Intentionally kept simple; all logic in `app.py`
- **No testing infrastructure** — No test framework or test files currently exist
- **No CI/CD** — No GitHub Actions, pre-commit hooks, or automated pipelines
- **Unpinned dependencies** — `requirements.txt` lists packages without version constraints

## Development Guidelines

- Keep the single-file architecture unless complexity demands splitting
- `st.set_page_config()` must remain as the first Streamlit call in the file
- Preserve the defensive data handling patterns (type coercion, NaN filling, safe division)
- Maintain backward compatibility with older Streamlit versions in `render_link()`
- Use `st.stop()` to halt execution early when data is missing or invalid
- Emojis are used intentionally in the UI for visual feedback (success/failure indicators, warnings)
