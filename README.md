# ShareChat Trending Tags MVP

A FastAPI-based MVP that fetches live India trends from Google Trends RSS, converts them into ranked trend tags, and shows them in a mobile-style clickable UI.

## Live App
`https://python-backend--vibecoder992.replit.app/app`

## Features
- Live India trend fetch from Google Trends RSS
- Tag normalization into hashtag-style labels
- Rule-based categorization
- Approx traffic extraction
- Heat score labeling
- Mobile-style feed UI
- Clickable detail view

## API
- `/` → health/root
- `/trending-tags` → JSON trends response
- `/app` → UI

## Tech Stack
- FastAPI
- Python
- Requests
- XML parsing
- Simple HTML/CSS/JS frontend

## Project Structure
- `main.py`
- `services/trend_service.py`
- `utils/categorizer.py`
- `utils/normalizer.py`
- `schemas/trend_schema.py`

## Limitations
- Uses a single live source
- Category inference is rule-based and imperfect
- Current feed snapshot returns around 10 live items
- No long-window aggregation yet

## Next Improvements
- Better multilingual categorization
- Multi-source aggregation
- Full-day trend persistence
- Improved ranking logic
