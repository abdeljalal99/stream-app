import os

# print(os.listdir('./001-opencv'))

from videoFrames import videoFrames

for frame in videoFrames('./videos/001.mp4'):
    print(frame)
    break
