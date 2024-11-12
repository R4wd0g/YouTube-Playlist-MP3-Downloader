import subprocess
import os
import requests
import gdown
from concurrent.futures import ThreadPoolExecutor, as_completed
import glob

max_simultaneous_downloads = 16
max_simultaneous_conversions = 8

YTDLP_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
FFMPEG_DRIVE_ID = "1SFIIYJSomDBGKfuICx1EkFDu-SxiDIRq"

def check_and_download_executables():
    if not is_executable_in_path("yt-dlp.exe") and not os.path.exists("yt-dlp.exe"):
        print("yt-dlp.exe not found. Downloading...")
        download_file(YTDLP_URL, "yt-dlp.exe")
    
    if not is_executable_in_path("ffmpeg.exe") and not os.path.exists("ffmpeg.exe"):
        print("ffmpeg.exe not found. Downloading from Google Drive with gdown...")
        download_ffmpeg_from_drive()

def is_executable_in_path(executable_name):
    return any(
        os.access(os.path.join(path, executable_name), os.X_OK)
        for path in os.environ["PATH"].split(os.pathsep)
    )

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Downloaded: {save_path}")

def download_ffmpeg_from_drive():
    url = f"https://drive.google.com/uc?id={FFMPEG_DRIVE_ID}"
    gdown.download(url, "ffmpeg.exe", quiet=False)
    print("ffmpeg.exe downloaded successfully.")

def extract_video_links():
    with open("playlist_links.txt", "r") as playlist_file, open("video_links.txt", "w") as video_file:
        playlists = playlist_file.readlines()
        for playlist in playlists:
            command = f'yt-dlp --flat-playlist -g -f m4a "{playlist.strip()}"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            video_file.write(result.stdout)

def download(link):
    command = f'yt-dlp -o "output/%(title)s.%(ext)s" -f m4a "{link.strip()}"'
    subprocess.call(command, shell=True)

def convert_file(m4a_file):
    mp3_file = m4a_file.replace(".m4a", ".mp3")
    command = f'ffmpeg -i "{m4a_file}" -vn -ar 44100 -ac 2 -b:a 128k -threads 4 "{mp3_file}"'
    subprocess.call(command, shell=True)
    os.remove(m4a_file)

check_and_download_executables()

extract_video_links()

with open("video_links.txt", "r") as file:
    links = file.readlines()

with ThreadPoolExecutor(max_workers=max_simultaneous_downloads) as executor:
    futures = [executor.submit(download, link) for link in links]
    for future in as_completed(futures):
        pass

m4a_files = glob.glob("output/*.m4a")
with ThreadPoolExecutor(max_workers=max_simultaneous_conversions) as executor:
    futures = [executor.submit(convert_file, m4a_file) for m4a_file in m4a_files]
    for future in as_completed(futures):
        pass
