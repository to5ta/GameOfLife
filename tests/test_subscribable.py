import unittest
import parentDirectory
from subscribable import Subscribable

class Mock(Subscribable):
    def __init__(self) -> None:
        self.iWasNotified = False
        self.strCache = "init"
        super().__init__()

    def onChange(self, other):
        self.strCache = other.strCache
        self.iWasNotified = True

class TestSubscribable(unittest.TestCase):
    def _setup(self):
        t0 = Mock()
        t1 = Mock()
        t0.subscribeTo(t1)
        t1.subscribeTo(t0)
        return t0, t1
    
    def testSubscriptionMechanism(self):
        t0, t1 = self._setup()
        t0.contactSubscribers()
        self.assertTrue(t1.iWasNotified, "Subscribers onChange was not called!")
        self.assertFalse(t0.iWasNotified, "Subscribers onChange was called unexpectedly!")
        t1.contactSubscribers()
        self.assertTrue(t0.iWasNotified, "Subscribers onChange was not called!")

if __name__ == "__main__":
    unittest.main()



