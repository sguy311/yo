# YouTube Video Selector

This project is a YouTube video selector application built with Python. It fetches video URLs from a YouTube playlist, downloads their thumbnails, displays them with colored borders using Pygame, and allows the user to play the selected video.

## Requirements

The project requires the following Python packages:

- `pytube==12.1.0`
- `requests==2.31.0`
- `Pillow==9.4.0`
- `pygame==2.1.2`

You can install the required packages using the following command:

```sh
pip install -r requirements.txt
```

## Usage

To run the application, execute the `yo.py` script:

```sh
python yo.py
```

## Features

- Fetches video URLs from a YouTube playlist.
- Downloads thumbnails of the videos.
- Displays thumbnails with colored borders using Pygame.
- Allows the user to play the selected video using `cvlc`.

## How It Works

1. The application fetches video URLs from a specified YouTube playlist.
2. It randomly selects 4 video URLs and downloads their thumbnails.
3. The thumbnails are displayed on a Pygame screen with colored borders.
4. The user can press keys `1`, `2`, `3`, or `4` to play the corresponding video.

## File Structure

- `yo.py`: Main script containing the application logic.
- `requirements.txt`: List of required Python packages.
- `.gitignore`: Git ignore file to exclude `.mp4` files.