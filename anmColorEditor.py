import struct
import tkinter as tk
from tkinter import colorchooser, simpledialog, filedialog, messagebox
import sys
from tkinterdnd2 import TkinterDnD, DND_FILES

# Global variables
pattern = b'\x02\x1c\x01\x00\x00\x00\x00\x00'
lines = []
colors = []
file_path = None
colors_hex = []

class ColorSelectorApp:
    def __init__(self, root, colors):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Anm Color Editor")

        # Initialize TkDND for drag and drop support
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.drop)

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add a File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open file", command=self.open_file)
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add an Options menu
        self.change_unique_colors = 0
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.options_menu.add_checkbutton(label="Change unique colors",
                                          variable=self.change_unique_colors,
                                          command=self.toggle_change_unique_colors)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)

        self.colors = colors
        self.current_color_index = 0

        if self.colors:
            # Display the first color in the list
            self.color_frame = tk.Frame(root, width=200, height=200, bg=self.colors[self.current_color_index])
        else:
            # Display a placeholder if no colors are loaded
            self.color_frame = tk.Frame(root, width=200, height=200)
            self.message_label = tk.Label(self.color_frame, text="Open or drag a .anm file\nto edit colors")
            self.message_label.pack(expand=True)

        self.color_frame.pack(padx=20, pady=10)

        # Control buttons for navigation (only if colors are available)
        if self.colors:
            self.control_frame = tk.Frame(root)
            self.control_frame.pack(pady=5)

            self.prev_button = tk.Button(self.control_frame, text="Prev", command=self.prev_color)
            self.prev_button.pack(side=tk.LEFT, padx=5)

            self.index_label = tk.Label(self.control_frame, text="1 / {}".format(len(self.colors)))
            self.index_label.pack(side=tk.LEFT, padx=5)

            self.next_button = tk.Button(self.control_frame, text="Next", command=self.next_color)
            self.next_button.pack(side=tk.LEFT, padx=5)

            # Buttons for selecting and changing colors
            self.select_button = tk.Button(root, text="Select color", command=self.select_color)
            self.select_button.pack(pady=5)

            self.change_color_button = tk.Button(root, text="Input color (#RRGGBB)", command=self.change_color_hex)
            self.change_color_button.pack(pady=5)

            self.finish_button = tk.Button(root, text="Save Colors", command=self.save_process)
            self.finish_button.pack(pady=5)

        # Center the window on the screen
        window_width = root.winfo_reqwidth()
        window_height = root.winfo_reqheight()
        position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
        root.geometry("+{}+{}".format(position_right, position_down))

        self.root.lift()
        self.root.focus_force()

    def toggle_change_unique_colors(self):
        """Handle the toggle of 'Change unique colors'."""
        self.change_unique_colors = 0 if (self.change_unique_colors) else 1

    def drop(self, event):
        """Handle file drop."""
        global file_path

        file_path = event.data.strip().strip('{').strip('}')
        if file_path:
            if file_path.endswith('.anm'):
                self.update_file()
            else:
                messagebox.showerror("Error", "Please drop a valid .anm file")

    def prev_color(self):
        """Go to the previous color in the list."""
        self.current_color_index = (self.current_color_index - 1) % len(self.colors)
        self.update_color()

    def next_color(self):
        """Go to the next color in the list."""
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        self.update_color()

    def update_color(self):
        """Update the displayed color and label."""
        if self.colors:
            self.color_frame.config(bg=self.colors[self.current_color_index])
            self.index_label.config(text="{:d} / {:d}".format(self.current_color_index + 1, len(self.colors)))

    def apply_color_change(self, color):
        """Applies color change depending if you have the change_unique_color option ON/OFF."""
        if (self.change_unique_colors):
            original_color = self.colors[self.current_color_index]
            for i in range(len(self.colors)):
                if (self.colors[i] == original_color):
                    self.colors[i] = color
        else:
            self.colors[self.current_color_index] = color

        self.color_frame.config(bg=color)

    def select_color(self):
        """Open a color chooser dialog to select a new color."""
        color = colorchooser.askcolor(title="Select a color")
        if color[1] is not None:
            self.apply_color_change(color[1])


    def change_color_hex(self):
        """Allow the user to input a hex color code."""
        hex_color = simpledialog.askstring("Change Color (#RRGGBB)", "Input value with format #RRGGBB/RRGGBB:")
        if hex_color and len(hex_color) == 7 and hex_color[0] == '#' and hex_color[1:].isnumeric():
            self.apply_color_change(hex_color)
        elif hex_color and len(hex_color) == 6 and hex_color.isnumeric():
            hex_color = f"#{hex_color}"
            self.apply_color_change(hex_color)
        elif hex_color != None:
            messagebox.showerror("Error", "Please input a valid color with format: #RRGGBB/RRGGBB")

    def save_process(self):
        """Save the modified colors and close the application."""
        global pattern, lines, colors, file_path, colors_hex
        save_colors(file_path, lines)
        messagebox.showinfo("Information", "File saved!")

    def open_file(self):
        """Open a .anm file using a file dialog."""
        global file_path, colors, lines, colors_hex
        file_path = filedialog.askopenfilename(
            title="Open file",
            filetypes=[("ANM files", "*.anm")]
        )
        if file_path: self.update_file()

    def update_file(self):
        """Update view with new .anm file."""
        global file_path, colors, lines, colors_hex

        lines = []
        colors = []
        colors_hex = []
        find_pattern(file_path, pattern)
        load_colors(file_path, lines)
        colors_hex = ["#{:02x}{:02x}{:02x}".format(*rgba[:3]) for rgba in colors]
            
        if (not hasattr(self, "prev_button")):
            self.color_frame.destroy()
            self.__init__(self.root, colors_hex)
            self.root.geometry("300x400")
        else:
            self.colors = colors_hex
            self.current_color_index = 0

        self.update_color()

class ErrorPopup:
    def __init__(self, root, message):
        """Display an error message in a popup window."""
        self.root = root
        self.root.title("Error")
        self.root.geometry("300x100")
        
        label = tk.Label(root, text=message, padx=10, pady=10)
        label.pack()
        
        ok_button = tk.Button(root, text="Exit", command=self.close_window)
        ok_button.pack(pady=5)

    def close_window(self):
        """Close the error popup window."""
        self.root.destroy()

def change_endianness(data, endianess):
    """Change the endianness of the provided binary data."""
    format_string = ">" if endianess == "big" else "<"
    
    unpacked_data = struct.unpack(format_string + "I", data)
    
    new_endianness_data = struct.pack("<I" if endianess == "big" else ">I", *unpacked_data)
    
    return new_endianness_data

def find_pattern(file_path, pattern):
    """Find all occurrences of the specified pattern in the file."""
    offset = 44  # Number of bytes to skip before comparing the next 4 bytes

    with open(file_path, "rb") as file:
        while True:
            block = file.read(8)  # Read 16 bytes
            if len(block) < 8:
                break  # End of file reached

            if pattern in block:  # Check if the first 4 bytes match the pattern
                current_block = file.read(4)
                file.seek(offset, 1)  # Skip 52 bytes
                next_block = file.read(4)  # Read the next 4 bytes

                if next_block == current_block:  # Check if the next 4 bytes match the pattern
                    lines.append(file.tell() - 52)
                file.seek(4, 1)

def hex_to_int(hex_str):
    """Convert a hexadecimal string to an integer."""
    float_value = struct.unpack('!f', bytes.fromhex(hex_str))[0]
    int_value = int(float_value)
    return int_value

def int_to_hex(int_value):
    """Convert an integer to a hexadecimal string."""
    float_value = float(int_value)
    hex_str = struct.pack('!f', float_value).hex()
    return hex_str

def load_colors(file_path, lines):
    """Load colors from the file based on the identified lines."""
    with open(file_path, "rb") as file:
        for line in lines:
            file.seek(line)
            hex_line = file.read(16)

            zeros = b'\x00\x00'

            r = change_endianness(hex_line[0:4], 'big')[2:] + zeros
            g = change_endianness(hex_line[4:8], 'big')[2:] + zeros
            b = change_endianness(hex_line[8:12], 'big')[2:] + zeros
            a = change_endianness(hex_line[12:16], 'big')[2:] + zeros

            current_rgba = [r.hex(), g.hex(), b.hex(), a.hex()]
            current_rgba = [hex_to_int(color) for color in current_rgba]
            
            colors.append(current_rgba)

            print(f"Color {current_rgba} detected in line {line}")

def save_colors(file_path, lines):
    """Save the modified colors back to the file."""
    with open(file_path, "rb+") as file:
        for line, color_hex, orig_color in zip(lines, colors_hex, colors):
            file.seek(line)

            zeros = b'\x00\x00'

            r = change_endianness(bytes.fromhex(int_to_hex(int(color_hex[1:3], 16))), 'little')[2:] + zeros
            g = change_endianness(bytes.fromhex(int_to_hex(int(color_hex[3:5], 16))), 'little')[2:] + zeros
            b = change_endianness(bytes.fromhex(int_to_hex(int(color_hex[5:], 16))), 'little')[2:] + zeros
            a = change_endianness(bytes.fromhex(int_to_hex(orig_color[3])), 'little')[2:] + zeros

            file.write(r)
            file.write(g)
            file.write(b)
            file.write(a)

            file.seek(line + 48)

            file.write(r)
            file.write(g)
            file.write(b)
            file.write(a)

            print(f"Saving color {color_hex} detected in line {line}")

def main():
    """Main function to start the application."""
    root = TkinterDnD.Tk()
    global pattern, lines, colors, file_path, colors_hex

    # If a file is provided via command line, open it
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg.endswith('.anm'):
                file_path = arg
                break

    if file_path:
        find_pattern(file_path, pattern)
        load_colors(file_path, lines)

        colors_hex = ["#{:02x}{:02x}{:02x}".format(*rgba[:3]) for rgba in colors]
        app = ColorSelectorApp(root, colors_hex)
        root.geometry("300x400")
    else:
        # If no file is provided, start with an empty color list and display the open file option
        app = ColorSelectorApp(root, [])
        root.geometry("300x75")

    root.mainloop()

if __name__ == "__main__":
    main()
