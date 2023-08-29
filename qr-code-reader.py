# Requirements: qrcode, opencv-python, pillow, pyzbar

import cv2
import qrcode
import tkinter as tk
from PIL import Image
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
    if askyesno(title='Close QR Code Generator and Scanner', message='Are you sure you want to close the application?'):
        window.destroy()

def generate_qrcode():
    """
    Function for generating the QR Code
    """
    qrcode_data = str(data_entry.get())
    qrcode_name = str(filename_entry.get())
    if qrcode_name == '':
        showerror(title='Error', message='An error occured.\n' \
                  '\nThe following is the cause:\n   -> Empty filename entry field\n\n' \
                  'Make sure the filename entry field is filled when generating the QRCode.')
    else:
        if askyesno(title='Confirmation', message=f'Do you want to create a QRCode with the provided information?'):
            try:
                qr = qrcode.QRCode(version=1, box_size=6, border=4)
                qr.add_data(qrcode_data)
                qr.make(fit=True)
                name = qrcode_name + '.png'
                qrcode_image = qr.make_image(fill_color='black', back_color='white')
                qrcode_image.save(name)
                global Image
                Image = tk.PhotoImage(file=f'{name}')
                image_label1.config(image=Image)
                reset_button.config(state='normal', command=reset)
            except:
                showerror(title='Error', message='Please provide a valid filename')

def reset():
    """
    Function for resetting or clearing the image label
    """
    if askyesno(title='Reset', message='Are you sure you want to reset?'):
        image_label1.config(image='')
        image_label2.config(image='')
        reset_button.config(state='disabled')
        reset_button2.config(state='disabled')
        data_label.config(text='')
        data_entry.delete(0, 'end')
        filename_entry.delete(0, 'end')
        file_entry.delete(0, 'end')

def open_dialog():
    filetypes = (('PNG extension', '*.png'), ('JPG extension', '*.jpg'), ('JPEG extension', '*.jpeg'), ('All Files', '*.*'))
    name = fd.askopenfilename(title='Select file', filetypes=filetypes)
    file_entry.delete(0, 'end')
    file_entry.insert(0, name)

def detect_qrcode():
    """
    Function to detect QRCode from image
    """
    image_file = file_entry.get()
    if image_file == '':
        showerror(title='Error', message='Please provide a QR Code image file to detect')
    else:
        try:
            global qrcode_image
            qrcode_image = tk.PhotoImage(file=f'{image_file}')
            image_label2.config(image=qrcode_image)

            qr_img = cv2.imread(f'{image_file}')
            data = pyzbar.decode(qr_img)
            for name in data:
                info = name.data.decode('utf-8')
            data_label.config(text=info)
            reset_button2.config(state='normal', command=reset)
        except:
            showerror(title='Error', message='An error occured while detecting data from the provided file.\n' \
                  '\nThe following is the cause:\n   -> Wrong image file\n\n' \
                  'Make sure the image file is a valid QRCode.')

def read_barcode(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x+6, y-6), font, 1, (255, 255, 255), 1)

        data_label.config(text=barcode_info)

    return frame

def open_camera():
    """
    VideoCaptureModes:
        CAP_MODE_BGR  = 0,
        CAP_MODE_RGB  = 1,
        CAP_MODE_GRAY = 2,
        CAP_MODE_YUYV = 3

    VideoCaptureProperties:
        CAP_PROP_POS_MSEC             = 0,       # Current position of video file in milliseconds
        CAP_PROP_POS_FRAMES           = 1,       # 0-based index of the frame to be decoded/captured next
        CAP_PROP_POS_AVI_RATIO        = 2,       # Relative position of the video file: 0=start of the film, 1=end of the film
        CAP_PROP_FRAME_WIDTH          = 3,       # Width of the frames in the video stream
        CAP_PROP_FRAME_HEIGHT         = 4,       # Height of the frames in the video stream
        CAP_PROP_FPS                  = 5,       # Frame rate
        CAP_PROP_FOURCC               = 6,       # 4-character code of codec
        CAP_PROP_FRAME_COUNT          = 7,       # Number of frames in the video file
        CAP_PROP_FORMAT               = 8,       # Format of the Mat objects
        CAP_PROP_MODE                 = 9,       # Backend-specific value indicating the current capture mode
        CAP_PROP_BRIGHTNESS           = 10,      # Brightness of the image
        CAP_PROP_CONTRAST             = 11,      # Constrast of the image
        CAP_PROP_SATURATION           = 12,      # Saturation of the image
        CAP_PROP_HUE                  = 13,      # Hue of the image
        CAP_PROP_GAIN                 = 14,      # Gain of the image
        CAP_PROP_EXPOSURE             = 15,      # Exposure
        CAP_PROP_CONVERT_RGB          = 16,      # Boolean flags indicating whether images shoyld be converted to RGB
        CAP_PROP_WHITE_BALANCE_BLUE_U = 17,      # Currently unsupported
        CAP_PROP_RECTIFICATION        = 18,      # Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)
        CAP_PROP_MONOCHROME           = 19,      #
        CAP_PROP_SHARPNESS            = 20,      #
        CAP_PROP_AUTO_EXPOSURE        = 21,      # DC1394: exposure control done by camera, user can adjust reference level using this feature.
        CAP_PROP_GAMMA                = 22,      #
        CAP_PROP_TEMPERATURE          = 23,      #
        CAP_PROP_TRIGGER              = 24,      #
        CAP_PROP_TRIGGER_DELAY        = 25,      #
        CAP_PROP_WHITE_BALANCE_RED_V  = 26,      #
        CAP_PROP_ZOOM                 = 27,      #
        CAP_PROP_FOCUS                = 28,      #
        CAP_PROP_GUID                 = 29,      #
        CAP_PROP_ISO_SPEED            = 30,      #
        CAP_PROP_BACKLIGHT            = 32,      #
        CAP_PROP_PAN                  = 33,      #
        CAP_PROP_TILT                 = 34,      #
        CAP_PROP_ROLL                 = 35,      #
        CAP_PROP_IRIS                 = 36,      #
        CAP_PROP_SETTINGS             = 37,      # Pop up video/camera filter dialog (note: only supported by DSHOW backend currently. The property value is ignored)
        CAP_PROP_BUFFERSIZE           = 38,      #
        CAP_PROP_AUTOFOCUS            = 39,      #
        CAP_PROP_SAR_NUM              = 40,      # Sample aspect ratio: num/den (num)
        CAP_PROP_SAR_DEN              = 41,      # Sample aspect ratio: num/den (den)
        CAP_PROP_BACKEND              = 42,      # Current backend (enum VideoCaptureAPIs). Read-only property
        CAP_PROP_CHANNEL              = 43,      # Video input or Channel Number (only for those cameras that support)
        CAP_PROP_AUTO_WB              = 44,      # Enable/ disable auto white-balance
        CAP_PROP_WB_TEMPERATURE       = 45,      # White-balance color temperature
        CAP_PROP_CODEC_PIXEL_FORMAT   = 46,      # (read-only) codec's pixel format. 4-character code
        CAP_PROP_BITRATE              = 47,      # (read-only) Video bitrate in kbits/s
        CAP_PROP_ORIENTATION_META     = 48,      # (read-only) Frame rotation defined by stream meta (applicable for FFmpeg back-end only)
        CAP_PROP_ORIENTATION_AUTO     = 49,      # if true - rotates output frames of CvCapture considering video file's metadata (applicable for FFmpeg back-end only)
        CAP_PROP_OPEN_TIMEOUT_MSEC    = 53,      #
        CAP_PROP_READ_TIMEOUT_MSEC    = 54,      #
    """
    # Computer webcam
    camera = cv2.VideoCapture(0)
    # --------------------- Use cv2.CAP_DSHOW for external camera module ---------------------
    # Reference: https://www.kurokesu.com/main/2020/07/12/pulling-full-resolution-from-a-webcam-with-opencv-windows/
    # resolution = (1920, 1080)
    # camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Enable autofocus
    # camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    # Solves the lagging issue
    # camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
    # camera.set(cv2.CAP_PROP_FPS, 24)
    # camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame = read_barcode(frame)
        cv2.imshow('Real Time QRCode / Barcode Scanner', frame)
        # Close if ESC key is pressed
        if cv2.waitKey(1) & 0xFF == 27 or data_label.cget('text'):
            break

    camera.release()
    cv2.destroyAllWindows()

def copy():
    window.clipboard_clear()
    window.clipboard_append(data_label.cget('text'))
    window.update()


# Initialize Tkinter window
window = tk.Tk()
window.title('QR Code Generator and Scanner')
# Alternate way to display window icon
# icon = tk.PhotoImage(file=r'C:/Users/yungng07/Documents/qr-code-reader/icons/icon.png')
# window.iconphoto(False, icon)
# Display window icon in .ico format
window.iconbitmap(r'C:/Users/yungng07/Documents/QRCodeReader/icons/icon.ico')
# Dimensions and position of window
window.geometry('500x480+440+180')
window.resizable(height=False, width=False)
window.protocol('WM_DELETE_WINDOW', close_window)

# Styles for the widgets, labels, entries and buttons
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 11))
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font=('DotumChe', 10))

# Create the Notebook widget
tab_control = ttk.Notebook(window)
first_tab = ttk.Frame(tab_control)
second_tab = ttk.Frame(tab_control)
tab_control.add(first_tab, text='QR Code Generator')
tab_control.add(second_tab, text='QR Code Scanner')
tab_control.pack(expand=1, fill='both')

first_canvas = tk.Canvas(first_tab, width=500, height=480)
first_canvas.pack()
second_canvas = tk.Canvas(second_tab, width=500, height=480)
second_canvas.pack()

# Widgets for first tab
image_label1 = ttk.Label(window)
first_canvas.create_window(250, 150, window=image_label1)

qrdata_label = ttk.Label(window, text='QRcode Data', style='TLabel')
data_entry = ttk.Entry(window, width=55, style='TEntry')
first_canvas.create_window(70, 330, window=qrdata_label)
first_canvas.create_window(300, 330, window=data_entry)

filename_label = ttk.Label(window, text='Filename', style='TLabel')
filename_entry = ttk.Entry(window, width=55, style='TEntry')
first_canvas.create_window(84, 360, window=filename_label)
first_canvas.create_window(300, 360, window=filename_entry)

reset_button = ttk.Button(window, text='Reset', style='TButton', state='disabled')
generate_button = ttk.Button(window, text='Generate QRCode', style='TButton', command=generate_qrcode)
first_canvas.create_window(300, 390, window=reset_button)
first_canvas.create_window(410, 390, window=generate_button)

# Widgets for second tab
image_label2 = ttk.Label(window)
data_label = ttk.Label(window)
second_canvas.create_window(250, 150, window=image_label2)
second_canvas.create_window(250, 300, window=data_label)

file_entry = ttk.Entry(window, width=60, style='TEntry')
browse_button = ttk.Button(window, text='Browse', style='TButton', command=open_dialog)
second_canvas.create_window(200, 350, window=file_entry)
second_canvas.create_window(430, 350, window=browse_button)

detect_button = ttk.Button(window, text='Scan QRCode', style='TButton', command=detect_qrcode)
second_canvas.create_window(65, 385, window=detect_button)
camera_button = ttk.Button(window, text='Turn On Camera', style='TButton', command=open_camera)
second_canvas.create_window(175, 385, window=camera_button)
copy_button = ttk.Button(window, text='Copy', style='TButton', command=copy)
second_canvas.create_window(277, 385, window=copy_button)
reset_button2 = ttk.Button(window, text='Reset', style='TButton', state='disabled')
second_canvas.create_window(370, 385, window=reset_button2)

window.mainloop()
