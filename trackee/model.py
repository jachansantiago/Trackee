from trackee.utils import get_video, new_body
import cv2


class Model():
    
    def __init__(self, video, video_data=None):
        self.video = get_video(video, video_data)
        self.capture = cv2.VideoCapture(video)
        self.capture_frame = -1
        
    @property
    def video_name(self):
        return self.video.video_name[:-4]
        
    def save(self, filename):
        self.video.save(filename)
        
    def get_image(self, frame_number, bbox=True, idtext=True):
        if frame_number - self.capture_frame != 1:
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
            
        ret, image = self.capture.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.capture_frame = frame_number

        return self.video[frame_number].draw_frame_image(image, bbox=bbox, idtext=idtext, min_parts=-1)
    
    def add_annotation(self, frame_id, body_id, coords):
        for body in self.video[frame_id]:
            if body.id == body_id:
                body._parts[3][0] = coords
                break
        else:
            body = new_body(self.video[frame_id], body_id, coords)
            self.video[frame_id].update([body])
            
    def get_video_size(self):
        return len(self.video)
