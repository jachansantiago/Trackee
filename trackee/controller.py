from plotbee.body import Body
from trackee.view import View
from trackee.model import Model

from IPython.display import display

import ipywidgets as widgets
from ipywidgets import HBox,VBox
from datetime import date

class GUIController():
    
    def __init__(self, video, video_data=None, frame_number=0, bbox_dim=(50,50)):
        
        Body.width, Body.height = bbox_dim
        
        self.view = View()
        self.model = Model(video, video_data)
        
        
        self.frame_number = frame_number
        self.current_id = 0
        
        # Controllers
        self.start_over = widgets.Button(description = 'Start Over')   
        self.next_button = widgets.Button(description = 'Next Frame')  
        self.prev_button = widgets.Button(description = 'Prev Frame')   
        self.save_button = widgets.Button(description="Save")
        self.text = widgets.IntText(description="Bee Id:")
       
    def get_image(self, bbox=True, idtext=True):
        if self.frame_number < 0:
            self.frame_number = 0
        if self.frame_number >= self.model.get_video_size():
            self.frame_number = self.model.get_video_size() - 1
        return self.model.get_image(self.frame_number, bbox=bbox, idtext=idtext)
    
    def add_annotation(self, frame_id, body_id, coords):
        self.model.add_annotation(frame_id, body_id, coords)
        
    def startover_clicked(self,arg):
        self.frame_number = 0
        image = self.get_image()
        self.view.refresh(self.frame_number, image) 
        
    def next_frame_clicked(self,arg):
        self.frame_number += 1
        image = self.get_image()
        self.view.refresh(self.frame_number, image)    
        
    def prev_frame_clicked(self,arg):
        self.frame_number -= 1    
        image = self.get_image()
        self.view.refresh(self.frame_number, image) 
        
    def next_frame(self):
        self.frame_number += 1
        image = self.get_image()
        self.view.refresh(self.frame_number, image)   
        
    def on_value_change(self, change):
        self.current_id = change['new']
        
    def on_click(self,event):
        coords = (event.xdata, event.ydata)
        self.add_annotation(self.frame_number, self.current_id, coords)
        self.next_frame()
                    
        
    def save_annotations(self,arg):
        today = date.today()
        date_str = today.strftime("%b-%d-%Y")
        
        video_name = self.model.video_name
        
        filename = "tracks_{date_str}_{video_name}.json".format(date_str=date_str,video_name=video_name)
        
        self.model.save(filename)
        
        
    def start(self):
        
        self.start_over.on_click(self.startover_clicked)
        self.next_button.on_click(self.next_frame_clicked)
        self.prev_button.on_click(self.prev_frame_clicked)
        self.save_button.on_click(self.save_annotations)
        self.text.observe(self.on_value_change, names='value')
    
        left_box = VBox([self.text])
        right_box = VBox([self.start_over, self.next_button,self.prev_button])
#         third_box = VBox([self.tracks_button])
        fourth_box = VBox([self.save_button])
        box_layout = widgets.Layout(display='flex',
                        flex_flow='row',
                        align_items='center',
                        width='50%')
      
        
        display(HBox([left_box,right_box],layout=box_layout))
        display(HBox([fourth_box],layout=box_layout))
        
        
        cid = self.view.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        image = self.get_image()
        self.view.refresh(self.frame_number, image)