import os

with open(fr"{os.environ['HOME']}/Downloads/download.log") as f:
    line = f.readline()
    size = line.split(" ")[1]
    print(size)


