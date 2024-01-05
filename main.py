# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from collections import deque
import cv2
from PIL import Image, ImageTk
import os
import time
import tkinter as tk
from tkinter import messagebox, Label, Button
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
DEFAULT_CONFIG = {
    'camera_num': 0,
    'camera_width': 1280,
    'camera_height': 720,
    'motion_delay': 1,  # in seconds
}


def overlay_images(background, overlay, opacity=0.5):
    """
    Overlays an image on another image with given opacity.
    :param background: Background Image
    :param overlay: Image to overlay
    :param opacity: Opacity of the overlay image
    :return: New image with overlay
    """
    # Resize overlay image to match background image size
    overlay_resized = cv2.resize(overlay, (background.shape[1], background.shape[0]))

    # Blend images
    return cv2.addWeighted(background, 1, overlay_resized, opacity, 0)


def create_motion_frame(current_frame, previous_frame):
    inverted_previous_frame = 255 - previous_frame
    # inverted_previous_frame = cv2.bitwise_not(previous_frame)
    return overlay_images(current_frame, inverted_previous_frame, 1)


class MotionExtraction:
    def __init__(self, window):
        self.window = window
        self.config = {}
        self.load_config()
        print("Creating Camera")
        self.cap = cv2.VideoCapture(self.config['camera_num'])
        print("Setting Camera Properties")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['camera_width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['camera_height'])

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        max_frames = int(self.fps * self.config['motion_delay'])
        self.frame_deque = deque(maxlen=max_frames)

        self.setup()

    def load_config(self):
        # check if config file exists
        if not os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'w') as f:
                yaml.dump(DEFAULT_CONFIG, f)
            self.config = DEFAULT_CONFIG
        else:
            with open(CONFIG_PATH, 'r') as f:
                data = yaml.safe_load(f)
            self.config = data

    def setup(self):
        label_widget = Label(self.window)
        label_widget.pack()
        button = Button(self.window, text="Open Camera", command=lambda: self.open_camera(label_widget))
        button.pack()

    def open_camera(self, widget):
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to open camera")
            return

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        self.frame_deque.append((time.time(), opencv_image))

        motion_image = create_motion_frame(opencv_image, self.get_past_frame(self.config['motion_delay']))

        capture_image = Image.fromarray(motion_image)
        photo = ImageTk.PhotoImage(image=capture_image)
        widget.photo_image = photo
        widget.configure(image=photo)
        widget.after(10, lambda: self.open_camera(widget))

    def get_past_frame(self, seconds):
        current_time = time.time()
        target_time = current_time - seconds
        closest_frame = min(self.frame_deque, key=lambda x: abs(x[0] - target_time))[1]
        return closest_frame


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Motion Extraction")
    root.geometry("1280x720")
    root.bind('<Escape>', lambda e: root.quit())  # press Esc to close app
    MotionExtraction(root)
    root.mainloop()
