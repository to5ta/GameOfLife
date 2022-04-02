import unittest
import parentDirectory
from model import GoLModel
import numpy as np

class TestGoLModel(unittest.TestCase):
    def testDoIteration(self):
        model = GoLModel(20, 20, 10, True)
        before =  [[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True,  False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  False, False],
                   [False, False, False, True,  False, False, False, False, False, False, False, False, False, False, True,  False, True,  False, False, False],
                   [False, False, False, True,  False, False, False, True,  True,  False, False, False, False, False, False, False, True,  False, False, False],
                   [False, False, False, True,  False, False, False, True,  True,  False, False, False, False, False, True,  True,  True,  True,  False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, True,  False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, True,  False, True,  False, False, False],
                   [False, False, False, False, True,  False, True,  False, False, False, False, False, False, True,  False, False, False, False, False, False],
                   [False, False, False, False, True,  True,  False, False, False, False, False, False, False, True,  False, False, False, False, False, False],
                   [False, False, False, False, False, True,  False, False, False, False, False, False, False, True,  False, False, True,  False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]]
        model.field_data[model.field_data_index] = np.array(before)
        after = [[False, False, False, False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, True,  True,  False, True,  True,  False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, True,  True,  False, False, False, False, False],
                 [False, False, True,  True,  True,  False, False, True,  True,  False, False, False, False, False, True,  False, False, False, False, False],
                 [False, False, False, False, False, False, False, True,  True,  False, False, False, False, False, True,  True,  True,  True,  False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, True,  False, False, False, False, False, False, False, False, True,  True,  False, False, False, False, False],
                 [False, False, False, False, True,  False, True,  False, False, False, False, False, True,  True,  True,  False, False, False, False, False],
                 [False, False, False, False, True,  True,  False, False, False, False, False, False, True,  True,  False, True,  False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, True,  False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]]
        field = model.generateNextIteration()

        self.assertTrue(np.array_equal(field, np.array(after)), "Field did not equal expected outcome after an Iteration!")

    def testCountNeighbours(self):
        size = {"x": 5, "y": 5}
        model = GoLModel(size["x"], size["y"], 10, True)
        neighbours = [[ 0 for _y in range(size["y"])] for _x in range(size["x"])]
        model.field_data[model.field_data_index][2][2] = True
        model.field_data[model.field_data_index][2][3] = True
        model.field_data[model.field_data_index][2][1] = True
        model.field_data[model.field_data_index][1][2] = True
        for x in range(size["x"]):
            for y in range(size["y"]):
                n = model.countNeighbours(x,y)
                neighbours[x][y] = n
        
        expected_neighbours = [[0, 1, 1, 1, 0], [1, 3, 3, 3, 1], [1, 2, 3, 2, 1], [1, 2, 3, 2, 1], [0, 0, 0, 0, 0]]
        self.assertEqual(neighbours, expected_neighbours, "Neighbour numbers did not equal expected data!")

if __name__ == "__main__":
    unittest.main()
