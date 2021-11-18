import cv2
from plotbee.video import Video
from plotbee.body import Body
from plotbee.frame import Frame
import os

def get_video(video, video_data):
    if video_data is None or not os.path.exists(video_data):
        video_data =  create_empty_video(video)
    else:
        video_data = Video.load(video_data)

    video_data.load_video(video)
    
    return video_data

def new_body(frame, body_id, coords):
    skeleton = {3: [coords]}
    return Body(skeleton, center=3, 
         connections=[], angle_conn=[3,3],
         frame=frame,body_id=body_id)

def get_video_length(video_file):
    cap = cv2.VideoCapture(video_file)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length


def create_empty_video(video_file):
    config = dict() 
    config["VIDEO_PATH"] = video_file
    video_len = get_video_length(video_file)
    
    frames = list()
    for frame_id in range(video_len):
        frames.append(Frame([], frame_id))
        
    video = Video(frames=frames, tracks={}, config=config)
    return video

def rescale(image, scale_factor=4):
    height, width, _ = image.shape
    width = width // scale_factor
    height = height // scale_factor
    dim = (width, height)
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)


def get_next_id(ids):
    i = 0
    while i in ids:
        i += 1
    return i