#!/usr/bin/python3

import os
import sys
from pytube import YouTube

logfile=""

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    with open(logfile, 'w') as w:
        w.write(f"Status: {round(pct_completed, 2)} %")
    #print(f"Status: {round(pct_completed, 2)} %")


if __name__ == '__main__':

    link = sys.argv[1]
    SAVE_PATH = fr"{os.environ['HOME']}/Downloads"

    try:
        yt = YouTube(link, on_progress_callback=on_progress)
    except:
        print("Connection Error")

    # Get all streams and filter for mp4 files
    mp4_streams = yt.streams.filter(file_extension='mp4').all()

    if sys.argv[2] == None:
        for video in mp4_streams:
            print(video)

        item = int(input("Which video you want to download?"))
    else:
        item = int(sys.argv[2])

    # select the video
    d_video = mp4_streams[item]

    #print(d_video.filesize)

    filename = sys.argv[1]
    logfile = fr"{os.environ['HOME']}/Downloads/{filename}.log"

    try:
        d_video.download(output_path=SAVE_PATH, filename=filename)
        print('Video downloaded successfully!')
    except:
        print("Error during downloading the video")

