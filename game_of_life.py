#!/usr/bin/env python3

import random
import PySimpleGUI as sg  
from timeit import default_timer as timer

def getUID(length=10) -> str:
    uid = ""
    pool = [*range(ord('0'), ord('9'))]
    pool += [*range(ord('a'), ord('z'))]
    pool += [*range(ord('A'), ord('Z'))]
    for _ in range(length):
        uid += chr(pool[random.randint(0,len(pool)-1)])
    return uid


class Game:
    def __init__(self, x: int, y: int, res: float) -> None:
        self.view = GoLView(x,y,res)
        self.model = GoLModel(x,y)
        self.viewmodel = GoLViewModel(self.view, self.model)
        
        self.__lastSimuUpdate = timer()
        self.isSimuRunning = False
        self.simuDelta = 200 #ms

        self.over = False
   
    def tryUpdateSimu(self):
        if(self.isSimuRunning):
            if(self.__lastSimuUpdate - timer() > self.simuDelta):
                self.model.doIteration()
                self.__lastSimuUpdate = timer()
    
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


class GoLModel:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.field = [[ False for _y in range(y)] for _x in range(x)]
    
    def toggleFieldID(self, x, y):
        try:
            self.field[x][y] = not self.field[x][y]
        except:
            pass

    def doIteration(self):
        field = [[ False for _y in range(y)] for _x in range(x)]

      
    def countNeighbours(self, px, py, noBorder=True):
        neighbours = 0
        # for x in range(px-1, px+1):
        #     if px < 0 and noBorder:
        #         continue
        #     else:
        #         px = self.x-1    
        #     for y in range(py-1, py+1):
        #         if (py < 0 and not noBorder:
        #             continue
        #         else:
        #             py = self.y-1
        #         if self.field[px][py]:
        #             neighbours += 1
        return neighbours

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

    def addBox(self, x, y) -> None:
        res = self.resolution
        self.graph.draw_rectangle(
            (x * res, y * res),
            (x * res + res, y * (res) + res),
            line_color='black', fill_color='yellow')

    def renderBoxes(self, boxes) -> None:
        self.clear()
        for x, box_col in enumerate(boxes):
            for y, box in enumerate(box_col):
                if box:
                    self.addBox(x,y)

    def clear(self) -> None:
        self.graph.erase()


class GoLViewModel:
    def __init__(self, view, model) -> None:
        self.view = view
        self.model = model
        self.res = view.resolution
        pass

    def toggleFieldPx(self, x, y):
        self.model.toggleFieldID(x//self.res, y//self.res)
    pass


class Application:
    def __init__(self) -> None:
        self.game = Game(10, 10, 30)
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

    def toggleStartStop(self):
        self.game.isSimuRunning = not self.game.isSimuRunning
        if(self.game.isSimuRunning):
            self.button.Update(text=' Start ')
        else:
            self.button.Update(text=' Stop  ')


def main():
    app = Application()


if __name__ == "__main__":
    main()