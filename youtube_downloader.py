import logging
import os
import shutil
import sys

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
    yt_single = YouTube(single_link, on_progress_callback=on_progress)
    yt_single.streams.get_highest_resolution().download(output_path=".")
    logger.info(f"From single download video option, downloaded: {single_link}")


def download_single_audio(single_link):
    yt_single = YouTube(single_link)
    file = yt_single.streams.get_audio_only().download(output_path=".")
    base, ext = os.path.splitext(file)
    new_file = f"{base}.mp3"
    os.rename(file, new_file)
    logger.info(f"From single download audio option, downloaded: {single_link}")


def display_progress_bar(
    bytes_received: int, filesize: int, ch: str = "█", scale: float = 0.55
):
    """Ref: https://github.com/pytube/pytube/blob/master/pytube/cli.py#L209"""
    """Display a simple, pretty progress bar.
    Example:
    ~~~~~~~~
    PSY - GANGNAM STYLE(강남스타일) MV.mp4
    ↳ |███████████████████████████████████████| 100.0%
    :param int bytes_received:
        The delta between the total file size (bytes) and bytes already
        written to disk.
    :param int filesize:
        File size of the media stream in bytes.
    :param str ch:
        Character to use for presenting progress segment.
    :param float scale:
        Scale multiplier to reduce progress bar size.
    """
    columns = shutil.get_terminal_size().columns
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    progress_bar = ch * filled + " " * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    text = f" ↳ |{progress_bar}| {percent}%\r"
    sys.stdout.write(text)
    sys.stdout.flush()


def on_progress(stream, chunk: bytes, bytes_remaining: int):
    """Ref: https://github.com/pytube/pytube/blob/master/pytube/cli.py#L243"""
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)


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
