import tkinter as tk
from tkinter import messagebox
from barcode import Code128
from barcode.writer import ImageWriter
import os

def generate_barcode():
    input_string = entry.get()
    
    if len(input_string) != 12:
        messagebox.showwarning("Input Error", "Please enter exactly 12 characters.")
        return

    try:
        # Create the barcode
        file_name = "barcode"
        my_code = Code128(input_string, writer=ImageWriter())
        my_code.save(file_name)  # Save the barcode as "barcode.png"
        
        # Get the full path where the file is saved
        file_path = os.path.abspath(f"{file_name}.png")
        messagebox.showinfo("Success", f"Barcode generated successfully!\nSaved to: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Set up the main application window
root = tk.Tk()
root.title("Barcode Generator")

# Create a label to indicate the requirement for input
requirement_label = tk.Label(root, text="Enter a 12-character string for the barcode:")
requirement_label.pack(pady=10)

# Create a second label to indicate batch and experiment rules
rules_label = tk.Label(root, text="Batches start with '0',\nExperiments start with a character.")
rules_label.pack(pady=5)

# Create and place the input entry
entry = tk.Entry(root, width=40)  # Adjust width as needed
entry.pack(pady=5)

# Create and place the generate button
generate_button = tk.Button(root, text="Generate Barcode", command=generate_barcode)
generate_button.pack(pady=20)

# Start the main event loop
root.mainloop()
