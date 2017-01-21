import unittest, os
from tests.models.character import test_loader
# TODO: Refine, bitch
aa = unittest.TestResult()
loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(test_loader)
print(type(suite))
runner = unittest.TextTestRunner()
runner.run(suite)