import os
import sys
import json
import string
import random
import logging
import unittest
from time import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Runs once before all tests
        logging.info('Setting up %s', self.__name__)
        self.maxDiff = None

    @classmethod
    def tearDownClass(self):
        # Runs once before all tests
        logging.info('Ending %s', self.__name__)

    def setUp(self):
        # Runs before each test
        logging.info('-'*85)
        logging.info('\t\t\tTest case: %s', self._testMethodName)
        logging.info('-'*85)
        self.start = time()
        return super().setUp()

    def tearDown(self):
        # Runs after each test
        self.end = time()
        logging.info('Elapsed time in seconds: %s', "%.5f" %
                     (self.end - self.start))
        return super().tearDown()


if __name__ == '__main__':
    unittest.main(verbosity=0)
