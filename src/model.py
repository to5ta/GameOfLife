from subscribable import Subscribable
from timeit import default_timer as timer
import numpy as np

from view_model import GoLViewModel
class GoLModel(Subscribable):
    def __init__(self, x, y, hist_size=99, noBorder=True) -> None:
        super(GoLModel, self).__init__()
        self.x = x
        self.y = y
        # self.field = np.zeros(shape=(x,y), dtype=bool)
        self.noBorder = noBorder

        self._lastSimuUpdate = timer()
        self.isSimuRunning = False
        self.simuDelta = .200 #s

        self.field_data = np.zeros(shape=(hist_size,x,y), dtype=bool)
        self.field_data_index = 0

        self.hist_size = hist_size
        self.current_hist_size = 0

    def forwardStep(self):
        if (self.current_hist_size < self.hist_size):
            self.current_hist_size += 1
        self.generateNextIteration()
        # self.field_data[self.field_data_index] = self.field
        self.field_data_index = (self.field_data_index+1) % self.hist_size 
        self.contactSubscribers()
        # print(f"Current History Size: {self.current_hist_size}")

    def backwardStep(self):
        if(self.current_hist_size > 0):
            self.current_hist_size -= 1
            self.field_data_index = (self.field_data_index-1) % self.hist_size 
            # self.field = self.field_data[self.field_data_index]
            self.contactSubscribers()
            # print(f"Current History Size: {self.current_hist_size}")


    def tryUpdateSimulation(self):
        if(self.isSimuRunning):
            now = timer()
            if((now - self._lastSimuUpdate) > self.simuDelta):
                self.forwardStep()
                self._lastSimuUpdate = now
    
    def onChange(self, viewmodel: GoLViewModel):
        self.field_data[self.field_data_index] = viewmodel.field
        self.simuDelta = viewmodel.simuDelta
        self.isSimuRunning = viewmodel.isRunning
    
    def setCacheSize(self, size):
        self.cache_length = size
        self.cache = self.cache[:size]

    def generateNextIteration(self):
        # field = np.zeros(shape=self.field.shape, dtype=bool)
        i = self.field_data_index + 1
        field = self.field_data[i]
        for x in range(self.x):
            for y in range(self.y):
                n = self.countNeighbours(x,y)
                c = self.field_data[self.field_data_index][x][y]
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
                if self.field_data[self.field_data_index][x][y]:
                    neighbours += 1
        return neighbours

