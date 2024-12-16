import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.main import flow
import multiprocessing


def browse_file(entry_field, file_type):
    """Open file dialog and update entry field."""
    file = filedialog.askopenfilename(
        filetypes=[(f"{file_type} files", f"*.{file_type}")]
    )
    if file:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, file)


def browse_directory(entry_field):
    """Open directory dialog and update entry field."""
    directory = filedialog.askdirectory()
    if directory:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, directory)


def run_flow():
    """Run the `flow` function with user inputs."""
    pdf_path = pdf_entry.get()
    excel_path = excel_entry.get()
    output_path = output_entry.get()
    sim_cat = sim_cat_var.get()
    threshold = threshold_var.get()

    if not pdf_path or not excel_path or not output_path:
        messagebox.showerror("Error", "Please provide all required inputs!")
        return

    try:
        flow(
            pdf_path=pdf_path,
            excel_path=excel_path,
            output_path=output_path,
            sim_cat=sim_cat,
            threshold=threshold
        )
        messagebox.showinfo("Success", "Flow function executed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def toggle_theme():
    """Toggle between light and dark themes."""
    global dark_mode
    dark_mode = not dark_mode

    bg_color = "#1E1E2F" if dark_mode else "#F5F5F5"
    fg_color = "#FFFFFF" if dark_mode else "#000000"
    entry_bg = "#252526" if dark_mode else "white"
    entry_fg = "#FFFFFF" if dark_mode else "#000000"
    button_bg = "#0078D4"
    button_fg = "#FFFFFF" if dark_mode else "white"
    top_bar_color = "#0078D4"

    root.configure(bg=bg_color)
    main_frame.configure(bg=bg_color)
    top_bar.configure(bg=top_bar_color)
    toggle_button.configure(
        bg=top_bar_color, fg=button_fg, text="🌙" if not dark_mode else "☀"
    )
    for widget in main_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=bg_color, fg=fg_color)
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        elif isinstance(widget, tk.Button):
            widget.configure(bg=button_bg, fg=button_fg)
        elif isinstance(widget, tk.Scale):
            widget.configure(bg=bg_color, fg=fg_color)
    sim_cat_check.configure(bg=bg_color)

if __name__ =='__main__':
    multiprocessing.freeze_support()  # For compatibility with PyInstaller

# Create the main application window
    root = tk.Tk()
    root.title("OCR App")
    root.geometry("800x500")  # Initial size
    dark_mode = False

    # Configure grid for dynamic resizing
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    # Top bar for the toggle theme button
    top_bar = tk.Frame(root, bg="#0078D4", height=50)
    top_bar.grid(row=0, column=0, sticky="ew")
    top_bar.grid_propagate(False)

    # Toggle Theme Icon Button
    toggle_button = tk.Button(
        top_bar, text="🌙", font=("Arial", 14), bg="#0078D4", fg="white",
        bd=0, relief="flat", command=toggle_theme
    )
    toggle_button.pack(side="right", padx=10)

    # Main frame with margin
    main_frame = tk.Frame(root, bg="#F5F5F5", padx=20, pady=20)
    main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Configure main frame grid
    main_frame.columnconfigure(1, weight=1)

    # Styles
    default_font = ("Arial", 12)

    # PDF Path
    tk.Label(main_frame, text="PDF Path", font=default_font, bg="#F5F5F5").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    pdf_entry = tk.Entry(main_frame, font=default_font, bg="white", fg="#000000")
    pdf_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    pdf_browse = tk.Button(main_frame, text="Browse", font=default_font, command=lambda: browse_file(pdf_entry, "pdf"))
    pdf_browse.grid(row=0, column=2, padx=10, pady=5)

    # Excel Path
    tk.Label(main_frame, text="Excel Path", font=default_font, bg="#F5F5F5").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    excel_entry = tk.Entry(main_frame, font=default_font, bg="white", fg="#000000")
    excel_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    excel_browse = tk.Button(main_frame, text="Browse", font=default_font, command=lambda: browse_file(excel_entry, "xls"))
    excel_browse.grid(row=1, column=2, padx=10, pady=5)

    # Output Path
    tk.Label(main_frame, text="Output Path", font=default_font, bg="#F5F5F5").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    output_entry = tk.Entry(main_frame, font=default_font, bg="white", fg="#000000")
    output_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    output_browse = tk.Button(main_frame, text="Browse", font=default_font, command=lambda: browse_directory(output_entry))
    output_browse.grid(row=2, column=2, padx=10, pady=5)

    # Sim Cat
    tk.Label(main_frame, text="Sim Cat (True/False)", font=default_font, bg="#F5F5F5").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    sim_cat_var = tk.BooleanVar(value=False)
    sim_cat_check = tk.Checkbutton(main_frame, variable=sim_cat_var, bg="#F5F5F5")
    sim_cat_check.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Threshold
    tk.Label(main_frame, text="Threshold (Default: 70)", font=default_font, bg="#F5F5F5").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    threshold_var = tk.IntVar(value=70)
    threshold_scale = tk.Scale(main_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=threshold_var, bg="#F5F5F5")
    threshold_scale.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    # إضافة Progress Bar
    progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=5, column=1, padx=10, pady=20, sticky="ew")
    
    # Run Button
    run_button = tk.Button(
        main_frame, text="Run Flow", font=("Arial", 12), bg="#0078D4", fg="white", command=run_flow
    )
    run_button.grid(row=6, column=1, pady=20, sticky="ew")

    # Start the Tkinter event loop
    root.mainloop()