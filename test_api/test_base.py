import os
import sys
import json
import string
import random
import unittest
from time import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app import app, headers
from utils.log import log
log = log.getLogger('TestBase')


class TestBase(unittest.TestCase):
    '''
        Base class for testing AWS Lambda API's
        
    '''

    @classmethod
    def setUpClass(self):
        # Runs once before all tests
        log.info('Setting up %s', self.__name__)
        self.maxDiff = None
        # self.sortTestMethodsUsing = None
        self.client = app.test_client()
    
    @classmethod
    def tearDownClass(self):
        # Runs once before all tests
        log.info('Ending %s', self.__name__)

    def setUp(self):
        # Runs before each test
        log.info('-'*85)
        log.info('\t\t\tTest case: %s', self._testMethodName)
        log.info('-'*85)
        self.start = time()
        return super().setUp()
    
    def tearDown(self):
        # Runs after each test
        self.end = time()
        log.info('Elapsed time in seconds: %s', "%.5f" % (self.end - self.start))
        return super().tearDown()

    def check_message(self, response, message={}, code=200):
        try:
            resp = json.loads(response.text)
        except Exception:
            resp = response.json
        
        self.assertEqual(response.status_code, code)
        self.assertEqual(
            resp, 
            {
                'message': message,
                'headers': headers
            }
        )
    
    def check_error(self, response, error='', code=400):
        try:
            resp = response.json
        except Exception:
            resp = json.loads(response.text)
        
        self.assertEqual(response.status_code, code)
        self.assertEqual(
            resp, 
            {
                'error': error,
                'headers': headers
            }
        )
    
    def generate_rand_string(self, length=32):
        characters = string.ascii_letters + string.digits # + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    # def test_something(self):
    #     self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main(verbosity=0)