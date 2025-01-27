import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw
from pytube import Playlist, YouTube
import pygame
import os

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
    bordered_image = Image.new('RGB', (THUMB_SIZE[0] + 2 * BORDER_WIDTH, THUMB_SIZE[1] + 2 * BORDER_WIDTH), color)
    bordered_image.paste(image, (BORDER_WIDTH, BORDER_WIDTH))
    return bordered_image

def display_thumbnails(screen, thumbnails):
    """
    Display the thumbnails with colored borders on the Pygame screen.
    """
    for i, (image, color) in enumerate(thumbnails):
        x = (i % 2) * (THUMB_SIZE[0] + 2 * BORDER_WIDTH + 10) + 100
        y = (i // 2) * (THUMB_SIZE[1] + 2 * BORDER_WIDTH + 10) + 100
        screen.blit(pygame.image.fromstring(image.tobytes(), image.size, image.mode), (x, y))
        pygame.display.update()

def play_video(video_url):
    """
    Play the selected video using vlc.
    """
    try:
        print(f"Streaming video from URL: {video_url}")
        os.system(f'vlc --fullscreen {video_url}')
    except Exception as e:
        print(f"Error playing video: {e}")

def main():
    """
    Main function to run the application.
    """
    playlist_url = 'https://youtube.com/playlist?list=PLqaalFyKa_zbnkR3mNCs2Z6cyp7pRCga8&si=xsnpH7Jf1WhUiRxB'
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
            elif event.type == pygame.KEYDOWN:
                # Check which key was pressed and play the corresponding video
                if event.key == pygame.K_1:
                    play_video(thumbnails[0][1])
                elif event.key == pygame.K_2:
                    play_video(thumbnails[1][1])
                elif event.key == pygame.K_3:
                    play_video(thumbnails[2][1])
                elif event.key == pygame.K_4:
                    play_video(thumbnails[3][1])

    pygame.quit()

if __name__ == '__main__':
    main()