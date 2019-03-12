
import unittest

from BuildNetwork.BuildModelGather import BuildModelGather
from BuildNetwork.BuildingNeutral import BuildingsNeutral
from BuildNetwork.BuildingTerranQueue import BuildingTerranQueue



class TestSuite(unittest.TestCase):

        def testModule(self):
            x = 81
            y = 81
            list = BuildModelGather.set_buildmap(self)
            assert len(list) == x
            assert len(list[0]) == y

        def testBuildModle(self):
           list = BuildModelGather.set_locations()







if __name__ == '__main__':
    unittest.main()