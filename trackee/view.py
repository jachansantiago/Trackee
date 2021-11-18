import matplotlib.pyplot as plt

class View():

    def __init__(self, figsize=(10, 5)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
    

    def refresh(self, frame_id, image):
        self.ax.imshow(image)
        plt.title('BeeID Track Labeling Frame: {}'.format(frame_id))
        plt.draw()
        