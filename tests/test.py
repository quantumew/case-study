"""
    Test runner and coverage reporter. Look to htmlcov/index.html for details.
"""

import unittest as unittest
import coverage

if __name__ == "__main__":
    cov = coverage.Coverage(include="./case_study/*.py")
    cov.start()
    all_tests = unittest.TestLoader().discover("tests", pattern="*.py")
    unittest.TextTestRunner().run(all_tests)
    cov.stop()
    cov.save()
    cov.html_report()
