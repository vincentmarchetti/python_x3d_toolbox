__all__ = ['encode','decode']

# MIT License
# 
# Copyright (c) 2024 Vincent Marchetti
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging
logger = logging.getLogger("MFStringEscaping")
logger.addHandler( logging.NullHandler() )
logger.setLevel( logging.WARN )

"""
Python (targeting 3.7) implementation of the rules for
encoding X3D MFString values into a single unicode string.
The intent is that this single unicode string is then further encoded
into a string appropriate for storage in an XML attribute value.
"""

BACKSLASH=u"\u005C"   # unicode REVERSE_SOLIDUS, the \ character
QUOTE_MARK= u"\u0022" # double quotes "
SPACE=u" "

from io import StringIO

class SlashEncodingError(ValueError):
    "Exception thrown when an a string cannot be decoded"
    
    def __init__(self,xString, *tups, **keyw):
        """initialize SlashEncodingError
                
        xString: the unicode string that fails as argument to slash_decoding
        """
        Exception.__init__(self,xString, *tups, **keyw)
        
    def __str__(self):
        return "invalid slash-encoded value: {%s}" % self.args[0]
        
class ListEncodingError(ValueError):
    "Exception thrown when an a string cannot be decoded as a list of strings"
    def __init__(self,xString, *tups, **keyw):
        """initialize ListEncodingError
        
        xString : the unicode string that fails as argument to decoding
        """
        Exception.__init__(self,xString, *tups, **keyw)
        
    def __str__(self):
        return "invalid slash-encoded value: {%s}" % self.args[0]


def slash_encode(aString):
    """Applies escaping to backslash and quote character
        
    Applied to elements of an MFString collection to allow the complete
    list to be encoded as a space delimited list of strings enclosed in unescaped quotes
    
    This method is exposed for the purpose of testing. It is applied to the
    elements of an MFString as part of the encode function. Users of this module will
    not have to call this function.
    
    aString : arbitrary unicode string
    return :  unicode string with \ --> \\ ; " --> \" replacements
    """
    rv=StringIO()
    for c in aString:
        if c == BACKSLASH or c==QUOTE_MARK:
            rv.write(BACKSLASH)
        rv.write(c)
    return rv.getvalue()
    

def slash_decode( xString ):
    """Reverses the slash_encoding
    
    This method is exposed for the purpose of testing. It is applied to the
    elements of an MFString as part of the decode function. Users of this module will
    not have to call this function.

    xString : a unicode string that is the result of an application of the slash_encode algorithm
        
    returns : The string that would be encoded to xString
    """
    rv=StringIO()
    escaping = False
    for c in xString:
        if escaping:
            if c==BACKSLASH or c==QUOTE_MARK:
                rv.write(c)                    
            else:
                raise SlashEncodingError(xString)
            escaping = False
        else: # not escaping
            if c==BACKSLASH:
                escaping = True
            else:
                rv.write(c)
    if escaping:
        raise SlashEncodingError(xString) 
    return rv.getvalue()   
                
    

def encode( aList):
    """Encode a list of unicode strings to a single unicode string
    
    The return value of this function will be passed to the function that applies
    the escaping and encoding required to render it as XML attribute value
    as specified in the XML reference document 
    https://www.w3.org/TR/2008/REC-xml-20081126
    
    
    input argument: a sequence of unicode strings
    returns: a unicode string
    """
    slash_encoded_items = [slash_encode(s) for s in aList ]
    quoted_items = ['"%s"' % item for item in slash_encoded_items]
    return SPACE.join(quoted_items)

    
whitespace = u" \n\r\t" # space, newlines, carriage returns, tab
def decode( mfstring_enc ):
    """Decode unicode string into a list of unicode strings
    
    
    This method is to be applied to the normalized attribute value, the
    result of appluing the algorithm specified in the section 3.3.3 of the
    XML reference document
    https://www.w3.org/TR/2008/REC-xml-20081126/#AVNormalize
    
    mfstring_enc : A unicode string, the result of the application of the encode function
    returns : Python list of unicode strings
    """
    retVal = []
    looking_for_delim = True
    escaping = False
    ix_start = -1
    for ix,c in enumerate(mfstring_enc):
        if looking_for_delim:
            if c==QUOTE_MARK:
                looking_for_delim = False
                escaping = False
                ix_start=ix+1
            elif c not in whitespace:
                logger.warning("unexpected character %r between MFString items" % c)
                
        else:
            if c==BACKSLASH:
                escaping = not escaping
            elif c==QUOTE_MARK:
                if not escaping:
                    retVal.append(slash_decode(mfstring_enc[ix_start:ix]))
                    looking_for_delim = True
                escaping = False
    
    if not looking_for_delim:
        raise ListEncodingError( mfstring_enc )
    return retVal                        
                    
                    
                    
            
    

