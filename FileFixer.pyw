"""
FileFixer / File Edit - a DiskFixer / Disk Edit clone for files instead of disks

On the Apple ][:
* there was a DISKFIXER, (C) 1980, The Image Producers, Inc., A Quicksilver Softsystems utility
* then a DISK EDIT, (C) 1985, The Software Factory, Inc.
  in which the help function still mentioned DISKFIXER
  
This version was made by Hubert Tournier
and distributed with a BSD licence.
"""

import os
import sys
import tkinter
import tkinter.filedialog
import tkinter.messagebox

TITLE = "FileFixer"

window = None
frame = None
frame_1 = None
frame_2 = None
frame_3 = None
frame_4 = None

filename = None
position = None
chunk_size = 512
chunk = None

offsets = None
hex_content = None
text_content = None
settings = None

color_scheme = 0
fg_color = "green"
bg_color = "black"
decimal_numbering = True
ascii_filter = False
file_modified = False

################################################################################
def read_chunk(filename, position):
    """ Read the chunk of filename at position and return it as a bytes array """
    with open(filename, "rb") as file:
        file.seek(position, os.SEEK_SET)
        return file.read(chunk_size)

################################################################################
def display_offsets():
    """ Display offsets in the chosen representation """
    global offsets
    columns = chunk_size // 32
    if offsets != None:
        for line in range(32):
            offsets[line].destroy()
    offsets = []
    for line in range(32):
        if decimal_numbering:
            label = tkinter.Label(text=f'{position + (line * columns):d}:', foreground=fg_color, background=bg_color)
        else: # hexadecimal numbering
            label = tkinter.Label(text=f'${position + (line * columns):X}:', foreground=fg_color, background=bg_color)
        label.grid(in_=frame_1, row=line, column=0, sticky="E")
        offsets.append(label)

################################################################################
def display_hexadecimal_content():
    """ Print the hexadecimal part of the chunk from filename at position """
    global hex_content
    columns = chunk_size // 32
    if frame_2 != None:
        if hex_content != None:
            for line in range(32):
                for column in range(columns):
                    if hex_content[line][column] !=  None:
                        hex_content[line][column].destroy()
        hex_content = []
        row = []
        number = 0
        for byte in chunk:
            label = tkinter.Label(text=f'{byte:02X}', foreground=fg_color, background=bg_color)
            label.grid(in_=frame_2, row=(number // columns), column=(number % columns), padx=2)
            row.append(label)
            if (number % columns) == (columns - 1):
                hex_content.append(row)
                row = []
            number += 1
        while number < chunk_size:
            label = tkinter.Label(text="", foreground=fg_color, background=bg_color)
            label.grid(in_=frame_2, row=(number // columns), column=(number % columns), padx=2)
            row.append(label)
            if (number % columns) == (columns - 1):
                hex_content.append(row)
                row = []
            number += 1

################################################################################
def display_textual_content():
    """ Print the textual part of the chunk from filename at position """
    global text_content
    columns = chunk_size // 32
    if frame_3 != None:
        if text_content != None:
            for line in range(32):
                for column in range(columns):
                    if text_content[line][column] !=  None:
                        text_content[line][column].destroy()
        text_content = []
        row = []
        number = 0
        for byte in chunk:
            if chr(byte).isprintable():
                label = tkinter.Label(text=chr(byte), foreground=fg_color, background=bg_color)
            elif ascii_filter:
                label = tkinter.Label(text='.', foreground=fg_color, background=bg_color)
            else:
                # Print control characters with inverted colors, adding 64 to the ASCII code
                # (ie. 1 (SOH) -> 65 (^A):
                label = tkinter.Label(text=chr(byte + 64), foreground=bg_color, background=fg_color)
            label.grid(in_=frame_3, row=(number // columns), column=(number % columns), padx=2)
            row.append(label)
            if (number % columns) == (columns - 1):
                text_content.append(row)
                row = []
            number += 1
        while number < chunk_size:
            label = tkinter.Label(text="", foreground=fg_color, background=bg_color)
            label.grid(in_=frame_3, row=(number // columns), column=(number % columns), padx=2)
            row.append(label)
            if (number % columns) == (columns - 1):
                text_content.append(row)
                row = []
            number += 1

################################################################################
def display_chunk():
    """ Print the chunk from filename at position DiskFixer style """
    display_offsets()
    display_hexadecimal_content()
    display_textual_content()

################################################################################
def display_settings():
    """ Print the current state of settings """
    settings = tkinter.Label(frame_4, text="Buffer 0 / Mask: OFF / Normal", foreground=fg_color, background=bg_color, takefocus=0)
    settings.grid(in_=frame_4, row=0, column=0)

################################################################################
def process_first_chunk():
    """ Print the first chunk """
    global position, chunk
    position = 0
    chunk = read_chunk(filename, position)
    display_chunk()

################################################################################
def process_next_chunk():
    """ Print the next chunk if we haven't reached the end of the file yet """
    global position, chunk
    if len(chunk) == chunk_size:
        position += chunk_size
        chunk = read_chunk(filename, position)
        display_chunk()

################################################################################
def process_previous_chunk():
    """ Print the previous chunk if we aren't at the beginning of the file """
    global position, chunk
    if position:
        position -= chunk_size
        chunk = read_chunk(filename, position)
        display_chunk()

################################################################################
def destroy_sub_frames():
    """ Destroy the hexadecimal and Textual frames """
    global frame_2, frame_3
    if frame_2 != None:
        frame_2.destroy()
        frame_2 = None
    if frame_3  != None:
        frame_3.destroy()
        frame_3 = None

################################################################################
def destroy_contents():
    """ Destroy widgets in case of chunk size modification """
    global hex_content, text_content
    columns = chunk_size // 32
    if hex_content != None:
        for line in range(32):
            for column in range(columns):
                if hex_content[line][column] !=  None:
                    hex_content[line][column].destroy()
    hex_content = None
    if text_content != None:
        for line in range(32):
            for column in range(columns):
                if text_content[line][column] !=  None:
                    text_content[line][column].destroy()
    text_content = None   

################################################################################
def set_ascii_display_mode():
    """ Set (A)SCII characters view mode """
    global frame_3, position, chunk_size, chunk
    if chunk_size == 512:
        destroy_contents()
        if position % 1024:
            position -= chunk_size
        chunk_size = 1024
        chunk = read_chunk(filename, position)

    destroy_sub_frames()
    frame_3 = tkinter.LabelFrame(frame, text="Content (text)", foreground=fg_color, background=bg_color, takefocus=0)
    frame_3.grid(in_=frame, row=0, column=1, padx=5)
    display_chunk()

################################################################################
def set_both_display_mode(display=True):
    """ Set mode ASCII-Hexa (half screen each) (B) """
    global frame_2, frame_3, chunk_size, chunk
    if chunk_size == 1024:
        destroy_contents()
        chunk_size = 512
        chunk = read_chunk(filename, position)

    destroy_sub_frames()
    frame_2 = tkinter.LabelFrame(frame, text="Content (hexadecimal)", foreground=fg_color, background=bg_color, takefocus=0)
    frame_3 = tkinter.LabelFrame(frame, text="Content (text)", foreground=fg_color, background=bg_color, takefocus=0)
    frame_2.grid(in_=frame, row=0, column=1, padx=5)
    frame_3.grid(in_=frame, row=0, column=2, padx=5)
    if display:
        display_chunk()
    
################################################################################
def set_hexadecimal_display_mode():
    """ Set (H)exadecimal bytes view mode """
    global frame_2, position, chunk_size, chunk
    if chunk_size == 512:
        destroy_contents()
        if position % 1024:
            position -= chunk_size
        chunk_size = 1024
        chunk = read_chunk(filename, position)

    destroy_sub_frames()
    frame_2 = tkinter.LabelFrame(frame, text="Content (hexadecimal)", foreground=fg_color, background=bg_color, takefocus=0)
    frame_2.grid(in_=frame, row=0, column=1, padx=5)
    display_chunk()
    
################################################################################
def toggle_hexa_decimal_numbering():
    """ Toggle hexa/decimal (n)umbering """
    global decimal_numbering
    if decimal_numbering:
        decimal_numbering = False
    else:
        decimal_numbering = True
    display_offsets()

################################################################################
def quit():
    """ (Q)uit the FileFixer to monitor """
    if file_modified:
        if not tkinter.messagebox.askokcancel(title="There are unsaved changes", message="Quit without saving?"):
            # Cancel (Q)uit:
            return
    sys.exit(0)

################################################################################
def select_new_file():
    """ (S)elect a new file """
    global filename, position, chunk, file_modified
    if file_modified:
        if not tkinter.messagebox.askokcancel(title="There are unsaved changes", message="Skip to next file without saving?"):
            # Cancel (S)elect a new file:
            return

    # Input file selection:
    filename = tkinter.filedialog.askopenfilename(title='Select a new file')

    # First chunk load and display:
    if os.path.exists(filename):
        process_first_chunk()
        file_modified = False

################################################################################
def toggle_ascii_filter():
    """ Toggle ASCII filter (Y) """
    global ascii_filter
    if ascii_filter:
        ascii_filter = False
    else:
        ascii_filter = True
    display_textual_content()

################################################################################
def cycle_colors():
    """ Cycle between different color schemes """
    global color_scheme, fg_color, bg_color
    if color_scheme == 0:
        color_scheme = 1
        fg_color = "#FFBF00" # amber
        bg_color = "black"
    elif color_scheme == 1:
        color_scheme = 2
        fg_color = "white"
        bg_color = "black"
    elif color_scheme == 2:
        color_scheme = 3
        fg_color = "black"
        bg_color = "white"
    elif color_scheme == 3:
        color_scheme = 0
        fg_color = "green"
        bg_color = "black"

    window.config(bg=bg_color)
    frame.config(foreground=fg_color, background=bg_color)
    frame_1.config(foreground=fg_color, background=bg_color)
    frame_2.config(foreground=fg_color, background=bg_color)
    frame_3.config(foreground=fg_color, background=bg_color)
    frame_4.config(foreground=fg_color, background=bg_color)
    display_chunk()
    display_settings()

################################################################################
def handle_keypress(event):
    """ Manage key press actions """
    try:
        print("char=", event.char, "ord(char)=", ord(event.char), "keysym=", event.keysym, "num=", event.num)
    except:
        print("char=", event.char, "keysym=", event.keysym, "num=", event.num)

    if event.keysym in ("Down", "Right") \
    or len(event.keysym) == 1 and ord(event.keysym) in (10, 21): # ^J ^U
        process_next_chunk()
    elif event.keysym in ("Up", "Left") \
    or len(event.keysym) == 1 and ord(event.keysym) in (11, 8): # ^K ^H
        process_previous_chunk()
    elif event.keysym in ('a', 'A'):
        set_ascii_display_mode()
    elif event.keysym in ('b', 'B'):
        set_both_display_mode()
    elif event.keysym in ('h', 'H'):
        set_hexadecimal_display_mode()
    elif event.keysym in ('n', 'N'):
        toggle_hexa_decimal_numbering()
    elif event.keysym in ('q', 'Q') \
    or len(event.keysym) == 1 and ord(event.keysym) == 17: # ^Q
        quit()
    elif event.keysym in ('s', 'S'): # a modified command!
        select_new_file()
    elif event.keysym in ('y', 'Y'):
        toggle_ascii_filter()
    elif event.keysym == "exclam": # a new command!
        cycle_colors()

################################################################################

# Main window creation:
window = tkinter.Tk()
window.geometry("1024x768")
window.title(TITLE)
window.config(bg=bg_color)

# Input file selection:
filename = tkinter.filedialog.askopenfilename(title='Select a file')
if os.path.exists(filename) :
    # Main frame creation:
    frame = tkinter.LabelFrame(window, text="Filename : " + filename, foreground=fg_color, background=bg_color, padx=5, takefocus=0)
    frame.pack(fill="both", expand="yes")

    # "panels" creation:
    frame_1 = tkinter.LabelFrame(frame, text="Offset", foreground=fg_color, background=bg_color, takefocus=0)
    frame_1.grid(in_=frame, row=0, column=0, padx=5)
    set_both_display_mode(display=False)
    frame_4 = tkinter.LabelFrame(frame, text="Settings", foreground=fg_color, background=bg_color, takefocus=0)
    frame_4.grid(in_=frame, row=1, column=0, columnspan=3, padx=5, sticky="nesw")
    display_settings()

    # First chunk load and display:
    process_first_chunk()

    # Handle keypress events:
    window.bind_all("<Key>", handle_keypress)
    window.focus_force()

    # Wait for events:
    window.mainloop()

sys.exit(0)