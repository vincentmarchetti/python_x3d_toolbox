"""
To be run as a script to run all available unittests in the
X3DToolkit package
"""

import unittest

suite = unittest.TestSuite()

from  X3dToolkit.MFStringTest import suite as MFStringSuite
suite.addTest( MFStringSuite )


if __name__ == '__main__':

    # Achieving the desired one line per test formatting 
    class TextTestResult(unittest.TextTestResult):
        def getDescription(self, test):
            return test.shortDescription()

    class TextTestRunner(unittest.TextTestRunner):
        resultclass = TextTestResult


    # if desired, combine logging and testing
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.WARN)
    
    TextTestRunner(verbosity=2).run(suite)
