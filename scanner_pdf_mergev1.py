import tkinter as tk
from tkinter import messagebox
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode
import os
from reportlab.pdfgen import canvas 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import landscape, A4

def generate_barcode(input_string):
    try:
        file_name = "barcode"
        my_code = Code128(input_string, writer=ImageWriter())
        my_code.save(file_name)  # Save the barcode as "barcode.png"
        return f"{file_name}.png"  # Return the file path for later use
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def generate_qr_code(input_string):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(input_string)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        file_name = "qr_code"
        img.save(f"{file_name}.png")
        return f"{file_name}.png"  # Return the file path for later use
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def generate_pdf(batch, size, date, barcode_path, qr_code_path):
    fileName = 'output.pdf'
    documentTitle = 'Generated PDF'
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
    
    # Paths for additional images
    logo = 'sofab_logo.png'  # Update with the correct path
    flame = 'flame.png'      # Update with the correct path

    # Creating a pdf object 
    pdf = canvas.Canvas(fileName) 
    pdf.setPageSize(landscape(A4))
    pdf.setTitle(documentTitle) 

    pdf.setFont('Helvetica-Bold', 36) 
    pdf.drawCentredString(300, 550, title) 

    pdf.setFillColorRGB(0, 0, 255) 
    pdf.setFont("Helvetica-Bold", 24) 
    pdf.drawCentredString(290, 600, subTitle) 

    pdf.rect(10, 25, 565, 245, stroke=1, fill=0)

    # Creating multiline text using textLines and a loop
    text = pdf.beginText(20, 250) 
    text.setFont("Helvetica", 16) 
    text.setFillColor(colors.black) 
    for line in textLines: 
        text.textLine(line) 
    pdf.drawText(text) 

    # Draw chemical info
    pdf.setFont("Helvetica-Bold", 25) 
    pdf.drawString(20, 350, 'Chemical Name:') 
    pdf.setFont("Helvetica", 25) 
    pdf.drawString(250, 350, batch) 

    pdf.setFont("Helvetica-Bold", 25) 
    pdf.drawString(20, 300, 'Size:') 
    pdf.setFont("Helvetica", 25) 
    pdf.drawString(250, 300, size) 

    pdf.setFont("Helvetica-Bold", 25) 
    pdf.drawString(20, 400, 'Date Created:') 
    pdf.setFont("Helvetica", 25) 
    pdf.drawString(250, 400, date) 

    # Draw barcode and QR code images
    if barcode_path:
        pdf.drawInlineImage(barcode_path, 460, 435, width=200, height=150)
    if qr_code_path:
        pdf.drawInlineImage(qr_code_path, 645, 415, width=200, height=200)

    # Draw additional images
    pdf.drawInlineImage(logo, 10, 440, width=150, height=150) 
    pdf.drawInlineImage(flame, 580, 30, width=250, height=300, preserveAspectRatio=True) 

    # Saving the pdf 
    pdf.save()

def on_submit():
    batch = batch_entry.get()
    size = size_entry.get()
    date = date_entry.get()
    barcode_input = barcode_entry.get()
    qr_code_input = qr_code_entry.get()

    # Generate barcode and QR code
    barcode_path = generate_barcode(barcode_input)
    qr_code_path = generate_qr_code(qr_code_input)

    # Create PDF with the collected data
    generate_pdf(batch, size, date, barcode_path, qr_code_path)
    messagebox.showinfo("Success", "PDF generated successfully!")

def setup_interface():
    # Create labels and entry fields for inputs
    tk.Label(root, text="Chemical Name:").grid(row=0, column=0)
    tk.Label(root, text="Size:").grid(row=1, column=0)
    tk.Label(root, text="Date Created:").grid(row=2, column=0)
    tk.Label(root, text="Barcode Data:").grid(row=3, column=0)
    tk.Label(root, text="QR Code Data:").grid(row=4, column=0)
    
    global batch_entry, size_entry, date_entry, barcode_entry, qr_code_entry
    batch_entry = tk.Entry(root)
    size_entry = tk.Entry(root)
    date_entry = tk.Entry(root)
    barcode_entry = tk.Entry(root)
    qr_code_entry = tk.Entry(root)
    
    batch_entry.grid(row=0, column=1)
    size_entry.grid(row=1, column=1)
    date_entry.grid(row=2, column=1)
    barcode_entry.grid(row=3, column=1)
    qr_code_entry.grid(row=4, column=1)
    
    # Submit button
    submit_button = tk.Button(root, text="Generate PDF", command=on_submit)
    submit_button.grid(row=5, columnspan=2, pady=20)

# Set up the main application window
root = tk.Tk()
root.title("Barcode/QR Code & PDF Generator")

setup_interface()

# Start the main event loop
root.mainloop()
