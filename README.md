# YouTube Downloader GUI & API

This project offers a **multi-interface YouTube downloader** with both:

- **Desktop GUI** (Tkinter + CustomTkinter)
- **Web Server API** using FastAPI + Bootstrap frontend

---

## Features

### Desktop GUI
- Modern Tkinter UI with custom widgets
- URL input with playlist & subtitles options
- Format selection (video/mp4 or audio/mp3)
- Download quality choice
- Folder selection for downloads
- Progress bar with speed, size, ETA
- Cancel download capability
- Rich logging window

### FastAPI Backend + Web UI
- REST API `/download` POST endpoint
- Accepts URL, format, playlist, subtitles, destination, quality
- Returns JSON success/error
- Serves static HTML (`index.html`) with Bootstrap
- Simple web page for initiating downloads
- Easily extendable for more frontend features

### Core Downloader (Shared)
- Unified downloader logic using `yt_dlp` in `downloader.py`
- Supports video/audio, subtitles, playlists
- Commonly used by both web and desktop interfaces

---

## Architecture

```
[ User ]
   |                     [ Desktop GUI ]
   |----------------------------|
   |                            | calls
[ Web Frontend ] ------> [ FastAPI API ] ----
                              |             |
                     calls downloader.py   |
                              |             |
                        Uses yt_dlp        |
                                           |
                          Shared core downloader
```

---

## Quick Start Instructions

### 1. Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

### 2. Using Desktop App

```bash
python main.py
```

### 3. Running API + Web Interface

```bash
python app.py
# or
uvicorn app:app --reload
```

- Then navigate to: [http://localhost:8000](http://localhost:8000)

---

## API Endpoint

### POST `/download`

**Request JSON:**

```json
{
  "url": "https://youtube.com/...",
  "format": "mp4" | "mp3",
  "playlist": true | false,
  "subtitles": true | false,
  "destination": "/path/to/download",
  "quality": "best" | "720p" | "480p"
}
```

**Response:**

```json
{
  "status": "success" | "error",
  "message": "Download completed!" | "Error details"
}
```

---

## Customization & Suggestions

- Add async job support (Celery + Redis recommended)
- Real-time progress feedback via WebSockets or SSE
- HTMX integration for richer web frontend updates
- Centralize configuration using `.env` or `config.yaml`
- Testing: Add unit & API tests
- Containerize with Docker
- Harden security & input validation

---

## Dependencies (from `requirements.txt`)
- fastapi
- uvicorn
- yt-dlp
- customtkinter
- tk

---

## License
MIT License

---

## Authors
Auto-generated and developed as a SPARC AI project bootstrap