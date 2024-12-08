import customtkinter as ctk
import yt_dlp
import threading
from pathlib import Path
import os

class YTDownloaderGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("YouTube Downloader")
        self.geometry("600x400")
        
        # Configure grid layouts
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # URL and Playlist Frame
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=20, pady=20)
        self.top_frame.grid_columnconfigure(0, weight=1)
        
        # URL Entry
        self.url_entry = ctk.CTkEntry(
            self.top_frame,  # Changed parent to top_frame
            placeholder_text="Enter YouTube URL",
            width=400,
            height=35
        )
        self.url_entry.grid(row=0, column=0, padx=(0, 10))  # Added right padding
        
        # Playlist Checkbox moved up
        self.is_playlist = ctk.BooleanVar(value=False)
        self.playlist_check = ctk.CTkCheckBox(
            self.top_frame,  # Changed parent to top_frame
            text="Playlist",
            variable=self.is_playlist,
            font=("Arial", 12),
            height=35
        )
        self.playlist_check.grid(row=0, column=1)
        
        # Format Selection with better styling
        self.format_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.format_frame.grid(row=1, column=0, padx=20, pady=5)
        
        self.format_var = ctk.StringVar(value="mp4")
        self.video_radio = ctk.CTkRadioButton(
            self.format_frame, 
            text="Video (MP4)", 
            variable=self.format_var, 
            value="mp4",
            font=("Arial", 12)
        )
        self.video_radio.grid(row=0, column=0, padx=20)
        
        self.audio_radio = ctk.CTkRadioButton(
            self.format_frame, 
            text="Audio (MP3)", 
            variable=self.format_var, 
            value="mp3",
            font=("Arial", 12)
        )
        self.audio_radio.grid(row=0, column=1, padx=20)
        
        # Quality Selection with better styling
        self.quality_var = ctk.StringVar(value="best")
        self.quality_menu = ctk.CTkOptionMenu(
            self,
            values=["Best", "720p", "480p", "360p"],
            variable=self.quality_var,
            width=200,
            height=32,
            font=("Arial", 12)
        )
        self.quality_menu.grid(row=2, column=0, padx=20, pady=10)
        
        # Download Button with better styling
        self.download_btn = ctk.CTkButton(
            self, 
            text="Download",
            command=self.start_download,
            width=200,
            height=40,
            font=("Arial", 13, "bold")
        )
        self.download_btn.grid(row=3, column=0, padx=20, pady=10)
        
        # Progress Frame (initially hidden)
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_remove()  # Hide initially
        
        # Progress Bar with better styling
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=15,
            corner_radius=5
        )
        self.progress_bar.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.progress_bar.set(0)
        
        # Status Labels Frame
        self.status_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.status_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.status_frame.grid_columnconfigure((0,1), weight=1)
        
        self.speed_label = ctk.CTkLabel(
            self.status_frame,
            text="Speed: --",
            font=("Arial", 11)
        )
        self.speed_label.grid(row=0, column=0, sticky="w")
        
        self.size_label = ctk.CTkLabel(
            self.status_frame,
            text="Size: --",
            font=("Arial", 11)
        )
        self.size_label.grid(row=0, column=1, sticky="e")
        
        self.eta_label = ctk.CTkLabel(
            self.status_frame,
            text="ETA: --",
            font=("Arial", 11)
        )
        self.eta_label.grid(row=1, column=0, sticky="w")
        
        self.progress_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=("Arial", 11)
        )
        self.progress_label.grid(row=1, column=1, sticky="e")

    def download_callback(self, d):
        if d['status'] == 'downloading':
            # Show progress frame if hidden
            if not self.progress_frame.winfo_viewable():
                self.progress_frame.grid()
            
            # Calculate percentage
            if 'total_bytes' in d:
                percentage = d['downloaded_bytes'] / d['total_bytes']
            elif 'total_bytes_estimate' in d:
                percentage = d['downloaded_bytes'] / d['total_bytes_estimate']
            else:
                percentage = 0
            
            # Update progress bar
            self.progress_bar.set(percentage)
            
            # Update status labels
            self.speed_label.configure(text=f"Speed: {d.get('speed_str', '--')}")
            self.size_label.configure(
                text=f"Size: {d.get('_percent_str', '--')} of {d.get('_total_bytes_str', '--')}"
            )
            self.eta_label.configure(text=f"ETA: {d.get('_eta_str', '--')}")
            
            if 'filename' in d:
                current_file = Path(d['filename']).name
                self.progress_label.configure(
                    text=f"Downloading: {current_file[:20]}..."
                )
                
        elif d['status'] == 'finished':
            self.progress_label.configure(text="Processing...")
            
        elif d['status'] == 'error':
            self.progress_label.configure(text="Error occurred!")
            self.progress_frame.grid_remove()  # Hide progress frame on error

    def download(self, url):
        download_path = str(Path.home() / "Downloads" / "YTDownloader")
        os.makedirs(download_path, exist_ok=True)
        
        format_opt = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        if self.format_var.get() == "mp3":
            format_opt = 'bestaudio/best'
            
        quality = self.quality_var.get().lower()
        if quality != "best":
            format_opt = f'bestvideo[height<={quality[:-1]}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

        ydl_opts = {
            'format': format_opt,
            'progress_hooks': [self.download_callback],
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'ignoreerrors': True,  # Skip failed downloads in playlist
            'nooverwrites': True,  # Don't overwrite files
        }
        
        if self.is_playlist.get():
            ydl_opts.update({
                'yes_playlist': True,
                'extract_flat': False,
                'outtmpl': os.path.join(download_path, '%(playlist_title)s/%(title)s.%(ext)s'),
            })
        
        if self.format_var.get() == "mp3":
            ydl_opts.update({
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Reset progress indicators
                self.progress_bar.set(0)
                self.speed_label.configure(text="Speed: --")
                self.size_label.configure(text="Size: --")
                self.eta_label.configure(text="ETA: --")
                
                # Extract info first to show total videos for playlist
                info = ydl.extract_info(url, download=False)
                if self.is_playlist.get() and 'entries' in info:
                    total_videos = len(list(info['entries']))
                    self.progress_label.configure(
                        text=f"Found {total_videos} videos in playlist"
                    )
                
                # Start actual download
                ydl.download([url])
                
                self.progress_label.configure(text="Download completed!")
                # Hide progress frame after a delay
                self.after(3000, self.progress_frame.grid_remove)
                
        except Exception as e:
            self.progress_label.configure(text=f"Error: {str(e)}")
            self.progress_frame.grid_remove()  # Hide progress frame on error
        finally:
            # Reset progress indicators
            self.progress_bar.set(0)
            self.speed_label.configure(text="Speed: --")
            self.size_label.configure(text="Size: --")
            self.eta_label.configure(text="ETA: --")

    def start_download(self):
        url = self.url_entry.get()
        if not url:
            self.progress_label.configure(text="Please enter a URL")
            return
            
        self.download_btn.configure(state="disabled")
        self.progress_label.configure(text="Starting download...")
        self.progress_frame.grid()  # Show progress frame when starting download
        
        # Start download in a separate thread
        thread = threading.Thread(target=self.download, args=(url,))
        thread.daemon = True
        thread.start()
        
        def check_thread():
            if thread.is_alive():
                self.after(100, check_thread)
            else:
                self.download_btn.configure(state="normal")
        
        check_thread()

if __name__ == "__main__":
    app = YTDownloaderGUI()
    app.mainloop() 