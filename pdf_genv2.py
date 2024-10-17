# importing modules 
from reportlab.pdfgen import canvas 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import landscape, A4
from tkinter import Tk, Label, Entry, Button

# Function to generate PDF
def generate_pdf(batch, size, date):
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

    barcode = 'barcode.png'
    qrcode = 'qr_code.png'
    logo = 'sofab_logo.png'
    flame = 'flame.png'

    # creating a pdf object 
    pdf = canvas.Canvas(fileName) 

    # change orientation of page
    pdf.setPageSize(landscape(A4))

    # setting the title of the document 
    pdf.setTitle(documentTitle) 

    # creating the title by setting its font 
    pdf.setFont('Helvetica-Bold', 36) 
    pdf.drawCentredString(300, 550, title) 

    # creating the subtitle by setting its font, 
    # colour and putting it on the canvas 
    pdf.setFillColorRGB(0, 0, 255) 
    pdf.setFont("Helvetica-Bold", 24) 
    pdf.drawCentredString(290, 600, subTitle) 

    # drawing a line 
    pdf.rect(10, 25, 565, 245, stroke=1, fill=0)

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
    pdf.drawString(20, 350, 'Chemical Name:') 
    pdf.setFont("Helvetica", 25)  # Set to regular font for user input
    pdf.drawString(250, 350, batch) 

    pdf.setFont("Helvetica-Bold", 25) 
    pdf.drawString(20, 300, 'Size:') 
    pdf.setFont("Helvetica", 25)  # Set to regular font for user input
    pdf.drawString(250, 300, size) 

    pdf.setFont("Helvetica-Bold", 25) 
    pdf.drawString(20, 400, 'Date Created:') 
    pdf.setFont("Helvetica", 25)  # Set to regular font for user input
    pdf.drawString(250, 400, date) 

    # drawing a image at the specified (x.y) position and scale
    pdf.drawInlineImage(barcode, 465, 435, width=200, height=150, preserveAspectRatio=True) 
    pdf.drawInlineImage(qrcode, 645, 415, width=200, height=200, preserveAspectRatio=True) 
    pdf.drawInlineImage(logo, 10, 440, width=150, height=150, preserveAspectRatio=True) 
    pdf.drawInlineImage(flame, 580, 30, width=250, height=300, preserveAspectRatio=True) 

    # saving the pdf 
    pdf.save()

# Function to handle the button click
def on_submit():
    batch = batch_entry.get()
    size = size_entry.get()
    date = date_entry.get()
    generate_pdf(batch, size, date)
    root.destroy()  # Close the Tkinter window

# Creating a Tkinter window
root = Tk()
root.title("Input Information")

# Creating labels and entry fields
Label(root, text="Chemical Name:").grid(row=0, column=0)
batch_entry = Entry(root)
batch_entry.grid(row=0, column=1)

Label(root, text="Size:").grid(row=1, column=0)
size_entry = Entry(root)
size_entry.grid(row=1, column=1)

Label(root, text="Date Created:").grid(row=2, column=0)
date_entry = Entry(root)
date_entry.grid(row=2, column=1)

# Submit button
submit_button = Button(root, text="Generate PDF", command=on_submit)
submit_button.grid(row=3, columnspan=2)

# Start the Tkinter main loop
root.mainloop()
