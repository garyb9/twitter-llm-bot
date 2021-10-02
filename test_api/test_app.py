import unittest
from test_base import TestBase
from utils.log import log
log = log.getLogger('TestApp')

class TestApp(TestBase):
    '''
        Test Flask app is a unittest class for testing flask app api service before deployment.
        
    '''

    def test_root(self):
        response = self.client.get('/')
        self.check_message(response=response, message='root', code=200)

if __name__ == '__main__':
    unittest.main(verbosity=0)