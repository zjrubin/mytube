#!/usr/bin/env python3
import math
import os
import sys

import yaml
from colorama import Fore
from pytube import YouTube


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "mytube_config.yml")


def main():
    try:
        # Read in the config
        with open(CONFIG_FILE, "r") as infile:
            config = yaml.safe_load(infile)

        for item in config:
            if "video" in item:
                handle_video(item)
            elif "collection" in item:
                handle_collection(item)
            else:
                raise ValueError(f"Unknown entry in mytube_config.yaml: {item}")

    except Exception as e:
        print(e)
        sys.exit(1)


def handle_video(video_config: dict):
    download_video(
        url=video_config["url"],
        directory=os.path.expanduser(video_config["dir"]),
        name=video_config.get("name"),
    )


def handle_collection(collection_config: dict):
    for video in collection_config["videos"]:
        download_video(
            url=video["url"],
            directory=os.path.expanduser(collection_config["dir"]),
            name=video.get("name"),
        )


def download_video(url: str, directory: str, name: str = None):
    file_extension = "mp4"
    video = None
    stream = None
    if name:
        file_path = f"{os.path.join(directory, name)}.{file_extension}"
    else:
        # Use highest resolution mp4 stream
        video = YouTube(url)
        stream = video.streams.filter(
            file_extension=file_extension
        ).get_highest_resolution()
        file_path = os.path.join(directory, stream.default_filename)

    # Check if the video file already exists.
    if os.path.exists(file_path):
        print(Fore.GREEN + f"{file_path} already exists! Skipping..." + Fore.RESET)
        return

    # If stream hasn't already been fetched, get it now
    video = video or YouTube(url)
    stream = (
        stream
        or video.streams.filter(file_extension=file_extension).get_highest_resolution()
    )

    # Register progress callbacks
    pc = ProgressCheck(file_path=file_path, file_size=stream.filesize)
    video.register_on_progress_callback(pc.on_progress)
    video.register_on_complete_callback(pc.on_complete)

    stream.download(
        output_path=directory,
        filename=name,
        skip_existing=False,
    )


class ProgressCheck:
    def __init__(self, file_path, file_size):
        self.file_path = file_path
        self.file_size = file_size
        self.percent_complete = 0

        print(Fore.YELLOW + f"{self.file_path} - beginning download..." + Fore.RESET)

    def on_progress(self, stream, chunk, bytes_remaining):
        # Gets the percentage of the file that has been downloaded.
        new_percent_complete = math.floor(
            (100 * (self.file_size - bytes_remaining)) / self.file_size
        )
        if new_percent_complete == self.percent_complete:
            return

        if new_percent_complete in (10, 20, 30, 40, 50, 60, 70, 80, 90):
            print(f"{self.file_path} - {new_percent_complete:00.0f}% downloaded")

        self.percent_complete = new_percent_complete

    def on_complete(self, stream, file_path):
        print(Fore.GREEN + f"{self.file_path} - finished downloading!" + Fore.RESET)


if __name__ == "__main__":
    main()
