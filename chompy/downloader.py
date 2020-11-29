#!/usr/bin/env python3
# Usage: vid https://clips.twitch.tv/AgitatedFitHyenaDansGame

import argparse
import os
import pathlib
import subprocess
import re
from typing import Optional, List

import youtube_dl

# DEFAULT_QUALITY = "bestvideo[height<=?1080]+bestaudio/best"
# Goals: <1080p, reasonable size, avoid merging if possible
# Below works decently well, but merges a lot?
# https://www.reddit.com/r/youtubedl/comments/fe08jx/can_youtubedl_download_only_mp4_files_at_1080_or/
DEFAULT_QUALITY = "bestvideo[ext=mp4][height<=?1080]+bestaudio[ext=m4a]/best"

class FilenameLogger:
    def __init__(self):
        self.final_path = None

    def debug(self, msg):
        print("got msg -> ", msg)
        match = re.search(r'^\[ffmpeg\] Merging formats into "(.*?)"$', msg)
        if match:
            self.final_path = match.group(1)
            print(f"[FilenameLogger] Captured filename {self.final_path}")
            return

        match = re.search(r'^\[download\][\s](.*?)[\s]has already.+$', msg)
        if match:
            self.final_path = match.group(1)
            print(f"[FilenameLogger] Captured filename {self.final_path}")
            return

    def get_path(self) -> Optional[str]:
        return self.final_path


class Downloader:
    # youtube-dl can merge seperate video+audio files into a single
    # container, with possible extensions:
    merged_file_exts: List[str] = [".mp4", ".mkv"]

    def __init__(self, download_dir: pathlib.Path) -> None:
        self.filename: Optional[str] = None
        self.download_dir = download_dir

        self.logger = FilenameLogger()

    def _get_logger(self):
        """
        return the specialized logger to capture filenames
        """
        return self.logger

    def handle_download(self, d):
        # print("d -> ", d)
        if d["status"] == "finished":
            # print("Download: ", d)
            self.filename = d["filename"]

    def _get_filename(self) -> Optional[str]:
        if self.logger.get_path():
            print("returning path from logger")
            return self.logger.get_path()
        if self.filename:
            print("returning path from self.filename")
            return self.filename
        return None

    def handle_complete(self) -> Optional[str]:
        path = self._get_filename()
        print("Using filename {}".format(path))
        if not path:
            raise Exception("no path found")

        p = pathlib.Path(path)
        if p.is_file():
            return path

        return None

    def download(self, url:str):
        ydl_opts = {
            "format": DEFAULT_QUALITY,
            "outtmpl": str(self.download_dir / "%(title)s.%(ext)s"),
            "progress_hooks": [self.handle_download],
            "retries": 3,
            "logger": self._get_logger()
        }

        out_filename = None
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            out = ydl.download([url])
            out_filename = self.handle_complete()
        return out_filename


