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
        self.model = GoLModel(x,y)
        self.viewmodel = GoLViewModel(self.model, res, x, y)
        self.view = GoLView(x, y, res, self.viewmodel)
        
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
                self.view.renderBoxes(self.model.field)
    
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
    def __init__(self, x, y, noBorder=True) -> None:
        self.x = x
        self.y = y
        self.field = [[ False for _y in range(y)] for _x in range(x)]
        self.noBorder = noBorder

    def toggleFieldID(self, x, y):
        try:
            self.field[x][y] = not self.field[x][y]
        except:
            pass

    def doIteration(self):
        field = [[ False for _y in range(self.y)] for _x in range(self.x)]
        for x in range(self.x):
            for y in range(self.y):
                n = self.countNeighbours(x,y)
                c = self.field[x][y]
                l = False
                if c and n==2:
                    l = True
                if n==3:
                    l = True
                field[x][y] = l
        self.field = field
        return 

    def countNeighbours(self, px, py):
        neighbours = 0
        for _x in range(px-1, px+2):
            for _y in range(py-1, py+2):
                x = _x
                y = _y
                if x == px and y == py:
                    continue
                if self.noBorder:
                    if x < 0:
                        x = self.x - 1
                    if x >= self.x:
                        x = 0
                    if y < 0:
                        y = self.y - 1
                    if y >= self.y:
                        y = 0
                elif x < 0 or x >= self.x or y < 0 or y >= self.y:
                    continue
                if self.field[x][y]:
                    neighbours += 1
        return neighbours


# should only know about Model changes / use model methods 
class GoLViewModel:
    def __init__(self, model, res: int, x: int, y: int) -> None:
        self.model = model
        self.res = res
        self.field = [[ False for _y in range(y)] for _x in range(x)]
        pass

    def toggleFieldPx(self, x, y):
        self.model.toggleFieldID(x//self.res, y//self.res)
    pass


# should only know about ViewModel changes
class GoLView:
    def __init__(self, x: int, y: int, res: float, viewModel: GoLViewModel) -> None:
        self.resolution = res
        self.graph_uid = getUID(10)
        self.graph = sg.Graph(
            (x*res, y*res), 
            (0, 0),
            (x*res, y*res),
            key=self.graph_uid,
            enable_events=True,
            background_color='lightgrey')
        setattr(self, 'field', viewModel.field) # bind on field 

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