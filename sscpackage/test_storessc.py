import unittest
from mysql.connector import connect, Error
import json
import os
import simplestockchecker_parsetool as sscp
import pandas as pd

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
