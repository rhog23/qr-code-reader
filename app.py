import cv2
import qrcode
import tkinter as tk
from PIL import Image, ImageTk
from pyzbar import pyzbar

# Widgets styling
from tkinter import ttk

# Browse and specify file paths
from tkinter import filedialog as fd

# Displays additional messages for debugging
from tkinter.messagebox import showerror, askyesno


def close_window():
    """
    Confirm with users before closing the window
    """
    if askyesno(
        title="Close QR Code Generator and Scanner",
        message="Are you sure you want to close the application?",
    ):
        window.destroy()


def read_barcode(frame):
    barcodes = pyzbar.decode(frame)
    if barcodes:
        # If any barcode is found
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            barcode_info = barcode.data.decode("utf-8")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 1, (0, 255, 0), 1)

            # Update the label with the barcode information
            data_label.config(text=barcode_info)
    else:
        # No barcode found, clear the label
        data_label.config(text="")

    return frame


def update_frame():
    ret, frame = camera.read()
    if ret:
        frame = read_barcode(frame)
        # Convert the frame to RGB and then to ImageTk format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the image in the Tkinter label
        image_label2.imgtk = imgtk
        image_label2.configure(image=imgtk)

    # Call the function again after 10 ms
    window.after(10, update_frame)


def open_camera():
    global camera
    camera = cv2.VideoCapture(0)
    update_frame()


def copy():
    window.clipboard_clear()
    window.clipboard_append(data_label.cget("text"))
    window.update()


# Initialize Tkinter window
window = tk.Tk()
window.title("QR Code Generator and Scanner")
# Display window icon in .ico format
window.iconbitmap(r"./icons/icon.ico")
# Dimensions and position of window
window.geometry("800x480+440+180")
window.resizable(height=False, width=False)
window.protocol("WM_DELETE_WINDOW", close_window)

# Styles for the widgets, labels, entries, and buttons
label_style = ttk.Style()
label_style.configure("TLabel", foreground="#000000", font=("OCR A Extended", 11))
entry_style = ttk.Style()
entry_style.configure("TEntry", font=("Dotum", 15))
button_style = ttk.Style()
button_style.configure("TButton", foreground="#000000", font=("DotumChe", 10))

# Create the Notebook widget
tab_control = ttk.Notebook(window)
second_tab = ttk.Frame(tab_control)
tab_control.add(second_tab, text="QR Code Scanner")
tab_control.pack(expand=1, fill="both")

second_canvas = tk.Canvas(second_tab, width=800, height=480)
second_canvas.pack()

# Widgets for the second tab
image_label2 = ttk.Label(window)
data_label = ttk.Label(window)
second_canvas.create_window(
    200, 240, window=image_label2
)  # Position for camera feed on the left side
second_canvas.create_window(
    600, 240, window=data_label
)  # Position for barcode info on the right side

camera_button = ttk.Button(
    window, text="Turn On Camera", style="TButton", command=open_camera
)
second_canvas.create_window(250, 430, window=camera_button)
copy_button = ttk.Button(window, text="Copy", style="TButton", command=copy)
second_canvas.create_window(350, 430, window=copy_button)
reset_button2 = ttk.Button(window, text="Reset", style="TButton", state="disabled")
second_canvas.create_window(450, 430, window=reset_button2)

window.mainloop()
