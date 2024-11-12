# YouTube Playlist MP3 Downloader

This project is a Python script that automates the process of downloading audio from YouTube playlists, extracting individual video links, and converting audio to MP3 format.

## Features

- Extracts individual video links from YouTube playlists.
- Downloads audio in M4A format.
- Converts downloaded M4A files to MP3 (128 kbps) using multiple threads for efficiency.
- Customizable settings for simultaneous downloads and conversions.

## Requirements

Install the required packages with:

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:

```plaintext
requests
gdown
```

Optionally, it is recommended to use a virtual environment to avoid any dependency conflicts:

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Usage

1. Clone or download the repository.
2. Create a file named `playlist_links.txt` and add YouTube playlist links, one per line.
3. Run the script:

   ```bash
   python download.py
   ```

4. The script will:
   - Check for `yt-dlp.exe` and `ffmpeg.exe`. If not found, they will be downloaded automatically.
   - Extract video links from each playlist and save them in `video_links.txt`.
   - Download each video as an M4A file in the `output` directory.
   - Convert each M4A file to MP3 format in the same directory.

## Configuration

You can customize the number of simultaneous downloads and conversions by adjusting these values at the beginning of the script:

```python
max_simultaneous_downloads = 16
max_simultaneous_conversions = 8
```

## License

This project is open-source and available under the MIT License.
