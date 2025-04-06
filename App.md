# YouTube Downloader GUI Project Overview

## Project Summary
This repository provides a multi-interface YouTube video and audio downloader built primarily using Python, FastAPI, and Tkinter (with `customtkinter`). It supports both a **web-based interface** via FastAPI and an **advanced desktop GUI app**.

---

## Architecture & Key Components

### 1. **FastAPI Web Backend (`app.py`)**
- Exposes a simple REST API with a `/download` POST endpoint accepting JSON payloads including URL, format, playlist, subtitles, and destination.
- Serves a static HTML page (`/static/index.html`), built with Bootstrap, containing a form for input.
- Utilizes `yt_dlp` for downloading videos or audio from YouTube with optional playlist and subtitle features.
- Handles errors gracefully, providing JSON responses with status.

### 2. **Web Frontend (`index.html`)**
- Responsive UI using Bootstrap 4 with input fields:
  - YouTube URL
  - Destination folder
  - Format (video/mp4 or audio/mp3)
  - Playlist toggle
  - Subtitles toggle
- Submits fetch POST requests to the FastAPI endpoint.
- Displays download status and simulates progress.

### 3. **Desktop GUI (`main.py`)**
- Built using `customtkinter`, modernizing Tkinter's appearance.
- Features include:
  - URL input
  - Format selection (Video/Audio)
  - Playlist and subtitles toggles
  - Download quality selection
  - Destination folder browsing
  - Real-time download progress bar, speed, size, ETA
  - Threaded downloads for UI responsiveness
  - Cancellation support during download
  - Extensive log window
- Uses `yt_dlp` internally, similar download options to FastAPI.

### 4. **Desktop Entry (`ytdownloader.desktop`)**
- Freedesktop `.desktop` launcher pointing to the Python GUI,
- for easy integration into Linux menus.

---

## Technologies Used
- **Backend:** Python, FastAPI, `yt_dlp`
- **Frontend Web:** HTML, Bootstrap, JavaScript Fetch API
- **Desktop GUI:** Python, Tkinter + `customtkinter`
- **Packaging:** Freedesktop `.desktop` integration.

---

## High-Level Flow
- **Web Mode:** User visits the page, enters data → sends POST to `/download` → backend triggers `yt_dlp` download → response sent back → frontend displays status.
- **Desktop GUI Mode:** User enters data in GUI → clicks download → threaded function calls `yt_dlp` → progress shown live → cancellation possible.

---

## Observations & Potential Improvements
- **Unified Backend**: Currently, both the FastAPI app and the Tk GUI have similar but duplicate configurations for `yt_dlp` options. Refactor core download logic into a separate module to avoid duplication.
- **Progress Reporting for API:** The REST API currently returns after completion — implementing real-time progress endpoints via WebSockets or Server-Sent Events would enhance UX.
- **Async Downloads:** Use Celery + message queue for background processing in web mode, allowing queueing multiple jobs.
- **HTMX Integration:** Replace fetch with HTMX to streamline dynamic updates and states in the web UI.
- **Settings Config File:** Use a config file (YAML, JSON, or environment variables) to standardize default download paths, formats, etc.
- **Dockerization:** Provide Docker setup to simplify deployment.
- **Installer:** Create cross-platform installers or packages.
- **Tests:** Add unit tests, especially for download functions, and API integration tests.
- **Security:** Validate inputs more rigorously (URLs, destination paths), limit filesystem access, sanitize user input.
- **Logging:** Add structured logging in backend and GUI for troubleshooting.
- **GUI Polish:**
  - Show download speed graph
  - Pause/resume capability
  - History of downloads
  - Dark/light mode toggle if not present
  - Multi-thread batch download options

---

## Summary Table
| Component          | Description                                      |
|-------------------|--------------------------------------------------|
| `app.py`          | FastAPI backend serving static files & downloads |
| `index.html`      | Bootstrap web frontend                          |
| `main.py`         | Tkinter-based desktop app                       |
| `ytdownloader.desktop` | Linux desktop launcher                     |

---

## Goal
A multiplatform YouTube downloader that works both via browser and as a desktop program, prioritizing user-friendly interfaces and reliable download experience.

---

## Next Steps Suggestions (Identify, Prioritize, Implement iteratively)
1. **Codebase Refactoring**: Extract common `yt_dlp` logic into a core module/package.
2. **Implement async background download queue for FastAPI**
3. **Enhance progress tracking via WebSockets or polling endpoints**
4. **Integrate HTMX for richer frontend interactions**
5. **Create configuration file for defaults**
6. **Add proper tests (unit + integration)**
7. **Installer scripts/Docker support**
8. **Improve UI/UX in both modes with additional features**
9. **Security & validation hardening**

---

*Generated based on repository content overview from packed Repomix output.*

