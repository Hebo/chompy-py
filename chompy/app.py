import pathlib
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .downloader import Downloader

app = FastAPI()

DOWNLOAD_DIR = pathlib.Path(r"./downloads")
# DOWNLOAD_URL_P = pathlib.Path(r"./downloads")

@app.get("/")
def read_root():
    return {"Hello": "Welcome to chompy!"}

@app.get("/download")
def download_video(url: str):
    print("Downloading %s" % url)
    downloader = Downloader(DOWNLOAD_DIR)
    path = downloader.download(url)

    print("got filename:", path)
    return {"video_path": path}

@app.get("/videos")
def get_video(path:str):
    """
    Open video at the given path
    """
    p = pathlib.Path(path)
    if not p.is_file():
        return HTTPException(status_code=404, detail="Video not found")

    return FileResponse(path)
