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

    """
        The test method for the stacking value in the  build Facade
    """
    def test_stacked_value(self):
        list=[1]
        n_list = BuildFacade.stacked_enviorment(self,list)
        assert len(list) == 4

    """
        Test method if the list is empty
    """
    def test_stacked_value_of_list(self):
        list=[]
        n_list = BuildFacade.stacked_enviorment(self,list)
        assert len(list) ==0