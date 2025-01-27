import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw
from pytube import Playlist, YouTube
import pygame
import os
import subprocess

# Initialize Pygame
pygame.init()

# Constants for colors and screen dimensions
COLORS = {'red': (255, 0, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0), 'yellow': (255, 255, 0)}
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
THUMB_SIZE = (160, 120)
BORDER_WIDTH = 5

def fetch_video_urls(playlist_url):
    """
    Fetch the video URLs from a YouTube playlist.
    """
    playlist = Playlist(playlist_url)
    # Ensure the result is a list
    return list(playlist.video_urls)

def download_thumbnail(video_url):
    """
    Download the thumbnail of a YouTube video.
    """
    yt = YouTube(video_url)
    thumbnail_url = yt.thumbnail_url
    response = requests.get(thumbnail_url)
    return Image.open(BytesIO(response.content))

def add_border(image, color):
    """
    Add a colored border to an image (thumbnail).
    """
    bordered_image = Image.new('RGB', (image.width + 2 * BORDER_WIDTH, image.height + 2 * BORDER_WIDTH), color)
    bordered_image.paste(image, (BORDER_WIDTH, BORDER_WIDTH))
    return bordered_image

def display_thumbnails(screen, thumbnails):
    """
    Display the thumbnails with colored borders on the Pygame screen.
    """
    screen_width, screen_height = screen.get_size()
    num_columns = 2
    num_rows = 2
    thumb_width = (screen_width - (num_columns + 1) * BORDER_WIDTH) // num_columns
    thumb_height = (screen_height - (num_rows + 1) * BORDER_WIDTH) // num_rows
    new_thumb_size = (thumb_width, thumb_height)

    for i, (image, color) in enumerate(thumbnails):
        if isinstance(color, str) and color.startswith('http'):
            color = 'black'  # Default to black if color is invalid
        resized_image = image.resize(new_thumb_size, Image.LANCZOS)
        bordered_image = add_border(resized_image, color)
        x = (i % num_columns) * (new_thumb_size[0] + BORDER_WIDTH) + BORDER_WIDTH
        y = (i // num_columns) * (new_thumb_size[1] + BORDER_WIDTH) + BORDER_WIDTH
        screen.blit(pygame.image.fromstring(bordered_image.tobytes(), bordered_image.size, bordered_image.mode), (x, y))
        pygame.display.update()
        
        
def play_video(video_url):
    """
    Play the selected video using cvlc.
    """
    try:
        # Download the video using yt-dlp
        video_path = f"{os.path.expanduser('~')}/Downloads/video.mp4"

        # Delete the file if it already exists
        if os.path.exists(video_path):
            os.remove(video_path)

        # Download the video using yt-dlp    
        subprocess.run(['yt-dlp', '-o', video_path, video_url], check=True)

        # Play the downloaded video using cvlc
        subprocess.run(['cvlc', '--play-and-exit', video_path])
    except Exception as e:
        print(f"Error playing video: {e}")
                
def main():
    """
    Main function to run the application.
    """
    while True:
        playlist_url = 'https://youtube.com/playlist?list=PL_ym6QHjS1syjzqEx_yKHjQsuYccFZ1mU&si=BaqsVMl6M7KW7e3a'
        # Fetch video URLs from the playlist
        video_urls = fetch_video_urls(playlist_url)
        print(f"Video URLs: {video_urls}")
        # Randomly select 4 video URLs
        selected_videos = random.sample(video_urls, 4)
        print(f"Selected videos: {selected_videos}")
        
        thumbnails = []
        for i, video_url in enumerate(selected_videos):
            # Download the thumbnail and resize it
            thumbnail = download_thumbnail(video_url).resize(THUMB_SIZE)
            # Select the color based on index
            color = list(COLORS.values())[i]
            # Add colored border to the thumbnail
            bordered_thumbnail = add_border(thumbnail, color)
            # Append the bordered thumbnail and video URL to the list
            thumbnails.append((bordered_thumbnail, video_url))
        
        # Set up the Pygame screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('YouTube Video Selector')

        # Display the thumbnails on the screen
        display_thumbnails(screen, thumbnails)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    # Check which key was pressed and play the corresponding video
                    if event.key == pygame.K_1:
                        index = event.key - pygame.K_1
                        if index < len(selected_videos):
                            play_video(thumbnails[0][1])
                            running = False  # Exit the inner loop to restart the main loop     
                    elif event.key == pygame.K_2:
                        index = event.key - pygame.K_2
                        if index < len(selected_videos):
                            play_video(thumbnails[1][1])
                            running = False  # Exit the inner loop to restart the main loop
                        #play_video(thumbnails[1][1])
                    elif event.key == pygame.K_3:
                        index = event.key - pygame.K_3
                        if index < len(selected_videos):
                            play_video(thumbnails[2][1])
                            running = False  # Exit the inner loop to restart the main loop
                        #play_video(thumbnails[2][1])
                    elif event.key == pygame.K_4:
                        index = event.key - pygame.K_4
                        if index < len(selected_videos):
                            play_video(thumbnails[0][1])
                            running = False  # Exit the inner loop to restart the main loop
                        #play_video(thumbnails[3][1])

        pygame.quit()

if __name__ == '__main__':
    main()