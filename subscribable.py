
class Subscribable(object):

    subscribers = {}

    def subscribeTo(self, other):
        if not other in Subscribable.subscribers.keys(): 
            Subscribable.subscribers[other] = [self]
        else:
            Subscribable.subscribers[other].append(self)

    def unsubscribeFrom(self, other):
        if self in Subscribable.subscribers.keys(): 
            del Subscribable.subscribers[other]

    def contactSubscribers(self):
        if self in Subscribable.subscribers.keys():
            for other in Subscribable.subscribers[self]:
                other.onChange(self)
    
    def onChange(self, other):
        raise NotImplementedError()


            