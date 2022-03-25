from subscribable import Subscribable

class GoLViewModel(Subscribable):
    def __init__(self, res: int, x: int, y: int, model) -> None:
        super(GoLViewModel, self).__init__()
        self.res = res
        self.field = [[ False for _y in range(y)] for _x in range(x)]
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
        self.field = model.field
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

