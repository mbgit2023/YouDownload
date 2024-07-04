import sys
import requests
import subprocess
from urllib.parse import urlparse

if __name__ == '__main__':
    url = sys.argv[1]
    if url == "":
        subprocess.run(["python3", "popup.py", "Enter a valid URL", "", "lightGreen"])
        exit(False)

    parsedurl = urlparse(url)
    if not parsedurl.scheme == 'http' and not parsedurl.scheme == 'https' and not parsedurl.scheme == 'ftp':
        subprocess.run(["python3", "popup.py", fr"The URL is not valid", "", "red"])
        exit(False)

    try:
        req = requests.get(url)
        if not req.status_code == 200:
            subprocess.run(
                ["python3", "./popup.py", "Error downloading the file", fr"Server response: {req.status_code}", "red"])
            exit(False)
    except:
        subprocess.run(
            ["python3", "./popup.py", f"Check the internet connection and try again", "", "red"])
        exit(False)
