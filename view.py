from view_model import * 
from utils import getUID
import PySimpleGUI as sg

class GoLView:
    def __init__(self, x: int, y: int, res: float) -> None:
        self.resolution = res
        self.graph_uid = getUID(10)
        self.graph = sg.Graph(
            (x*res, y*res), 
            (0, 0),
            (x*res, y*res),
            key=self.graph_uid,
            enable_events=True,
            background_color='lightgrey')

    def _addBox(self, x, y) -> None:
        res = self.resolution
        self.graph.draw_rectangle(
            (x * res, y * res),
            (x * res + res, y * (res) + res),
            line_color='black', fill_color='yellow')

    def renderBoxes(self, boxes) -> None:
        self.graph.erase()
        for x, box_col in enumerate(boxes):
            for y, box in enumerate(box_col):
                if box:
                    self._addBox(x,y)
    
    def onViewModelChanged(self, viewModel: GoLViewModel):
        self.renderBoxes(viewModel.field)
