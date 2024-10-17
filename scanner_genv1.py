from barcode import Code128 

# import ImageWriter to generate an image file 
from barcode.writer import ImageWriter 

## 12 char/character
input_string = 'ABC1234567'

my_code = Code128(input_string, writer=ImageWriter()) 

my_code.save("barcode")
