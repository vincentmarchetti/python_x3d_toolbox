import  unittest 


from . import mfstring
    
class SlashEncodingTest(unittest.TestCase):
    def __init__(self, original, encoded, *tups, **keyw):
        self.original = original
        self.encoded  = encoded
        unittest.TestCase.__init__(self,*tups, **keyw)
        
    def shortDescription(self):
        return "slash encoding %s ==> %s" % (self.original, self.encoded)
        
    def runTest(self):
        test = mfstring.slash_encode(self.original)
        self.assertEqual(self.encoded, test)
        
class SlashDecodingTest(unittest.TestCase):
    def __init__(self, original, encoded, *tups, **keyw):
        self.original = original
        self.encoded  = encoded
        unittest.TestCase.__init__(self,*tups, **keyw)
        
    def shortDescription(self):
        return "slash decoding %s ==> %s" % (self.encoded, self.original)
        
    def runTest(self):
        test = mfstring.slash_decode(self.encoded)
        self.assertEqual(self.original, test)

class ListTests(unittest.TestCase):
    
    def test10(self):
        "Basic mfstring encoding"        
        inList = [u'apple', u'pear']
        goodResult= u'"apple" "pear"'
        
        test = mfstring.encode( inList )
        self.assertEqual(goodResult, test)
        
    def test20(self):
        "Empty mfstring encoding"        
        inList = []
        goodResult= u''
        
        test = mfstring.encode( inList )
        self.assertEqual(goodResult, test)
        
    def test30(self):
        "Empty mfstring decoding"        
        inStr = ''
        goodResult= []
        
        test = mfstring.decode( inStr )
        self.assertEqual(goodResult, test)

        
    def test40(self):
        "roundtrip encode - decode 1"        
        inList = ['apple' , 'final slash\\']
        encoded = mfstring.encode( inList)
        roundTripped = mfstring.decode(encoded)
        self.assertEqual(inList, roundTripped)
        
    def test42(self):
        "roundtrip encode - decode 2"        
        inList = ['apple' , 'internal \\" quote']
        encoded = mfstring.encode( inList)
        roundTripped = mfstring.decode(encoded)
        self.assertEqual(inList, roundTripped)
        
    def test50(self):
        "raise ValueError for invalid MFString encoding"         
        # this is string which cannot be decoded as MFString values
        testStr = '"apple" "this item never ends\\"'
        self.assertRaises(ValueError, mfstring.decode, testStr)

slash_escaping_test = [
    (u'apple'           , u'apple'),
    (u'"initial quote' , u'\\"initial quote'),
    (u'final quote"'     , u'final quote\\"'),
    (u'internal " quote', u'internal \\" quote'),
    (u'""'              , u'\\"\\"'),
    (u'final slash\\'   , u'final slash\\\\'),
    (u''                , u'')  # this is empty string --> empty string test    
]    
    
class PartialDecodingTest(unittest.TestCase):
    """
    tests to develop a version of mfstring decoding that will
    allow for partial return of an MFString value; if one (or more)
    of the elements is invalid the others will still be returned
    """
    
    def test10(self):
        "partial return with warning message"
        
        encodedSFStrings = [
            r'MFString in classic encoding.',
            r'You should see single backslash: \\',
            r'You should see double qoute: \"',
            #r'This is invalid \blahblah',
            #r'C:/Users/data/Temp/..\maya\projects\untitled-files\Default.tif'
            ]
        encoded_value=" ".join(
            [ ('"%s"' % v) for v in encodedSFStrings ]
        )
        
        value = mfstring.decode(encoded_value)
        # should be one fewer value in the returned Python list
        self.assertEqual(len(encodedSFStrings) , len(value))
    
# loading up a suite of tests            
suite = unittest.TestSuite()

for pair in slash_escaping_test[0:0]:
    suite.addTest( SlashEncodingTest(pair[0], pair[1]))
    suite.addTest( SlashDecodingTest(pair[0], pair[1]))

#suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( ListTests )  )
suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( PartialDecodingTest ) ) 
  
   
if __name__ == '__main__':

    # Achieving the formatting I like
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
