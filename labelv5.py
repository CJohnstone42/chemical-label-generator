import tkinter as tk
from tkinter import ttk, messagebox
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode
from reportlab.pdfgen import canvas 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch

# Dark theme colors
BACKGROUND_COLOR = "#2E2E2E" #gray
TEXT_COLOR = "#FFFFFF"  #white
BUTTON_COLOR = "#4A4A4A"    #dark gray
HIGHLIGHT_COLOR = "#3E3E3E" #light gray
ENTRY_COLOR = "#4A4A4A" #dark gray

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

def generate_pdf(batch, date, concentration, volume, barcode_path, qr_code_path, page_size, text):
    fileName = 'output.pdf'
    documentTitle = 'Generated PDF'
    
    # Paths for additional images
    logo = 'soFabLogo2.png'  # Update with the correct path
    flame = 'flame.png'      # Update with the correct path

    # Creating a pdf object 
    pdf = canvas.Canvas(fileName) 
    pdf.setPageSize(page_size)
    pdf.setTitle(documentTitle) 

    pdf.rect(10, 25, 565, 245, stroke=1, fill=0)

    # Adding multiline text from the Text widget
    pdf.setFont("Helvetica", 16)
    pdf.setFillColor(colors.black) 
    text_obj = pdf.beginText(20, 250)
    for line in text.splitlines():
        text_obj.textLine(line)
    pdf.drawText(text_obj)

    # Draw chemical info
    pdf.setFont("Helvetica-Bold", 25) 
    pdf.drawString(20, 350, 'Chemical Name:') 
    pdf.setFont("Helvetica", 25) 
    pdf.drawString(250, 350, batch) 

    pdf.setFont("Helvetica-Bold", 25) 
    pdf.drawString(20, 300, 'Volume:') 
    pdf.setFont("Helvetica", 25) 
    pdf.drawString(250, 300, volume) 

    pdf.setFont("Helvetica-Bold", 25) 
    pdf.drawString(20, 450, 'Concentration:') 
    pdf.setFont("Helvetica", 25) 
    pdf.drawString(250, 300, concentration) 

    pdf.setFont("Helvetica-Bold", 25) 
    pdf.drawString(20, 400, 'Date Created:') 
    pdf.setFont("Helvetica", 25) 
    pdf.drawString(250, 400, date) 

    # Draw barcode and QR code images
    if barcode_path:
        pdf.drawInlineImage(barcode_path, 460, 435, width=200, height=150)
    if qr_code_path:
        pdf.drawInlineImage(qr_code_path, 645, 415, width=200, height=200)

    # Draw additional images (logo and flame)
    pdf.drawInlineImage(logo, 0, 475, width=None, height=None, preserveAspectRatio=True) 
    pdf.drawInlineImage(flame, 580, 30, width=250, height=300, preserveAspectRatio=True) 

    # Add precautions text
    #pdf.setFont("Helvetica-Bold", 25) 
    #pdf.drawString(20, 450, 'Precautions:') 
    #pdf.setFont("Helvetica", 16)
    #precaution_text_obj = pdf.beginText(20, 420)
    #for line in precautions.splitlines():
    #    precaution_text_obj.textLine(line)
    #pdf.drawText(precaution_text_obj)

    # Saving the pdf 
    pdf.save()

def on_submit():
    batch = batch_entry.get()
#    size = size_entry.get()
    date = date_entry.get()
    volume = volume_entry.get()
    concentration = concentration_entry.get()
    barcode_input = barcode_entry.get()
    qr_code_input = qr_code_entry.get()
    page_size_option = page_size_var.get()
    text = text_box.get("1.0", tk.END).strip()  # Get text from the Text widget
    #precautions = precaution_box.get("1.0", tk.END).strip()  # Get precautions from the Text widget

    # Set page size based on user selection
    page_size = landscape(A4) if page_size_option == "Landscape" else A4

    barcode_path = generate_barcode(barcode_input)
    qr_code_path = generate_qr_code(qr_code_input)
    generate_pdf(batch, date, concentration, volume, barcode_path, qr_code_path, page_size, text)

# Set up GUI interface
def setup_interface():
    global batch_entry, volume_entry, concentration_entry, date_entry, barcode_entry, qr_code_entry
    global page_size_var, hazard_type_var, text_box, checkbox_frame, precaution_frame
    global precaution_type_var, precaution_box, precaution_checkbox_frame, checkbox_vars
    global hazard_checkbox_vars, precaution_checkbox_vars

    notebook = ttk.Notebook(root)
    
    # First tab for Chemical Details
    chemical_frame = ttk.Frame(notebook, style="TFrame")
    notebook.add(chemical_frame, text="Chemical Details")

    tk.Label(chemical_frame, text="Chemical Name:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=5)
    batch_entry = tk.Entry(chemical_frame, bg=ENTRY_COLOR, fg=TEXT_COLOR)
    batch_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(chemical_frame, text="Volume:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=5)
    volume_entry = tk.Entry(chemical_frame, bg=ENTRY_COLOR, fg=TEXT_COLOR)
    volume_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(chemical_frame, text="Concentration:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, padx=10, pady=5)
    concentration_entry = tk.Entry(chemical_frame, bg=ENTRY_COLOR, fg=TEXT_COLOR)
    concentration_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(chemical_frame, text="Date Created:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=4, column=0, padx=10, pady=5)
    date_entry = tk.Entry(chemical_frame, bg=ENTRY_COLOR, fg=TEXT_COLOR)
    date_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(chemical_frame, text="Barcode Input:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=5, column=0, padx=10, pady=5)
    barcode_entry = tk.Entry(chemical_frame, bg=ENTRY_COLOR, fg=TEXT_COLOR)
    barcode_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(chemical_frame, text="QR Code Input:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=6, column=0, padx=10, pady=5)
    qr_code_entry = tk.Entry(chemical_frame, bg=ENTRY_COLOR, fg=TEXT_COLOR)
    qr_code_entry.grid(row=6, column=1, padx=10, pady=5)

    # Page size selection
    tk.Label(chemical_frame, text="Page Size:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=7, column=0, padx=10, pady=5)
    page_size_var = tk.StringVar(value="Portrait")  # Default value
    page_size_menu = ttk.OptionMenu(chemical_frame, page_size_var, "Portrait", "Portrait", "Landscape")
    page_size_menu.grid(row=7, column=1, padx=10, pady=5)

    # Second tab for Hazard Details
    hazard_frame = ttk.Frame(notebook)
    notebook.add(hazard_frame, text="Hazard Details")

    # Signal Word selection
    hazard_type_var = tk.StringVar(value="H2")  # Default value

    hazard_type_menu = tk.OptionMenu(hazard_frame, hazard_type_var, 
        "Physical Hazards (H2)", 
        "Health Hazards (H3)", 
        "Environmental Hazards (H4)")
    hazard_type_menu.config(bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=HIGHLIGHT_COLOR)
    tk.Label(hazard_frame, text="Select Hazard Type:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=5)
    hazard_type_menu.grid(row=0, column=1, padx=10, pady=5)

    # Textbox for hazard details
    text_box = tk.Text(hazard_frame, height=5, width=40, bg=ENTRY_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
    text_box.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    # Frame for hazard checkboxes
    checkbox_frame = tk.Frame(hazard_frame, bg=BACKGROUND_COLOR)
    checkbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    # List to keep track of hazard checkbox variables
    hazard_checkbox_vars = [] 
    checkbox_vars = [] 

    # Function to update checkboxes when hazard type changes
    hazard_type_var.trace_add("write", lambda *args: update_hazard_checkboxes(checkbox_frame))

    # Third tab for Precautionary Type
    precaution_frame = ttk.Frame(notebook)
    notebook.add(precaution_frame, text="Precautionary Details")

    # Precautionary Type selection
    precaution_type_var = tk.StringVar(value="P1")  # Default value
    precaution_type_menu = tk.OptionMenu(precaution_frame, precaution_type_var,
        "General precautionary statements (P1)", 
        "Prevention precautionary statements (P2)", 
        "Response precautionary statements (P3)", 
        "Storage precautionary statements (P4)", 
        "Disposal precautionary statements (P5)")
    precaution_type_menu.config(bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=HIGHLIGHT_COLOR)
    tk.Label(precaution_frame, text="Select Precautionary Type:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=5)
    precaution_type_menu.grid(row=0, column=1, padx=10, pady=5)

    # Precaution description text box
    precaution_box = tk.Text(precaution_frame, height=5, width=40, bg=ENTRY_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
    precaution_box.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    # Frame for precautionary checkboxes
    precaution_checkbox_frame = tk.Frame(precaution_frame, bg=BACKGROUND_COLOR)
    precaution_checkbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    # List to keep track of precaution checkbox variables
    precaution_checkbox_vars = [] 

    # Generate PDF button
    # Generate PDF button
    generate_button = tk.Button(precaution_frame, text="Generate PDF", command=on_submit, bg=BUTTON_COLOR, fg=TEXT_COLOR)
    generate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    precaution_type_var.trace_add("write", lambda *args: update_precautionary_checkboxes(precaution_checkbox_frame))

    notebook.pack(expand=True, fill='both')
#######################################################################
def update_hazard_checkboxes(checkbox_frame):
    global checkbox_vars  # Ensure we're using the global variable
    # Clear existing checkboxes
    for widget in checkbox_frame.winfo_children():
        widget.destroy()

    # Check if the selected hazard type is "Physical Hazards"
    if hazard_type_var.get() == "Physical Hazards (H2)":
        hazards = [
            "H200 Unstable explosive",
            "H201 Explosive; mass explosion hazard",
            "H202 Explosive; severe projection hazard",
            "H203 Explosive; fire, blast or projection hazard",
            "H204 Fire or projection hazard",
            "H205 May mass explode in fire",
            "H206 Fire, blast or projection hazard; increased risk of explosion if desensitizing agent is reduced",
            "H207 Fire or projection hazard; increased risk of explosion if desensitizing agent is reduced",
            "H208 Fire hazard; increased risk of explosion if desensitizing agent is reduced",
            "H220 Extremely flammable gas",
            "H221 Flammable gas",
            "H222 Extremely flammable aerosol",
            "H223 Flammable aerosol",
            "H224 Extremely flammable liquid and vapour",
            "H225 Highly flammable liquid and vapour",
            "H226 Flammable liquid and vapour",
            "H227 Combustible liquid",
            "H228 Flammable solid",
            "H229 Pressurized container: may burst if heated",
            "H230 May react explosively even in the absence of air",
            "H231 May react explosively even in the absence of air at elevated pressure and/or temperature",
            "H232 May ignite spontaneously if exposed to air",
            "H240 Heating may cause an explosion",
            "H241 Heating may cause a fire or explosion",
            "H242 Heating may cause a fire",
            "H250 Catches fire spontaneously if exposed to air",
            "H251 Self-heating; may catch fire",
            "H252 Self-heating in large quantities; may catch fire",
            "H260 In contact with water releases flammable gases which may ignite spontaneously",
            "H261 In contact with water releases flammable gas",
            "H270 May cause or intensify fire; oxidizer",
            "H271 May cause fire or explosion; strong oxidizer",
            "H272 May intensify fire; oxidizer",
            "H280 Contains gas under pressure; may explode if heated",
            "H281 Contains refrigerated gas; may cause cryogenic burns or injury",
            "H290 May be corrosive to metals"
        ]

        # Create checkboxes for each hazard
        for hazard in hazards:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(checkbox_frame, text=hazard, variable=var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR)
            checkbox.pack(anchor='w')
            checkbox_vars.append((var, hazard))  # Keep track of checkbox vars and labels

    # Check if the selected hazard type is "Health Hazards"
    elif hazard_type_var.get() == "Health Hazards (H3)":
        health_hazards = [
            "H300 Fatal if swallowed",
            "H301 Toxic if swallowed",
            "H302 Harmful if swallowed",
            "H303 May be harmful if swallowed",
            "H304 May be fatal if swallowed and enters airways",
            "H305 May be harmful if swallowed and enters airways",
            "H310 Fatal in contact with skin",
            "H311 Toxic in contact with skin",
            "H312 Harmful in contact with skin",
            "H313 May be harmful in contact with skin",
            "H314 Causes severe skin burns and eye damage",
            "H315 Causes skin irritation",
            "H316 Causes mild skin irritation",
            "H317 May cause an allergic skin reaction",
            "H318 Causes serious eye damage",
            "H319 Causes serious eye irritation",
            "H320 Causes eye irritation",
            "H330 Fatal if inhaled",
            "H331 Toxic if inhaled",
            "H332 Harmful if inhaled",
            "H333 May be harmful if inhaled",
            "H334 May cause allergy or asthma symptoms or breathing difficulties if inhaled",
            "H335 May cause respiratory irritation",
            "H336 May cause drowsiness or dizziness",
            "H340 May cause genetic defects",
            "H341 Suspected of causing genetic defects",
            "H350 May cause cancer",
            "H351 Suspected of causing cancer",
            "H360 May damage fertility or the unborn child",
            "H361 Suspected of damaging fertility or the unborn child",
            "H361d Suspected of damaging the unborn child",
            "H362 May cause harm to breast-fed children",
            "H370 Causes damage to organs",
            "H371 May cause damage to organs",
            "H372 Causes damage to organs through prolonged or repeated exposure",
            "H373 May cause damage to organs through prolonged or repeated exposure"
        ]

        # Create checkboxes for each health hazard
        for hazard in health_hazards:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(checkbox_frame, text=hazard, variable=var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR)
            checkbox.pack(anchor='w')
            checkbox_vars.append((var, hazard))  # Keep track of checkbox vars and labels

    # Check if the selected hazard type is "Environmental Hazards"
    elif hazard_type_var.get() == "Environmental Hazards (H4)":
        environmental_hazards = [
            "H400 Very toxic to aquatic life",
            "H401 Toxic to aquatic life",
            "H402 Harmful to aquatic life",
            "H410 Very toxic to aquatic life with long-lasting effects",
            "H411 Toxic to aquatic life with long-lasting effects",
            "H412 Harmful to aquatic life with long-lasting effects",
            "H413 May cause long-lasting harmful effects to aquatic life",
            "H420 Harms public health and the environment by destroying ozone in the upper atmosphere",
            "H441 Very toxic to terrestrial invertebrates"
        ]

        # Create checkboxes for each environmental hazard
        for hazard in environmental_hazards:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(checkbox_frame, text=hazard, variable=var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR)
            checkbox.pack(anchor='w')
            checkbox_vars.append((var, hazard))  # Keep track of checkbox vars and labels

    # Add functionality to update text box based on checkboxes
    update_text_box()

#######################################################################
def update_precautionary_checkboxes(precaution_checkbox_frame):
    global checkbox_vars  # Ensure we're using the global variable
    # Clear existing checkboxes
    for widget in precaution_checkbox_frame.winfo_children():
        widget.destroy()

    if precaution_type_var.get() == "General precautionary statements (P1)":
        precautions = [
            "P101 If medical advice is needed, have product container or label at hand.",
            "P102 Keep out of reach of children.",
            "P103 Read carefully and follow all instructions." 
        ]

        # Create checkboxes for each hazard
        for precaution in precautions:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(precaution_checkbox_frame, text=precaution, variable=var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR)
            checkbox.pack(anchor='w')
            checkbox_vars.append((var, precaution))  # Keep track of checkbox vars and labels

    # Check if the selected hazard type is "Health Hazards"
    elif precaution_type_var.get() == "Prevention precautionary statements (P2)":
        precautions = [
            "P203 Obtain, read and follow all safety instructions before use. "
        ]

        # Create checkboxes for each hazard
        for precaution in precautions:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(precaution_checkbox_frame, text=precaution, variable=var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR)
            checkbox.pack(anchor='w')
            checkbox_vars.append((var, precaution))  # Keep track of checkbox vars and labels

    elif precaution_type_var.get() == "Response precautionary statements (P3)":
        precautions = [  
        "P301 IF SWALLOWED: ",
        "P302 IF ON SKIN: ",
        "P303 IF ON SKIN (or hair): ",
        "P304 IF INHALED: ",
        "P305 IF IN EYES: ",
        "P306 IF ON CLOTHING: ",
        "P308 IF exposed or concerned: ",
        "P332 IF SKIN irritation occurs: ",
        "P333 If skin irritation or rash occurs: ",
        "P337 If eye irritation persists: ",
        "P370 In case of fire: ",
        "P371 In case of major fire and large quantities: "
        ]

        # Create checkboxes for each hazard
        for precaution in precautions:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(precaution_checkbox_frame, text=precaution, variable=var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR)
            checkbox.pack(anchor='w')
            checkbox_vars.append((var, precaution))  # Keep track of checkbox vars and labels

    elif precaution_type_var.get() == "Storage precautionary statements (P4)":
        precautions = [
            "P401 Store in accordance with ... ",
            "P402 Store in a dry place. ",
            "P403 Store in a well-ventilated place.",
            "P404 Store in a closed container.",
            "P405 Store locked up.",
            "P406 Store in corrosive resistant/... container with a resistant inner liner.",
            "P407 Maintain air gap between stacks or pallets.",
            "P410 Protect from sunlight.",
            "P411 Store at temperatures not exceeding ... °C/...°F.", 
            "P412 Do not expose to temperatures exceeding 50 °C/ 122 °F. ",
            "P413 Store bulk masses greater than ... kg/...lbs at temperatures not exceeding ... °C/...°F. ",
            "P420 Store separately."
        ]

        # Create checkboxes for each hazard
        for precaution in precautions:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(precaution_checkbox_frame, text=precaution, variable=var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR)
            checkbox.pack(anchor='w')
            checkbox_vars.append((var, precaution))  # Keep track of checkbox vars and labels

    elif precaution_type_var.get() == "Disposal precautionary statements (P5)":
        precautions = [
            "P501 Dispose of contents/container to ... ",
            "P502 Refer to manufacturer or supplier for information on recovery or recycling.",
            "P503 Refer to manufacturer/supplier... for information on disposal/recovery/recycling."
        ]

        # Create checkboxes for each hazard
        for precaution in precautions:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(precaution_checkbox_frame, text=precaution, variable=var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR)
            checkbox.pack(anchor='w')
            checkbox_vars.append((var, precaution))  # Keep track of checkbox vars and labels

    # Add functionality to update text box based on checkboxes
    update_text_box()


#######################################################################
def update_text_box():
    text = ""
    for var, label in checkbox_vars:
        if var.get():
            text += f"{label}\n"
    text_box.delete("1.0", tk.END)  # Clear the existing text
    text_box.insert(tk.END, text)  # Insert the updated text

# Initialize main application
root = tk.Tk()
root.title("Chemical Hazard Generator")
root.geometry("800x600")
root.configure(bg=BACKGROUND_COLOR)

setup_interface()
root.mainloop()
