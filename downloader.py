import yt_dlp
import os
from pathlib import Path

def download_video(
    url: str,
    format_opt: str = 'mp4',
    destination: str = None,
    playlist: bool = False,
    subtitles: bool = False,
    quality: str = 'best',
    progress_hooks=None
) -> None:
    """
    Unified YouTube download logic using yt_dlp.

    Args:
        url: The YouTube video or playlist URL.
        format_opt: 'mp4' for video, 'mp3' for audio-only.
        destination: Target directory path.
        playlist: Whether to download entire playlist.
        subtitles: Download subtitles if available.
        quality: Quality restriction e.g., 'best', '720p'.
        progress_hooks: List of yt_dlp progress hook callables.

    Raises:
        Exception: If download fails.
    """
    if destination is None:
        destination = str(Path.home() / "Downloads" / "YTDownloader")

    os.makedirs(destination, exist_ok=True)

    # Default format string
    if format_opt == 'mp4':
        fmt_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    else:
        fmt_str = 'bestaudio/best'

    # Limit resolution if specified
    q = quality.lower()
    if q != 'best' and format_opt == 'mp4':
        q_val = q.replace('p', '')
        fmt_str = f"bestvideo[height<={q_val}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

    outtmpl = os.path.join(destination, '%(title)s.%(ext)s')
    if playlist:
        outtmpl = os.path.join(destination, '%(playlist_title)s', '%(title)s.%(ext)s')

    ydl_opts = {
        'format': fmt_str,
        'outtmpl': outtmpl,
        'ignoreerrors': True,
        'nooverwrites': True,
    }

    if progress_hooks is not None:
        ydl_opts['progress_hooks'] = progress_hooks

    if playlist:
        ydl_opts['yes_playlist'] = True

    if subtitles:
        ydl_opts.update({
            'writesubtitles': True,
            'allsubtitles': True,
            'subtitleslangs': ['en']
        })

    if format_opt == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise Exception(f"Download failed: {e}")