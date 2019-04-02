import unittest

from Models.BuildNetwork.BuildFacade import BuildFacade
import numpy as np
import numpy.testing as npt
import random


class test_buildFacade(unittest.TestCase):

    """
        The Method tests the build facade method
        for the print enviorment
    """

    def test_print_enviorment(self):
        value = 82*82
        list = []
        for i in range(value):
            list.append(random.randint(0,1))
        assert len(list) == value
        BuildFacade.print_enviroment(self,list)

