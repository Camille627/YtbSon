# YtbSon

YouTube Audio Downloader and Converter (currently obsolete)

## Introduction

After frequently using questionable websites to obtain audio tracks from YouTube videos, I wondered if it was possible to program my own converter. The goal of this project is to create a simple and efficient converter that does not impose ads, redirects, delays, or unnecessary clicks.

Let's take a closer look at how YouTube works. The extracted audio file from a video is initially in the format provided by YouTube (often WebM or MP4). WebM is a simple lossy compression format, whereas MP4 is a container that can hold multiple audio or video tracks of different formats (e.g., MP3 or AAC). The AAC format does not contain metadata, which is inconvenient, so conversion is necessary. We offer two conversion formats: FLAC (lossless) and MP3 (lossy), which are widely used. The Python library `pytubefix` allows downloading YouTube videos. The conversion is done via the terminal, and to avoid additional parameters, we have a script for each format: `ytbmp3.py` and `ytbflac.py`.

Note that MP3 conversion reduces audio quality since it is a lossy compression format. FLAC files are, on average, ten times larger than MP3s for music but retain the original quality (compared to the extracted YouTube video file). The quality of an MP3 format is mainly related to its bitrate in kbps. Although the quality cannot be improved, it can be significantly degraded if this parameter is too low. Therefore, it must be properly adjusted.

## Prerequisites

- Python 3.x (<https://www.python.org/>)
- The following libraries:
  - `pytubefix`
  - (for `ytbmp3.py`) `pydub`
  - `mutagen`
- (for `ytbflac.py`) `ffmpeg` installed and accessible in the system PATH

### Installing Prerequisites

After installing Python, use the following commands to verify the installation:

> python --version  
> pip --version  

Install the required Python libraries via the terminal:

> pip install pytubefix pydub mutagen  

### Installing ffmpeg

1. Download `ffmpeg` (<https://ffmpeg.org/download.html>). Under "Windows," click on "Windows builds from gyan.dev" and download a "release full" version.
2. Extract the downloaded archive to a folder of your choice.
3. Add the `bin` folder path to the environment variable PATH:
   - Open Advanced System Settings (Win + R, then type "sysdm.cpl") and click "Environment Variables."
   - In the "User Variables" section, edit the "Path" variable:
     - Click "New" and add the full path to the `bin` directory of the `ffmpeg` folder (e.g., `C:\user\ffmpeg\bin`). Click "OK."
   - Verify the installation using the `ffmpeg -version` command in the terminal.

## Usage

### ytbflac.py

Run the following command in the terminal (navigate to the script directory):

> python ytbflac.py <YouTube_Video_URL> [output_path]

- `<YouTube_Video_URL>`: The URL of the YouTube video you want to download.
- `[output_path]`: (Optional) The directory where the audio file will be saved. If not specified, the file will be saved in the user's Downloads folder.

**Example**

To download and convert a YouTube video to FLAC and save it in the Downloads folder:

> python ytbflac.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

**Features**

- Converts the downloaded audio stream to FLAC format.
- Adds metadata (title, author) to the FLAC file.
- Deletes the original audio file after conversion.

**Notes**

- The downloaded audio file is initially in the format provided by YouTube (often WebM or MP4). The MP4 format is a container and can contain multiple audio or video tracks (e.g., AAC, which does not preserve metadata).
- The script automatically converts WebM and MP4 files to FLAC using `ffmpeg` (faster than `pydub`).

### ytbmp3.py

Run the following command in the terminal:

> python ytbmp3.py <YouTube_Video_URL> [output_path] --bitrate [bitrate]

- `<YouTube_Video_URL>`: The URL of the YouTube video you want to download.
- `[output_path]`: (Optional) The directory where the audio file will be saved. If not specified, the file will be saved in the user's Downloads folder.
- `[bitrate]`: (Optional) The bitrate value in kbps. Default is 124 kbps.

**Example**

To download and convert a YouTube video to MP3 and save the file in the Downloads folder:

> python ytbmp3.py https://www.youtube.com/watch?v=bc0KhhjJP98

To select a bitrate of 320 kbps:

> python ytbmp3.py https://www.youtube.com/watch?v=aqRGb8JkO38 --bitrate 320

**Features**

- Converts the downloaded audio stream to MP3 format.
- Adds metadata (title, author) to the MP3 file.

**Notes**

- The script automatically converts WebM and MP4 files to MP3 using `pydub` (slower than `ffmpeg`).
- The final audio track quality cannot exceed that of the extracted web page file. A high bitrate approaches the original quality but takes up more space (less than a FLAC file), whereas a low bitrate significantly degrades audio quality.

-------------------------------------------------
## Contribution

Thanks to Gauthier MARTIN for his advice.

Camille ANSEL

