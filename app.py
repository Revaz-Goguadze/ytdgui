from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    format_opt = data.get('format', 'mp4')
    download_path = data.get('destination', str(Path.home() / "Downloads" / "YTDownloader"))
    os.makedirs(download_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if format_opt == 'mp4' else 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [download_callback],
        'ignoreerrors': True,
        'nooverwrites': True,
    }

    if data.get('playlist'):
        ydl_opts['yes_playlist'] = True
        ydl_opts['outtmpl'] = os.path.join(download_path, '%(playlist_title)s/%(title)s.%(ext)s')

    if data.get('subtitles'):
        ydl_opts.update({
            'writesubtitles': True,
            'allsubtitles': True,
            'subtitleslangs': ['en']
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({"status": "success", "message": "Download completed!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 