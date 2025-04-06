import customtkinter as ctk
from downloader import download_video
import yt_dlp
import threading
from pathlib import Path
import os
from tkinter import filedialog

class YTDownloaderGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("YouTube Downloader")
        self.geometry("800x600")
        self.cancel_download = False  # Used to cancel an ongoing download

        # Main grid: 2 columns to split some buttons
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- Top Frame: URL, Options & Destination ---
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        
        # URL Entry (Row 0)
        self.url_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text="Enter YouTube URL",
            width=600,
            height=35
        )
        self.url_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=(0,10), sticky="ew")
        
        # Options: Playlist and Subtitles (Row 1)
        self.playlist_var = ctk.BooleanVar(value=False)
        self.playlist_check = ctk.CTkCheckBox(
            self.top_frame,
            text="Playlist",
            variable=self.playlist_var,
            font=("Arial", 12),
            height=30
        )
        self.playlist_check.grid(row=1, column=0, padx=10, sticky="w")
        
        self.download_subtitles = ctk.BooleanVar(value=False)
        self.subtitles_check = ctk.CTkCheckBox(
            self.top_frame,
            text="Subtitles",
            variable=self.download_subtitles,
            font=("Arial", 12),
            height=30
        )
        self.subtitles_check.grid(row=1, column=1, padx=10, sticky="e")
        
        # Destination Selection (Row 2)
        default_path = str(Path.home() / "Downloads" / "YTDownloader")
        self.dest_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text="Destination Folder",
            width=400,
            height=35,
        )
        self.dest_entry.insert(0, default_path)
        self.dest_entry.grid(row=2, column=0, padx=(10,5), pady=(10,0), sticky="ew")
        
        self.browse_btn = ctk.CTkButton(
            self.top_frame,
            text="Browse",
            command=self.browse_folder,
            width=100,
            height=35,
            font=("Arial", 12)
        )
        self.browse_btn.grid(row=2, column=1, padx=(5,10), pady=(10,0))
        
        # --- Format Selection Frame (Row 1 in main grid) ---
        self.format_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.format_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.format_frame.grid_columnconfigure((0,1), weight=1)
        
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
        
        # --- Quality Selection (Row 2 in main grid) ---
        self.quality_var = ctk.StringVar(value="Best")
        self.quality_menu = ctk.CTkOptionMenu(
            self,
            values=["Best", "720p", "480p", "360p"],
            variable=self.quality_var,
            width=200,
            height=32,
            font=("Arial", 12)
        )
        self.quality_menu.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
        
        # --- Buttons Frame: Download & Cancel (Row 3 in main grid) ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0,1), weight=1)
        
        self.download_btn = ctk.CTkButton(
            self.button_frame,
            text="Download",
            command=self.start_download,
            width=200,
            height=40,
            font=("Arial", 13, "bold")
        )
        self.download_btn.grid(row=0, column=0, padx=10)
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.cancel_download_process,
            width=200,
            height=40,
            font=("Arial", 13, "bold"),
            state="disabled"
        )
        self.cancel_btn.grid(row=0, column=1, padx=10)
        
        # --- Progress Frame (Row 4 in main grid) ---
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_remove()
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=15,
            corner_radius=5
        )
        self.progress_bar.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.progress_bar.set(0)
        
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
        
        # --- Log Textbox (Row 5 in main grid) ---
        self.log_text = ctk.CTkTextbox(self, width=760, height=100)
        self.log_text.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.log_text.configure(state="normal")
        self.log_message("Application started.")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, "end")
            self.dest_entry.insert(0, folder)
            self.log_message(f"Destination set to: {folder}")

    def log_message(self, message: str):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        
    def download_callback(self, d):
        if self.cancel_download:
            raise Exception("Download cancelled by user.")
        if d['status'] == 'downloading':
            if not self.progress_frame.winfo_viewable():
                self.progress_frame.grid()
            if 'total_bytes' in d and d['total_bytes']:
                percentage = d['downloaded_bytes'] / d['total_bytes']
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                percentage = d['downloaded_bytes'] / d['total_bytes_estimate']
            else:
                percentage = 0
            self.progress_bar.set(percentage)
            self.speed_label.configure(text=f"Speed: {d.get('speed_str', '--')}")
            self.size_label.configure(text=f"Size: {d.get('_percent_str', '--')} of {d.get('_total_bytes_str', '--')}")
            self.eta_label.configure(text=f"ETA: {d.get('_eta_str', '--')}")
            if 'filename' in d:
                current_file = Path(d['filename']).name
                self.progress_label.configure(text=f"Downloading: {current_file[:20]}...")
        elif d['status'] == 'finished':
            self.progress_label.configure(text="Processing...")
        elif d['status'] == 'error':
            self.progress_label.configure(text="Error occurred!")
            self.progress_frame.grid_remove()
    
    def download(self, url):
        destination = self.dest_entry.get() or str(Path.home() / "Downloads" / "YTDownloader")
        format_opt = self.format_var.get()
        playlist = self.playlist_var.get()
        subtitles = self.download_subtitles.get()
        quality = self.quality_var.get()

        try:
            download_video(
                url=url,
                format_opt=format_opt,
                destination=destination,
                playlist=playlist,
                subtitles=subtitles,
                quality=quality,
                progress_hooks=[self.download_callback]
            )
            self.progress_label.configure(text="Download completed!")
            self.log_message("Download completed successfully.")
            self.after(3000, self.progress_frame.grid_remove)
        except Exception as e:
            if "cancelled" in str(e).lower():
                self.progress_label.configure(text="Download cancelled by user.")
                self.log_message("Download cancelled by user.")
            else:
                self.progress_label.configure(text=f"Error: {str(e)}")
                self.log_message(f"Error occurred: {str(e)}")
            self.progress_frame.grid_remove()
        finally:
            self.progress_bar.set(0)
            self.speed_label.configure(text="Speed: --")
            self.size_label.configure(text="Size: --")
            self.eta_label.configure(text="ETA: --")
            self.download_btn.configure(state="normal")
            self.cancel_btn.configure(state="disabled")
    
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            self.progress_label.configure(text="Please enter a URL")
            return
            
        self.cancel_download = False
        self.download_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_label.configure(text="Starting download...")
        self.progress_frame.grid()
        thread = threading.Thread(target=self.download, args=(url,))
        thread.daemon = True
        thread.start()
        
        def check_thread():
            if thread.is_alive():
                self.after(100, check_thread)
            else:
                self.download_btn.configure(state="normal")
                self.cancel_btn.configure(state="disabled")
        check_thread()
    
    def cancel_download_process(self):
        self.cancel_download = True
        self.log_message("Download cancellation requested.")
        self.cancel_btn.configure(state="disabled")

if __name__ == "__main__":
    app = YTDownloaderGUI()
    app.mainloop() 