from view_model import * 
from utils import getUID

import PySimpleGUI as sg

from view_model import GoLViewModel

class GoLView(Subscribable):
    def __init__(self, x: int, y: int, boxSize: float, viewModel: GoLViewModel) -> None:
        self.viewModel = viewModel
        self.boxSize = boxSize
        self.graph_uid = getUID(10)
        self.graph = sg.Graph(
            (x*boxSize, y*boxSize), 
            (0, 0),
            (x*boxSize, y*boxSize),
            key=self.graph_uid,
            enable_events=True,
            background_color='lightgrey')
        
        self.stopped = True
        self.button = sg.Button('  Start  ', key=getUID(10))
        self.window = sg.Window(
            'Conways Game of Life', 
            [[self.graph], 
             [self.button]],
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
    
    def onChange(self, viewModel: GoLViewModel):
        self._renderBoxes(viewModel.field)

    def handleEvents(self):
        if not self.terminated:
            event, values = self.window.read(timeout=500) 
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
    
    def dispatchEvents(self, event, values):
        if event == sg.WIN_CLOSED:
            self.window.close()
            self.terminated = True
        elif event == '__TIMEOUT__':
            pass
        elif event == self.button.Key:
            self.toggleStartStop()        
        elif (self.stopped and event == self.graph_uid):
            self.viewModel.toggleFieldPx( *values[self.graph_uid] )   


