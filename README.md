# python_x3d_toolbox

A collection of Python modules implementing common string and mathematic operations required in reading and writing X3D XML Encoding files.

X3D is a ISO Standard for 3D scenegraphs.

Unless otherwise noted, algorithms will conform to [ISO 19776-1:2015 X3D : XML Encoding 3.3](https://www.web3d.org/documents/specifications/19776-1/V3.3/index.html)

### MFString
Contains a python module mfstring with encode and decode functions for encoding a collection of strings into a single unicode string ready for being encoded as a XML attribute.

References: 
- [X3D XML-Encoding 3.3 Section 5.15 : SFString and MFString](https://www.web3d.org/documents/specifications/19776-1/V3.3/Part01/EncodingOfFields.html#SFString)

- [Discusion of SFString/MFString and survey of X3D implementations](https://github.com/michaliskambi/x3d-tests/wiki/Clarify-the-usage-of-quotes-and-backslashes-for-MFString-and-SFString-in-XML-encoding)

## Dependencies
None beyond standard Python libraries. Developed and tested at Python 3.9

## Testing
Running script `Test.py` with X3dToolkit in the package search path will run all implemented unit tests.
