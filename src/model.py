from subscribable import Subscribable
from timeit import default_timer as timer

from view_model import GoLViewModel
class GoLModel(Subscribable):
    def __init__(self, x, y, noBorder=True) -> None:
        super(GoLModel, self).__init__()
        self.x = x
        self.y = y
        self.field = [[ False for _y in range(y)] for _x in range(x)]
        self.noBorder = noBorder

        self._lastSimuUpdate = timer()
        self.isSimuRunning = False
        self.simuDelta = .200 #s
    
    def tryUpdateSimulation(self):
        if(self.isSimuRunning):
            now = timer()
            if((now - self._lastSimuUpdate) > self.simuDelta):
                self.doIteration()
                self._lastSimuUpdate = now
    
    def onChange(self, viewmodel: GoLViewModel):
        self.field = viewmodel.field
        self.simuDelta = viewmodel.simuDelta
        self.isSimuRunning = viewmodel.isRunning

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
        self.contactSubscribers()
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

