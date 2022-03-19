
class Observable(object):
    def __init__(self) -> None:
        self.eventHandler = {}

    def registerHandler(self, other, handler):
        self.eventHandler[other] = handler
    
    def unregisterHandler(self, other):
        try:
            del self.eventHandler[other]
        except:
            print("WARN: No object found for deleteing EventHandler!")

    def onPropertyChanged(self):
        for ob, eventhandler in self.eventHandler.items():
            getattr(ob, eventhandler)(self)

            