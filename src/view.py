from view_model import *
from utils import getUID
import os

import PySimpleGUI as sg
from PIL import ImageGrab
from view_model import GoLViewModel
import numpy as np

recorded_frames = 0
record_session = getUID(5)

def windowToImage(window : sg.Window, filepath : str):
    window.refresh()
    lx, ly = window.CurrentLocation()
    x, y = window.size
    coord = np.array((lx+7, ly,(x+5+lx +5), (y+ly+30))) * 1.5
    grab = ImageGrab.grab(bbox=coord.tolist(), all_screens=True)
    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    grab.save(filepath)

def graphToImage(graph : sg.Graph, filepath : str):
    widget = graph.Widget
    box = (
        widget.winfo_rootx(),
        widget.winfo_rooty(),
        widget.winfo_rootx() + widget.winfo_width(),
        widget.winfo_rooty() + widget.winfo_height())
    grab = ImageGrab.grab(bbox=box)
    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    grab.save(filepath)

class GoLView(Subscribable):
    def __init__(self, x: int, y: int, boxSize: float, viewModel: GoLViewModel) -> None:
        self.viewModel = viewModel
        self.boxSize = boxSize
        self.graph_uid = getUID(10)

        self.record = True

        self.graph = sg.Graph(
            (x*boxSize, y*boxSize),
            (0, 0),
            (x*boxSize, y*boxSize),
            key=self.graph_uid,
            enable_events=True,
            background_color='lightgrey')

        self.stopped = True
        self.button = sg.Button(
            '  Start  ',
            key=getUID(10))

        self.speedSlider = sg.Slider(
            key=getUID(10),
            range=(10,750),
            default_value=200,
            resolution=1,
            orientation='h',
            tooltip="Simulation Cycle in ms",
            enable_events=True,
            size=(50, 10))

        self.renderCheckbox = sg.Checkbox(
            "Record", 
            key=getUID(10),
            enable_events=True)

        self.window = sg.Window(
            'Conways Game of Life',
            [[self.graph],
             [self.button, self.renderCheckbox, self.speedSlider]],
            return_keyboard_events=True)        

        self.terminated = False

    def _addBox(self, x, y) -> None:
        res = self.boxSize
        self.graph.draw_rectangle(
            (x * res, y * res),
            (x * res + res, y * (res) + res),
            line_color='black', fill_color='yellow')

    def _renderBoxes(self, boxes) -> None:
        self.graph.erase()
        for x, box_col in enumerate(boxes):
            for y, box in enumerate(box_col):
                if box:
                    self._addBox(x,y)
        if (self.record):
            global recorded_frames, record_session
            windowToImage(self.window, f"records/{record_session}_{recorded_frames:04}.jpg")
            recorded_frames += 1
            
    def onChange(self, viewModel: GoLViewModel):
        self._renderBoxes(viewModel.field)
        self.speedSlider.DefaultValue = viewModel.simuDelta * 1000

    def handleEvents(self):
        if not self.terminated:
            event, values = self.window.read(timeout=17)
            self.dispatchEvents(event, values)

    def toggleStartStop(self):
        if(self.stopped):
            self.stopped = False
            self.viewModel.start()
            self.button.Update(text=' Stop  ')
        else:
            self.stopped = True
            self.viewModel.stop()
            self.button.Update(text=' Start ')

    def __del__(self):
        self.window.close()

    def dispatchEvents(self, event, values):
        if event == sg.WIN_CLOSED:
            self.window.close()
            self.terminated = True
        elif event == '__TIMEOUT__':
            pass
        elif event == self.button.Key:
            self.toggleStartStop()
        elif event == self.speedSlider.Key:
            self.viewModel.setSimuDelta(values[event])
        elif (self.stopped and event == self.graph_uid):
            self.viewModel.toggleFieldPx( *values[self.graph_uid] )
        elif event == self.renderCheckbox.Key:
            self.record = values[event]


