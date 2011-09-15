import sys
import unittest
import buscape_tests

runner = unittest.TextTestRunner()

if sys.argv[1] in 'fast':
    runner.run(buscape_tests.suite_fast())

if sys.argv[1] in 'request':
    runner.run(buscape_tests.suite_request())
