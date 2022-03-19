#!/usr/bin/env python3

import PySimpleGUI as sg  
from timeit import default_timer as timer

from utils import getUID

from model import GoLModel
from view_model import GoLViewModel
from view import GoLView

class Game:
    def __init__(self, x: int, y: int, res: float) -> None:
        self.model = GoLModel(x,y)
        self.viewmodel = GoLViewModel(self.model, res, x, y)
        self.view = GoLView(x, y, res)
        
        self.viewmodel.registerHandler(self.view, self.view.onViewModelChanged.__name__)
        self.viewmodel.registerHandler(self.model, self.model.onViewModelChanged.__name__)
        self.model.registerHandler(self.viewmodel, self.viewmodel.onModelChanged.__name__)

        self._lastSimuUpdate = timer()
        self.isSimuRunning = False
        self.simuDelta = .200 #s

        self.over = False
    
    def tryUpdateSimu(self):
        if(self.isSimuRunning):
            now = timer()
            if((now - self._lastSimuUpdate) > self.simuDelta):
                self.model.doIteration()
                self._lastSimuUpdate = now
    
    def getGraph(self):
        return self.view.graph

    def dispatch(self, event, values):
        try:
            if (not self.isSimuRunning and event == self.view.graph_uid):
                self.viewmodel.toggleFieldPx( *values[self.view.graph_uid] )   
        except: 
            pass
        self.view.renderBoxes(self.model.field)
    
    def setIterDelta(self, delta: int):
        self.simuDelta = delta


class Application:
    def __init__(self) -> None:
        self.game = Game(20, 20, 30)
        self.button = sg.Button('  Start  ', key=getUID(10))

        self.window = sg.Window(
            'Conways Game of Life', 
            [[self.game.getGraph()], 
             [self.button]],
            return_keyboard_events=True) 
        self.terminated = False

        while not self.game.over:
            if not self.terminated:
                event, values = self.window.read(timeout=500) 

            if event == sg.WIN_CLOSED:
                self.window.close()
                self.terminated = True
            elif event == '__TIMEOUT__':
                pass
            elif event == self.button.Key:
                self.toggleStartStop()
            else:
                self.game.dispatch(event, values)
            self.game.tryUpdateSimu()

    def toggleStartStop(self):
        self.game.isSimuRunning = not self.game.isSimuRunning
        if(self.game.isSimuRunning):
            self.button.Update(text=' Stop  ')
        else:
            self.button.Update(text=' Start ')


def main():
    app = Application()


if __name__ == "__main__":
    main()