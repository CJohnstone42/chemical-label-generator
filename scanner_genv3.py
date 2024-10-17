import tkinter as tk
from tkinter import messagebox
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode
import os

def generate_barcode(input_string):
    try:
        file_name = "barcode"
        my_code = Code128(input_string, writer=ImageWriter())
        my_code.save(file_name)  # Save the barcode as "barcode.png"
        
        file_path = os.path.abspath(f"{file_name}.png")
        messagebox.showinfo("Success", f"Barcode generated successfully!\nSaved to: {file_path}")
        
        reset_interface()  # Redirect to the selection menu
    except Exception as e:
        messagebox.showerror("Error", str(e))

def generate_qr_code(input_string):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(input_string)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        file_name = "qr_code"
        img.save(f"{file_name}.png")

        file_path = os.path.abspath(f"{file_name}.png")
        messagebox.showinfo("Success", f"QR Code generated successfully!\nSaved to: {file_path}")

        reset_interface()  # Redirect to the selection menu
    except Exception as e:
        messagebox.showerror("Error", str(e))

def setup_generator(generator_type):
    # Show requirement labels and input entry
    requirement_label.pack()
    entry.pack()
    
    if generator_type == 'barcode':
        rules_label.pack()
        generate_button.config(command=lambda: generate_barcode(entry.get()))
    else:
        generate_button.config(command=lambda: generate_qr_code(entry.get()))
    
    generate_button.pack(pady=20)

def reset_interface():
    # Hide requirement labels and input entry
    requirement_label.pack_forget()
    rules_label.pack_forget()
    entry.pack_forget()
    generate_button.pack_forget()
    
    # Show type selection buttons again
    type_selection_frame.pack(pady=20)

def choose_type_barcode():
    setup_generator('barcode')
    type_selection_frame.pack_forget()  # Hide the type selection frame

def choose_type_qr_code():
    setup_generator('qr_code')
    type_selection_frame.pack_forget()  # Hide the type selection frame

# Set up the main application window
root = tk.Tk()
root.title("Barcode/QR Code Generator")

# Create frames for type selection
type_selection_frame = tk.Frame(root)
type_selection_frame.pack(pady=20)

# Create buttons for selection
barcode_button = tk.Button(type_selection_frame, text="Generate Barcode", command=choose_type_barcode)
qr_code_button = tk.Button(type_selection_frame, text="Generate QR Code", command=choose_type_qr_code)

barcode_button.pack(side=tk.LEFT, padx=10)
qr_code_button.pack(side=tk.LEFT, padx=10)

# Create labels for requirements
requirement_label = tk.Label(root, text="Enter a 12-character string for the barcode,\n Or a link for the QR Code:")
rules_label = tk.Label(root, text="For Bar Codes:\nBatches start with '0',\nExperiments start with a character.")

# Create and place the input entry
entry = tk.Entry(root, width=40)  # Adjust width as needed

# Create and place the generate button
generate_button = tk.Button(root, text="Generate", command=None)

# Start the main event loop
root.mainloop()
