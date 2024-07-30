import tkinter as tk
from tkinter import simpledialog, messagebox

def generate_batch_file(selected_modules, target_device_name):
    batch_file_content = f"""@echo off
REM Set the path to the portable Python interpreter
set "PYTHON_PATH=E:\\WPy64-31241\\python-3.12.4.amd64\\python.exe"

REM Set the path to the main Python script
set "SCRIPT_PATH=E:\\RapidExtractor\\Scripts\\main.py"

REM Debug output
echo Python Path: %PYTHON_PATH%
echo Script Path: %SCRIPT_PATH%

REM Check if the Python interpreter exists
if not exist "%PYTHON_PATH%" (
    echo The specified Python interpreter does not exist: %PYTHON_PATH%
    pause
    exit /b
)

REM Check if the main script exists
if not exist "%SCRIPT_PATH%" (
    echo The specified Python script does not exist: %SCRIPT_PATH%
    pause
    exit /b
)

REM Run the main script with selected modules
"%PYTHON_PATH%" "%SCRIPT_PATH%" "{selected_modules}" "{target_device_name}"

pause
"""

    batch_file_name = f"{target_device_name}.bat"
    with open(batch_file_name, "w") as batch_file:
        batch_file.write(batch_file_content)

    messagebox.showinfo("Success", f"Batch file '{batch_file_name}' has been created successfully.")

def create_gui():
    root = tk.Tk()
    root.title("Module Selector")

    target_device_name = simpledialog.askstring("Input", "Name your target device:", parent=root)
    if not target_device_name:
        messagebox.showerror("Error", "Target device name is required.")
        root.destroy()
        sys.exit()

    root.withdraw()  # Hide the main window during module selection

    selected_modules = []
    select_all_state = tk.BooleanVar(value=True)

    def on_select():
        nonlocal selected_modules
        selected_modules.clear()
        for module_name, module_var in modules:
            if module_var.get():
                selected_modules.append(module_var._name)
        if selected_modules:
            selected_modules_str = " ".join(selected_modules)
            generate_batch_file(selected_modules_str, target_device_name)
            root.quit()

    def toggle_select_all():
        state = select_all_state.get()
        for _, module_var in modules:
            module_var.set(state)
        select_all_state.set(not state)
        toggle_button.config(text="Deselect All" if state else "Select All")

    modules = [
        ("DirTree", tk.BooleanVar(name="dir_tree")),
        ("Prefetch", tk.BooleanVar(name="prefetch")),
        ("Event Logs", tk.BooleanVar(name="event_logs")),
        ("Processes", tk.BooleanVar(name="processes")),
        ("Installed Programs", tk.BooleanVar(name="installed_programs")),
    ]

    for module_name, module_var in modules:
        tk.Checkbutton(root, text=module_name, variable=module_var).pack(anchor=tk.W)

    toggle_button = tk.Button(root, text="Select All", command=toggle_select_all)
    toggle_button.pack(anchor=tk.W)
    tk.Button(root, text="Generate Batch File", command=on_select).pack(anchor=tk.W)

    root.deiconify()  # Show the main window again for module selection
    root.mainloop()

if __name__ == "__main__":
    create_gui()
