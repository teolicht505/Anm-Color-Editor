# Anm Color Editor
## Description
This program provides a graphical interface to edit .anm files used in the game Persona 3 FES. It allows you to modify and save specific colors found within these files.

## Features
- **Open File**: Open .anm files using a file dialog.
- **Drag and Drop**: Supports dragging and dropping .anm files to open them directly.
- **Color Navigation**: Navigate between colors found in the file.
- **Select Color**: Choose a new color using a color picker dialog.
- **Change Color by Hex Code**: Enter a hexadecimal code to change the current color.
- **Save Modified Colors**: Save the modified colors back to the .anm file.

## Requirements
- Python 3.x
- Libraries: 'struct', 'tkinter', 'tkinterdnd2'

## Usage
1. Run the program.
2. Open an .anm file using the "File" menu or by dragging and dropping the file into the window.
3. Navigate through the colors using the "Prev" and "Next" buttons.
4. Select a new color using the "Select color" button or enter a hexadecimal code with the "Input color (#RRGGBB)" button.
5. To save changes, click on "Save Colors".
6. Drag and drop a new file or select it with the "File" menu to edit another file.

## Known issues
The file "fade_if_time_1b.anm" missdetects a color, making it to be saved incorrectly. This issue could cause the game to skip this animation or result in other issues. Until this problem is resolved, you will need to manually edit the colors in this file.