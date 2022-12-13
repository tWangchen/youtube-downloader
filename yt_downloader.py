import logging
import os

from pytube import Playlist, YouTube

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s: %(levelname)s:%(name)s: %(message)s")

file_handler = logging.FileHandler("yt-downloader.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

menu_options = {
    1: "Download YouTube single video",
    2: "Download YouTube single audo",
    3: "Download YouTube playlist video",
    4: "Download YouTube playlist audio",
    5: "Exit",
}


def print_menu():
    for key in menu_options.keys():
        print(f"{key} -- {menu_options[key]}")


def download_playlist_video(playlist_link):
    """Ref: https://pytube.io/en/latest/user/exceptions.html"""
    yt_playlist = Playlist(playlist_link)
    for url in yt_playlist.video_urls:
        try:
            yt = YouTube(url)
        except VideoUnavailable:
            logger.exception(f"Video {url} is unavaialable, skipping.")
        else:
            yt.streams.get_highest_resolution().download(output_path=".")
            logger.info(f"From playlist download video option, downloaded: {url}")


def download_playlist_audio(playlist_link):
    """Ref: https://pytube.io/en/latest/user/exceptions.html"""
    yt_playlist = Playlist(playlist_link)
    for url in yt_playlist.video_urls:
        try:
            yt = YouTube(url)
        except VideoUnavailable:
            logger.exception(f"Video {url} is unavaialable, skipping.")
        else:
            file = yt.streams.get_audio_only().download(output_path=".")
            base, ext = os.path.splitext(file)
            new_file = f"{base}.mp3"
            os.rename(file, new_file)
            logger.info(f"From playlist download audio option, downloaded: {url}")


def download_single_video(single_link):
    yt_single = YouTube(single_link)
    yt_single.streams.get_highest_resolution().download(output_path=".")
    logger.info(f"From single download video option, downloaded: {single_link}")


def download_single_audio(single_link):
    yt_single = YouTube(single_link)
    file = yt_single.streams.get_audio_only().download(output_path=".")
    base, ext = os.path.splitext(file)
    new_file = f"{base}.mp3"
    os.rename(file, new_file)
    logger.info(f"From single download audio option, downloaded: {single_link}")


def main():
    while True:
        print_menu()
        option = int(input("Enter your choice: "))
        try:
            if option == 1:
                single_link = input("Enter YouTube link for video download: ")
                download_single_video(single_link)
            elif option == 2:
                single_link = input("Enter YouTube link for audio download: ")
                download_single_audio(single_link)
            elif option == 3:
                playlist_link = input("Enter YouTube playlist for video download: ")
                download_playlist_video(playlist_link)
            elif option == 4:
                playlist_link = input("Enter YouTube playlist for audio download: ")
                download_playlist_audio(playlist_link)
            elif option == 5:
                exit()
        except Exception as e:
            logger.exception(f"Opps! {e}")


if __name__ == "__main__":
    main()
