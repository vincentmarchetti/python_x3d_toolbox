# SPDX-FileCopyrightText: 2024 Vincent Marchetti
#
# SPDX-License-Identifier: MIT

__all__ = ['encode', 'decode']

import logging
logger = logging.getLogger("x3d-toolbox.mfstring")
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
ITEM_SEPARATORS = u", \n\r\t" # allowed without warning between list items

from io import StringIO

class SlashEncodingError(ValueError):
    "Exception thrown when an a string cannot be slash-decoded"
    
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
            elif c not in ITEM_SEPARATORS:
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
                    
                    
                    
            
    

