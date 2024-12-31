import logging
import os

from pytubefix import Playlist, YouTube

# from pytube import Playlist, YouTube


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s: %(levelname)s:%(name)s: %(message)s")

file_handler = logging.FileHandler("yt-downloader.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

menu_options = {
    1: "Download YouTube single video",
    2: "Download YouTube single audio",
    3: "Download YouTube playlist video",
    4: "Download YouTube playlist audio",
    5: "Exit",
}


def print_menu():
    for key in menu_options.keys():
        print(f"{key} -- {menu_options[key]}")


def download_playlist(playlist_link, audio_video):
    yt_playlist = Playlist(playlist_link)
    for single_link in yt_playlist.video_urls:
        try:
            yt_single = YouTube(single_link)
        except VideoUnavailable:
            logger.exception(f"Video {single_link} is unavaialable, skipping.")
        else:
            download_single(single_link, audio_video)


def download_single(single_link, audio_video):
    yt_single = YouTube(single_link)
    print(f"Downloading: {yt_single.title}")
    file = yt_single.streams.get_highest_resolution().download(output_path=".")
    base, ext = os.path.splitext(file)
    publish_date = str(yt_single.publish_date)[0:10]
    if audio_video == "video":
        new_file = f"{base}_{publish_date}{ext}"
    elif audio_video == "audio":
        new_file = f"{base}_{publish_date}.mp3"
    os.rename(file, new_file)
    logger.info(f"Completed downloading: {yt_single.title}")
    print(f"Completed downloading: {yt_single.title}\n")


def main():
    while True:
        print_menu()
        option = int(input("Enter your choice: "))
        try:
            if option == 1:
                single_link = input("Enter YouTube link for video download: ")
                download_single(single_link, "video")
            elif option == 2:
                single_link = input("Enter YouTube link for audio download: ")
                download_single(single_link, "audio")
            elif option == 3:
                playlist_link = input("Enter YouTube playlist for video download: ")
                download_playlist(playlist_link, "video")
            elif option == 4:
                playlist_link = input("Enter YouTube playlist for audio download: ")
                download_playlist(playlist_link, "audio")
            elif option == 5:
                exit()
        except Exception as e:
            logger.exception(f"Opps! {e}")


if __name__ == "__main__":
    main()
