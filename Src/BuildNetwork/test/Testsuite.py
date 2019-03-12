
import unittest

from BuildNetwork.BuildModelGather import BuildModelGather
import numpy as np
import numpy.testing as npt
from BuildNetwork.BuildingNeutral import BuildingsNeutral
from BuildNetwork.BuildingTerranQueue import BuildingTerranQueue



class TestSuite(unittest.TestCase):

        def testModule(self):
            x = 81
            y = 81
            list = BuildModelGather.set_buildmap(self)
            assert len(list) == x
            assert len(list[0]) == y
            newList = np.full((81,81),0)
            npt.assert_array_equal(list, newList)
            print("Test Size being Created to true")

        def testBuildModle(self):
          list = BuildModelGather.set_locations(self)







if __name__ == '__main__':
    unittest.main()