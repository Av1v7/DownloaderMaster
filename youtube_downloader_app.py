import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pytube import YouTube
import os

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 350
appearance_modes = {"System": "System", "Light": "Light", "Dark": "Dark"}
download_files_path = os.path.expanduser("~\Desktop")

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.load_saved_path()
        self.setup_ui()

    def save_path(self):
        with open("path.txt", "w") as file:
            file.write(download_files_path)

    def load_saved_path(self):
        global download_files_path
        if not os.path.exists("path.txt") or os.stat("path.txt").st_size == 0:
            download_files_path = os.path.expanduser("~\Desktop")
            with open("path.txt", "w") as file:
                file.write(download_files_path)
        else:
            with open("path.txt", "r") as file:
                saved_path = file.read().strip()
                if os.path.exists(saved_path): 
                    download_files_path = saved_path
                else:
                    download_files_path = os.path.expanduser("~\Desktop")
                    with open("path.txt", "w") as new_file:
                        new_file.write(download_files_path)

    def browse_file(self):
        global download_files_path
        self.new_download_files_path = filedialog.askdirectory()
        if self.new_download_files_path:
            download_files_path = self.new_download_files_path
            self.saved_files_path.configure(text=f"Download Path: {download_files_path}")
            self.save_path()
        
    def clear_fields(self):
        self.link.delete(0, tk.END)
        self.title.configure(text=f"Last Download: {self.youtube_obj.title}")
        self.is_downloaded_text.configure(text="", text_color="black")
        self.progress_precentage.configure(text="0%")
        self.progress_bar.set(0)

    
    def change_download_format(self, format):
        if format in ["MP3", "MP4"]:
            self.file_format.set(format)

    def load_appearance_mode(self):
        mode = ""
        if not os.path.exists("appearance_mode.txt") or os.stat("appearance_mode.txt").st_size == 0:
            ctk.set_appearance_mode("System")
            with open("appearance_mode.txt", "w") as file:
                file.write("System")
        else:
            with open("appearance_mode.txt", "r") as file:
                mode = file.read()
                ctk.set_appearance_mode(appearance_modes[mode])
        return mode
    
    def optionmenu_callback(self, choice):
        if choice in appearance_modes.keys():
            ctk.set_appearance_mode(choice)
            with open("appearance_mode.txt", "w") as file:
                file.write(choice)

    def center_screen(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100

        percentage = str(int(percentage_of_completion))

        self.progress_precentage.configure(text=f"{percentage}%")
        self.progress_precentage.update()
        self.progress_bar.set(float(percentage_of_completion) / 100)

    def download_video(self):
        try:
            self.already_downloaded = False
            self.youtube_link = self.link.get()
            self.youtube_obj = YouTube(self.youtube_link, on_progress_callback=self.on_progress)
            
            self.file_extension = ".mp4" if self.file_format.get() == "MP4" else ".mp3"
            self.downloaded_file_path = os.path.join(download_files_path, self.youtube_obj.title + self.file_extension)
            
            if os.path.isfile(self.downloaded_file_path):
                self.already_downloaded = True
                self.is_downloaded_text.configure(text=f"{self.youtube_obj.title}{self.file_extension} Already downloaded.", text_color="orange")
                messagebox.showinfo("Info", "File already downloaded.")
                self.link.delete(0, tk.END)
                return
            
            if self.file_format.get() == "MP4" and not self.already_downloaded:
                youtube_video = self.youtube_obj.streams.get_highest_resolution()
                downloaded_file = youtube_video.download(output_path=download_files_path)
                
                self.title.configure(text=self.youtube_obj.title, text_color="white")
                self.is_downloaded_text.configure(text="Downloaded successfully.", text_color="green")
                messagebox.showinfo("Success", "Download successful!")
                self.clear_fields()
                
                if os.path.isfile(downloaded_file):
                    os.startfile(downloaded_file)
            else:
                youtube_audio = self.youtube_obj.streams.filter(only_audio=True).first()
                downloaded_file = youtube_audio.download(output_path=download_files_path)
                
                mp3_filename = downloaded_file.split('.')[0] + '.mp3'
                os.rename(downloaded_file, mp3_filename)
                
                self.title.configure(text=self.youtube_obj.title, text_color="white")
                self.is_downloaded_text.configure(text="Downloaded successfully.", text_color="green")
                messagebox.showinfo("Success", "Download successful!")
                self.clear_fields()
                
                if os.path.isfile(mp3_filename):
                    os.startfile(mp3_filename)
        except:
            if not self.youtube_link:
                self.is_downloaded_text.configure(text="Empty youtube URL.", text_color="red")
            else:
                self.is_downloaded_text.configure(text="Invalid youtube URL.", text_color="red")

    def setup_ui(self):
        self.root.title("Youtube Downloader Master")
        self.center_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.root.resizable(False, False)

        self.title = ctk.CTkLabel(self.root, text="Insert a youtube link:")
        self.title.pack(padx=10, pady=10)

        self.url = tk.StringVar()
        self.link = ctk.CTkEntry(self.root, width=350, height=40, textvariable=self.url)
        self.link.pack()

        self.is_downloaded_text = ctk.CTkLabel(self.root, text="")
        self.is_downloaded_text.pack()

        self.progress_precentage = ctk.CTkLabel(self.root, text="0%")
        self.progress_precentage.pack()

        self.progress_bar = ctk.CTkProgressBar(self.root, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=10, pady=10)

        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack()

        self.download_button = ctk.CTkButton(self.root, text="Download", command=self.download_video)
        self.download_button.pack(in_=self.button_frame, side=ctk.LEFT, padx=10, pady=10)

        self.brwose_button = ctk.CTkButton(self.root, text="Browse", command=self.browse_file)
        self.brwose_button.pack(in_=self.button_frame, side=ctk.LEFT, padx=10, pady=10)

        self.saved_files_path = ctk.CTkLabel(self.root, text=f"Download Path: {download_files_path}")
        self.saved_files_path.pack(padx=10, pady=10)

        self.file_format = tk.StringVar()
        self.file_format.set("MP3")

        self.format_label = ctk.CTkLabel(self.root, text="Select file format:")
        self.format_label.pack()

        self.mp4_radio = ctk.CTkRadioButton(self.root, text="MP3", variable=self.file_format, value="MP3")
        self.mp4_radio.pack()

        self.mp3_radio = ctk.CTkRadioButton(self.root, text="MP4", variable=self.file_format, value="MP4")
        self.mp3_radio.pack()

        self.appearance_mode_label = ctk.CTkLabel(self.root, text="Select appearance mode:")
        self.appearance_mode_label.pack(side=ctk.LEFT)
        self.appearance_mode_label.place(y=290)

        self.default_appearance_mode = self.load_appearance_mode()

        self.optionmenu_var = ctk.StringVar(value=self.default_appearance_mode or "System")
        self.combobox = ctk.CTkOptionMenu(self.root, values=list(appearance_modes.keys()), variable=self.optionmenu_var, command=self.optionmenu_callback, height=30, width=30)
        self.combobox.pack(side=ctk.LEFT)
        self.combobox.place(y=315)