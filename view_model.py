from observable import *
from model import *

class GoLViewModel(Observable):
    def __init__(self, model : GoLModel, res: int, x: int, y: int) -> None:
        super(GoLViewModel, self).__init__()
        self.model = model
        self.res = res
        self.field = [[ False for _y in range(y)] for _x in range(x)]

    def toggleFieldPx(self, px, py):
        try:
            x = px//self.res 
            y = py//self.res
            self.field[x][y] = not self.field[x][y]
            self.onPropertyChanged()
        except:
            pass
    
    def onModelChanged(self, model : GoLModel):
        self.field = model.field
        self.onPropertyChanged()

