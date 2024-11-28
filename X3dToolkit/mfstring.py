__all__ = ['encode','decode']

import logging
logger = logging.getLogger("MFStringEscaping")
logger.addHandler( logging.NullHandler() )
logger.setLevel( logging.WARN )

"""
Python (targeting 3.7) implementation of the rules for
encoding X3D MFString values into a single unicode string.
The intent is that this single unicode string is then further encoded
into a string appropriate for storage in an XML attribute value.

Also includes 
"""

BACKSLASH=u"\u005C"   # unicode REVERSE_SOLIDUS, the \ character
QUOTE_MARK= u"\u0022" # double quotes "
SPACE=u" "

from io import StringIO

class SlashEncodingError(ValueError):
    def __init__(self,xString, *tups, **keyw):
        """
        xString a unicode string that fails as argument to slash_decoding
        """
        Exception.__init__(self,xString, *tups, **keyw)
        
    def __str__(self):
        return "invalid slash-encoded value: {%s}" % self.args[0]
        
class ListEncodingError(ValueError):
    def __init__(self,xString, *tups, **keyw):
        """
        xString a unicode string that fails as argument to decoding
        """
        Exception.__init__(self,xString, *tups, **keyw)
        
    def __str__(self):
        return "invalid slash-encoded value: {%s}" % self.args[0]


def slash_encode(aString):
    """
    input arbitrary unicode string
    return unicode string with \ --> \\ ; " --> \" replacements
    """
    rv=StringIO()
    for c in aString:
        if c == BACKSLASH or c==QUOTE_MARK:
            rv.write(BACKSLASH)
        rv.write(c)
    return rv.getvalue()
    

def slash_decode( xString ):
    """
    xString : a unicode string that meets requirements of encoding,
        namely QUOTE_MARK and BACKSLASH are always part of of
        an escaped pair
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
    """
    input argument: a sequence of unicode strings
    returns: a unicode string
    """
    slash_encoded_items = [slash_encode(s) for s in aList ]
    quoted_items = ['"%s"' % item for item in slash_encoded_items]
    return SPACE.join(quoted_items)

    
whitespace = u" \n\r\t"
def decode( mfstring_enc ):
    """
    input : a unicode string
    output: Python list of unicode strings
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
                    
                    
                    
            
    

