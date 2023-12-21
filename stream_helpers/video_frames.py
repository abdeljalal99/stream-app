import cv2
import numpy as np
import base64


def get_saving_frames_durations(cap, saving_fps): # saving_fps = output fps
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def get_framerate(video_file):
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    return fps

def video_frames(video_file):
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_durations = get_saving_frames_durations(cap, fps)
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break
        frame_duration = count / fps
        count += 1
        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            break

        if frame_duration >= closest_duration:
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
            _, im_arr = cv2.imencode('.jpg', frame)
            im_bytes = im_arr.tobytes()

            enc_frame = base64.b64encode(im_bytes)
            yield enc_frame
