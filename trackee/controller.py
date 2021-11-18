from plotbee.body import Body
from trackee.view import View
from trackee.model import Model
from trackee.utils import get_next_id

from IPython.display import display

import ipywidgets as widgets
from ipywidgets import HBox,VBox
from datetime import date


class GUIController():
    
    def __init__(self, video, video_data=None, frame_number=0, bbox_dim=(25,25), rescale_factor=4, **kwargs):
        
        Body.width, Body.height = bbox_dim

        self.view = View()
        self.model = Model(video, video_data, rescale_factor=rescale_factor, **kwargs)
        
        
        self.frame_number = frame_number
        self.jump_to = 0

        video_ids = self.model.get_ids()
        self._current_id = get_next_id(video_ids)
        
        # Controllers
        self.jump_button = widgets.Button(description = 'Jump!')
        self.jump_text = widgets.IntText(description="Jump to Frame:")
        self.next_button = widgets.Button(description = 'Next Frame')  
        self.prev_button = widgets.Button(description = 'Prev Frame')   
        self.save_button = widgets.Button(description="Save")
        self.beeid_text = widgets.IntText(description="Bee Id:", value=self._current_id)

    @property
    def current_id(self):
        return self._current_id

    @current_id.setter
    def current_id(self, value):
        self._current_id = value
        self.beeid_text.value = value
        
       
    def get_image(self, bbox=True, idtext=True):
        if self.frame_number < 0:
            self.frame_number = 0
        if self.frame_number >= self.model.get_video_size():
            self.frame_number = self.model.get_video_size() - 1
        return self.model.get_image(self.frame_number, bbox=bbox, idtext=idtext)
    
    def add_annotation(self, frame_id, body_id, coords):
        self.model.add_annotation(frame_id, body_id, coords)
        
    def jump_clicked(self,arg):
        # 1. change bee id
        video_ids = self.model.get_ids()
        self.current_id = get_next_id(video_ids)
        # jump
        self.frame_number = self.jump_to
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
        
    def on_beeid_change(self, change):
        self.current_id = change['new']

    def on_jumpto_change(self, change):
        self.jump_to = change['new']
        video_ids = self.model.get_ids()
        self.current_id = get_next_id(video_ids)
        
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
        
        self.jump_button.on_click(self.jump_clicked)
        self.next_button.on_click(self.next_frame_clicked)
        self.prev_button.on_click(self.prev_frame_clicked)
        self.save_button.on_click(self.save_annotations)
        self.beeid_text.observe(self.on_beeid_change, names='value')
        self.jump_text.observe(self.on_jumpto_change, names='value')
    
        id_controllers = HBox([self.beeid_text])
        frame_controllers = HBox([self.next_button, self.prev_button, self.jump_button, self.jump_text])
        save_controllers = HBox([self.save_button])
        box_layout = widgets.Layout(display='flex',
                        # flex_flow='row',
                        # align_items='center',
                        width='100%')
      
        
        display(VBox([id_controllers,frame_controllers, save_controllers],layout=box_layout))
        
        
        cid = self.view.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        image = self.get_image()
        self.view.refresh(self.frame_number, image)