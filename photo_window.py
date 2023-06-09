import tkinter as tk
from PIL import ImageTk, Image

# List of image paths
image_paths = ["C:/Users/vicky/Pictures/Screenshots/Screenshot (6).png","brush.png","C:/Users/vicky/Pictures/Screenshots/Screenshot (5).png"]

# Initialize Tkinter
root = tk.Tk()
root.title("Image Viewer")

# Create a label to display the images
image_label = tk.Label(root)
image_label.pack()

# Variable to track the current image index
current_image_index = 0

# Function to update the displayed image
def update_image():
    global current_image_index
    image_path = image_paths[current_image_index]
    image = Image.open(image_path)
    image = image.resize((400, 400))  # Adjust the size as per your requirements
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo

# Function to handle arrow key presses
def on_arrow_key(event):
    global current_image_index
    if event.keysym == "Right":
        current_image_index = (current_image_index + 1) % len(image_paths)
    elif event.keysym == "Left":
        current_image_index = (current_image_index - 1) % len(image_paths)
    update_image()

# Bind the arrow key events to the function
root.bind("<Right>", on_arrow_key)
root.bind("<Left>", on_arrow_key)

# Display the initial image
update_image()

# Start the Tkinter event loop
root.mainloop()
