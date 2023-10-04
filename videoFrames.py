from datetime import timedelta
import cv2
import numpy as np
import os
import base64


def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def videoFrames(video_file):
    filename, _ = os.path.splitext(video_file)
    # if not os.path.isdir(filename):
    #     os.mkdir(filename)
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
            # frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            # cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame)

            _, im_arr = cv2.imencode('.jpg', frame)
            im_bytes = im_arr.tobytes()

            enc_frame = base64.b64encode(im_bytes)
            yield enc_frame


if __name__ == "__main__":
    import sys
    video_file = sys.argv[1]
    videoFrames(video_file)