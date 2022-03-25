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

    
        self.cache = []
        self.cache_length = 10

    def forwardStep(self):
        self.field = self.generateNextIteration()
        self.cache.insert(0, self.field)
        if len(self.cache) > self.cache_length:
            self.cache.pop(-1)
        self.contactSubscribers()

    def backwardStep(self):
        if len(self.cache) > 1:
            self.cache.pop(0)
            self.field = self.cache[0]
            self.contactSubscribers()
            print(f"cache len: {len(self.cache)}")

    def tryUpdateSimulation(self):
        if(self.isSimuRunning):
            now = timer()
            if((now - self._lastSimuUpdate) > self.simuDelta):
                self.forwardStep()
                self._lastSimuUpdate = now
    
    def onChange(self, viewmodel: GoLViewModel):
        self.field = viewmodel.field
        self.simuDelta = viewmodel.simuDelta
        self.isSimuRunning = viewmodel.isRunning
    
    def setCacheSize(self, size):
        self.cache_length = size
        self.cache = self.cache[:size]

    def generateNextIteration(self):
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
        self.contactSubscribers()
        return field
        

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

