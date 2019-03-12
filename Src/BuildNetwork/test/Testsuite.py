
import unittest

from BuildNetwork.BuildingQueue import BuildingQueue
from BuildNetwork.BuildModelGather import BuildModelGather

class TestSuite(unittest.TestCase):

        def testModule(self):
           m = BuildModelGather.set_buildmap(self)
           assert len(m) == 10
           assert len(m[0]) == 10






if __name__ == '__main__':
    unittest.main()