#!/usr/bin/env python3

from statistics import mode
import PySimpleGUI as sg  
from timeit import default_timer as timer

from utils import getUID

from model import GoLModel
from view_model import GoLViewModel
from view import GoLView

class Game:
    def __init__(self, x: int, y: int, res: float) -> None:
        self.model = GoLModel(x,y)
        self.viewmodel = GoLViewModel(res, x, y)
        self.view = GoLView(x, y, res, self.viewmodel)

        self.view.subscribeTo(self.viewmodel)
        self.viewmodel.subscribeTo(self.model)
        self.model.subscribeTo(self.viewmodel)
        
        self.over = False


class Application:
    def __init__(self) -> None:
        self.game = Game(20, 20, 30)
        self.terminated = False
    
    def run(self):
        while not self.game.over:
            self.game.view.handleEvents()
            self.game.model.tryUpdateSimulation()

def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()