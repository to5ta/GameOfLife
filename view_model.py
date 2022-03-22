from subscribable import Subscribable

class GoLViewModel(Subscribable):
    def __init__(self, res: int, x: int, y: int) -> None:
        super(GoLViewModel, self).__init__()
        self.res = res
        self.field = [[ False for _y in range(y)] for _x in range(x)]
        self.isRunning = False

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
    
    def onChange(self, model):
        self.field = model.field
        self.contactSubscribers()

