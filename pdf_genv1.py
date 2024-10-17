# importing modules 
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib import utils

# initializing variables with values 
fileName = 'samplev2.pdf'
documentTitle = 'sample'
title = 'Sofab Inks'
subTitle = 'AHHHHHHH'
textLines = [ 
	'Sticker draft version 2. This is a pdf that can be converted into a sticker,', 
	'and this is filler text. Sticker draft version 2. This is a pdf that can be',
	'converted into a sticker, and this is filler text. Sticker draft version 2.', 
	'This is a pdf that can be converted into a sticker, and this is filler text.',
	'Sticker draft version 2. This is a pdf that can be converted into a sticker,',
	'and this is filler text. Sticker draft version 2. This is a pdf that can be',
	'converted into a sticker, and this is filler text. Sticker draft version 2.', 
]
textLines2 = [
	'Sticker draft version 2. This is a pdf that can be converted into a sticker,', 
	'and this is filler text. Sticker draft version 2. This is a pdf that can be',
	'converted into a sticker, and this is filler text. Sticker draft version 2.', 
	'This is a pdf that can be converted into a sticker, and this is filler text.',

]
batch='Chemical Name:'
size='Size:'
barcode = 'barcode.png'
qrcode= 'qr_code.png'
logo='sofab_logo.png'
flame='flame.png'
date='Date Created:'

# creating a pdf object 
pdf = canvas.Canvas(fileName) 

## change orientation of page
canvas.Canvas.setPageSize(pdf, (landscape(A4)))

# setting the title of the document 
pdf.setTitle(documentTitle) 


# creating the title by setting it's font 
# and putting it on the canvas  
pdf.setFont('Helvetica-Bold', 36) 
pdf.drawCentredString(300, 550, title) 

# creating the subtitle by setting it's font, 
# colour and putting it on the canvas 
pdf.setFillColorRGB(0, 0, 255) 
pdf.setFont("Helvetica-Bold", 24) 
pdf.drawCentredString(290, 600, subTitle) 

# drawing a line 
#pdf.line(10, 25, 550, 25) 
#pdf.line(10, 275, 550, 275) 
# 		x, y, width, height
pdf.rect(10, 25, 565, 245, stroke=1,fill=0)

# creating a multiline text using 
# textline and for loop 
text = pdf.beginText(20, 250) 
text.setFont("Helvetica", 16) 
text.setFillColor(colors.black) 
for line in textLines: 
	text.textLine(line) 
pdf.drawText(text) 

# 2nd text 
text = pdf.beginText(20, 100) 
for line in textLines2: 
	text.textLine(line) 
pdf.drawText(text) 

# chem info
pdf.setFont("Helvetica-Bold", 25) 
pdf.drawString(20, 350, batch) 
pdf.drawString(20, 300, size) 
pdf.drawString(20, 400, date) 


# drawing a image at the 
# specified (x.y) position 
# and scale
pdf.drawInlineImage(barcode, 465, 435, width=200, height=150,preserveAspectRatio=True) 

pdf.drawInlineImage(qrcode, 645, 415, width=200, height=200,preserveAspectRatio=True) 

pdf.drawInlineImage(logo, 10, 440, width=150, height=150,preserveAspectRatio=True) 

pdf.drawInlineImage(flame, 580, 30, width=250, height=300,preserveAspectRatio=True) 

# saving the pdf 
pdf.save() 
