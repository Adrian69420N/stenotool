from tkinter import *
from tkinter import filedialog
from PIL import Image

# function to convert a text message to binary
def text_to_binary(message):
    binary_message = ''.join(format(ord(i), '08b') for i in message)
    return binary_message

# function to convert a binary message to text
def binary_to_text(binary_message):
    message = ''
    for i in range(0, len(binary_message), 8):
        message += chr(int(binary_message[i:i+8], 2))
    return message

# function to hide a message in an image
def hide_message_in_image(image_file, message, output_file):
    # open the image file
    image = Image.open(image_file)

    # convert the message to binary
    binary_message = text_to_binary(message)

    # get the pixels of the image
    pixels = image.load()

    # get the size of the image
    width, height = image.size

    # make sure the message will fit in the image
    if len(binary_message) > (width * height):
        raise ValueError('Message too large to hide in image')

    # loop through the pixels and hide the message in the least significant bit of each color channel
    index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if index < len(binary_message):
                r = (r & ~1) | int(binary_message[index])
                index += 1
            if index < len(binary_message):
                g = (g & ~1) | int(binary_message[index])
                index += 1
            if index < len(binary_message):
                b = (b & ~1) | int(binary_message[index])
                index += 1
            pixels[x, y] = (r, g, b)

    # save the modified image
    image.save(output_file)

# function to extract a message from an image
def extract_message_from_image(image_file):
    # open the image file
    image = Image.open(image_file)

    # get the pixels of the image
    pixels = image.load()

    # get the size of the image
    width, height = image.size

    # loop through the pixels and extract the least significant bit of each color channel to recover the message
    binary_message = ''
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

    # convert the binary message to text
    message = binary_to_text(binary_message)

    return message

# function to handle the "Choose File" button for the message input
def choose_message_file():
    global message_file_path
    message_file_path = filedialog.askopenfilename()

# function to handle the "Choose File" button for the image input
def choose_image_file():
    global image_file_path
    image_file_path = filedialog.askopenfilename()

# function to handle the "Hide Message" button
def hide_message():
    global message_file_path
    global image_file_path

    # get the message from the message file
    with open(message_file_path, 'r') as f:
        message = f.read()

        # hide the message in the image
    output_file_path = filedialog.asksaveasfilename(defaultextension='.png')
    try:
        hide_message_in_image(image_file_path, message, output_file_path)
    except ValueError as e:
        messagebox.showerror('Error', str(e))
        return

    messagebox.showinfo('Success', 'Message hidden in image and saved to ' + output_file_path)
    # create the main window
root = Tk()
root.title('Image Steganography')

# create the message input section
message_frame = Frame(root)
message_frame.pack(fill=BOTH, padx=10, pady=10)

message_label = Label(message_frame, text='Message:')
message_label.pack(side=LEFT)

message_button = Button(message_frame, text='Choose File', command=choose_message_file)
message_button.pack(side=RIGHT)

# create the image input section
image_frame = Frame(root)
image_frame.pack(fill=BOTH, padx=10, pady=10)

image_label = Label(image_frame, text='Image:')
image_label.pack(side=LEFT)

image_button = Button(image_frame, text='Choose File', command=choose_image_file)
image_button.pack(side=RIGHT)

# create the hide message button
hide_button = Button(root, text='Hide Message', command=hide_message)
hide_button.pack(padx=10, pady=10)

# run the main loop
root.mainloop()

