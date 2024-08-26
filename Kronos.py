# @hoodcomp on cord
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from lupa import LuaRuntime
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading
import time

class ExecutorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kronos - 1.0")
        self.root.geometry("600x340")
        self.root.configure(bg="#2E2E2E")  # Dark gray background color
        self.root.resizable(False, False)  # Disable resizing
        self.lua_runtime = LuaRuntime(unpack_returned_tuples=True)
        self.injected = False  # Injection status
        self.current_executor = "Monaco"  # Default executor

        # Load logos and resize them
        self.inject_logo = self.load_image("https://j.top4top.io/p_3157dlowg0.png", (20, 20))
        self.execute_logo = self.load_image("https://f.top4top.io/p_3157jmab30.png", (20, 20))
        self.save_logo = self.load_image("https://a.top4top.io/p_3157ltnl80.png", (20, 20))
        self.clear_logo = self.load_image("https://b.top4top.io/p_3157rd76j1.png", (20, 20))
        self.settings_logo = self.load_image("https://icon-url-here.png", (20, 20))  # Replace with actual logo URL

        self.create_widgets()

        # Bind the close event to a custom handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Title Label at the Top Left
        self.title_label = tk.Label(self.root, text="Kronos - 1.0", font=("Segoe UI", 14, "bold"), bg="#2E2E2E", fg="#FFFFFF", anchor='w')
        self.title_label.pack(side=tk.TOP, anchor='nw', padx=10, pady=(10, 0))

        # Status Label
        self.status_label = tk.Label(self.root, text="Status: Not Injected", font=("Segoe UI", 10), bg="#2E2E2E", fg="#FF4136")
        self.status_label.pack(side=tk.TOP, anchor='nw', padx=10, pady=(0, 10))

        # Create Frame for buttons and script
        top_frame = tk.Frame(self.root, bg="#2E2E2E")
        top_frame.pack(fill=tk.X, padx=10)

        # Execute Button
        self.execute_button = tk.Button(top_frame, image=self.execute_logo, command=self.execute_script, bg="#1E1E1E", borderwidth=0, highlightthickness=0, relief="flat", width=40, height=30)
        self.execute_button.grid(row=0, column=0, padx=5, pady=5)

        # Inject Button
        self.inject_button = tk.Button(top_frame, image=self.inject_logo, command=self.inject_script, bg="#1E1E1E", borderwidth=0, highlightthickness=0, relief="flat", width=40, height=30)
        self.inject_button.grid(row=0, column=1, padx=5, pady=5)

        # Save Button
        self.save_button = tk.Button(top_frame, image=self.save_logo, command=self.save_script, bg="#1E1E1E", borderwidth=0, highlightthickness=0, relief="flat", width=40, height=30)
        self.save_button.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        # Clear Button
        self.clear_button = tk.Button(top_frame, image=self.clear_logo, command=self.clear_text, bg="#1E1E1E", borderwidth=0, highlightthickness=0, relief="flat", width=40, height=30)
        self.clear_button.grid(row=0, column=3, padx=5, pady=5, sticky='e')

        # Settings Button
        self.settings_button = tk.Button(top_frame, image=self.settings_logo, command=self.open_settings, bg="#1E1E1E", borderwidth=0, highlightthickness=0, relief="flat", width=40, height=30)
        self.settings_button.grid(row=0, column=4, padx=5, pady=5, sticky='e')

        # Create Frame for script and line numbers
        text_frame = tk.Frame(self.root, bg="#2E2E2E")
        text_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=(10, 0))

        # Line Counter
        self.line_numbers = tk.Text(text_frame, width=4, bg="#1E1E1E", fg="#7F8C8D", padx=5, pady=5, state=tk.DISABLED, borderwidth=0)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Script Text Area
        self.script_text = tk.Text(text_frame, bg="#1E1E1E", fg="#FFFFFF", insertbackground='white', wrap=tk.NONE, borderwidth=0, height=12)
        self.script_text.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.script_text.bind("<KeyRelease>", self.update_line_numbers)
        self.script_text.bind("<Key>", self.auto_close_characters)
        self.update_line_numbers()

    def load_image(self, url, size):
        response = requests.get(url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize(size, Image.LANCZOS)  # Resize image with high-quality filter
        return ImageTk.PhotoImage(img)

    def update_line_numbers(self, event=None):
        # Update line numbers in the line_numbers text area
        line_count = self.script_text.index('end-1c').split('.')[0]
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        for i in range(1, int(line_count) + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")
        self.line_numbers.config(state=tk.DISABLED)

    def inject_script(self):
        if self.injected:
            messagebox.showinfo("Inject", "Already Injected!")
            return

        # Simulate freezing the UI and injecting
        threading.Thread(target=self.inject_process).start()

    def inject_process(self):
        time.sleep(10)  # Simulate 10 seconds of freezing
        self.injected = True
        self.status_label.config(text="Status: Ready", fg="#2ECC40")

    def execute_script(self):
        if not self.injected:
            messagebox.showerror("Error", "You must inject first before executing the script!")
            return

        # Execute Lua script
        script = self.script_text.get("1.0", tk.END).strip()
        if script:
            try:
                lua_result = self.lua_runtime.execute(script)
                # Optional: You can process lua_result here if needed
            except Exception as e:
                pass  # Skip error alerts

    def save_script(self):
        # Save the script text to a file
        script = self.script_text.get("1.0", tk.END).strip()
        if script:
            file_path = filedialog.asksaveasfilename(defaultextension=".lua", filetypes=[("Lua files", "*.lua"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(script)
                messagebox.showinfo("Save", "Script saved successfully!")

    def clear_text(self):
        # Clear the script text area
        self.script_text.delete("1.0", tk.END)

    def auto_close_characters(self, event):
        # Auto-insert closing characters
        pairs = {'"': '"', "'": "'", '(': ')', '{': '}', '[': ']'}
        current = event.char
        if current in pairs:
            self.script_text.insert(tk.INSERT, pairs[current])
            self.script_text.mark_set(tk.INSERT, f"{self.script_text.index(tk.INSERT)}-1c")

    def open_settings(self):
        # Open settings popup
        settings_popup = tk.Toplevel(self.root)
        settings_popup.title("Settings")
        settings_popup.geometry("300x200")
        settings_popup.configure(bg="#2E2E2E")
        settings_popup.transient(self.root)
        settings_popup.grab_set()
        settings_popup.focus_set()

        # Executor Option
        tk.Label(settings_popup, text="Select Executor:", bg="#2E2E2E", fg="#FFFFFF", font=("Segoe UI", 12)).pack(pady=10)
        executor_var = tk.StringVar(value=self.current_executor)
        ace_option = tk.Radiobutton(settings_popup, text="Ace", variable=executor_var, value="Ace", bg="#2E2E2E", fg="#FFFFFF", font=("Segoe UI", 10), command=self.change_executor)
        ace_option.pack(anchor=tk.W, padx=20)
        monaco_option = tk.Radiobutton(settings_popup, text="Monaco", variable=executor_var, value="Monaco", bg="#2E2E2E", fg="#FFFFFF", font=("Segoe UI", 10), command=self.change_executor)
        monaco_option.pack(anchor=tk.W, padx=20)

    def change_executor(self):
        # Change the executor based on the selection
        selected_executor = self.current_executor.get()
        if selected_executor == "Ace":
            self.current_executor = "Ace"
            self.apply_ace_theme()
        elif selected_executor == "Monaco":
            self.current_executor = "Monaco"
            self.apply_monaco_theme()

    def apply_ace_theme(self):
        # Change the script_text to mimic Ace Editor style (simple example)
        self.script_text.config(bg="#1E1E1E", fg="#FFFFFF", insertbackground='white', font=("Courier New", 10))

    def apply_monaco_theme(self):
        # Change the script_text to mimic Monaco Editor style (simple example)
        self.script_text.config(bg="#1E1E1E", fg="#FFFFFF", insertbackground='white', font=("Consolas", 11))

    def on_closing(self):
        # Custom close event
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExecutorUI(root)
    root.mainloop()
    
