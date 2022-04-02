from subscribable import Subscribable
import numpy as np

class GoLViewModel(Subscribable):
    def __init__(self, res: int, x: int, y: int, model) -> None:
        super(GoLViewModel, self).__init__()
        self.res = res
        self.field = np.zeros(shape=(x,y), dtype=bool)
        self.isRunning = False
        self.simuDelta = .2
        self.model = model

    def toggleFieldPx(self, px, py):
        try:
            x = px//self.res 
            y = py//self.res
            self.field[x][y] = not self.field[x][y]
            self.contactSubscribers()
        except:
            pass
    
    def start(self):
        self.isRunning = True
        self.contactSubscribers()
    
    def stop(self):
        self.isRunning = False
        self.contactSubscribers()
    
    def setSimuDelta(self, ms):
        self.simuDelta = ms / 1000.
        self.contactSubscribers()
    
    def onChange(self, model):
        self.field = model.field_data[model.field_data_index]
        self.simuDelta = model.simuDelta
        self.contactSubscribers()
    
    def stepForward(self):
        if not self.isRunning:
            self.model.forwardStep()
    
    def stepBackward(self):
        if not self.isRunning:
            self.model.backwardStep()
    
    def setCacheSize(self, size):
        self.model.setCacheSize(size)

