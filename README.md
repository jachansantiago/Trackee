# Trackee v1.1
> Python tracking annotation tool

[![Python Version][python-image]][python-url]


Notebook for efficient quick annotation of tracks in a video.

![Tool Screenshot][tool-image]

## Installation
```sh
git clone --recurse-submodules https://github.com/jachansantiago/Trackee.git
cd Trackee
pip install . # or pip install .[tags] to install with apriltag
```
## Instructions
To annotate a bee you must first add an ID in the "Bee ID" field of the GUI. After this all you need to do is click in the center of the desired bee to annotate and the frame will change after each click. Once done click the "Save" button and you should be set.


## Tool Buttons
Currently the tool supports:
1. Start Over: Changes the view to the first frame.
2. Next Frame: Changes the view to the next frame.
3. Prev Frame: Changes the view to the previous frame.
4. ID Bee: Add ID wanted for bee (This is needed to for the plotting to work. Use integers)
5. View Tracks: Plots complete tracks if view is in the first frame. Else it would plot the tracks backwards (Trajectory)
6. Save: Allows to add annotations to the json file provided.
![Buttons Screenshot][buttons-image]



## Meta
Kendrick G. Morales Ortiz - [Github](https://github.com/KendrickMorales)


<!-- Markdown link & img dfn's -->
[python-url]: https://www.python.org/downloads/
[python-image]: https://upload.wikimedia.org/wikipedia/commons/a/a5/Blue_Python_3.8_Shield_Badge.svg
[tool-image]: docs/tracking_tool.png
[buttons-image]: docs/buttons.png
[bookera-url]: https://github.com/Bookera-App
[plotbee-url]: https://github.com/jachansantiago/plotbee
