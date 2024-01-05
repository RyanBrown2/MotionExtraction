# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2
from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import messagebox, Label, Button
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
DEFAULT_CONFIG = {
    'camera_num': 0,
    'camera_width': 1280,
    'camera_height': 720,
}


class MotionExtraction:
    def __init__(self, window):
        self.window = window
        self.config = {}
        self.load_config()
        self.cap = cv2.VideoCapture(self.config['camera_num'])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['camera_width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['camera_height'])
        self.setup_gui()

    def load_config(self):
        # check if config file exists
        # if not os.path.exists(CONFIG_PATH):
        #     with open(CONFIG_PATH, 'w') as f:
        #         yaml.dump(DEFAULT_CONFIG, f)
        #     self.config = DEFAULT_CONFIG
        # else:
        #     with open(CONFIG_PATH, 'r') as f:
        #         data = yaml.safe_load(f)
        #     self.config = data
        self.config = DEFAULT_CONFIG

    def setup_gui(self):
        label_widget = Label(self.window)
        label_widget.pack()
        button = Button(self.window, text="Open Camera", command=lambda: self.open_camera(label_widget))
        button.pack()

    def open_camera(self, widget):
        _, frame = self.cap.read()

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        capture_image = Image.fromarray(opencv_image)
        photo = ImageTk.PhotoImage(image=capture_image)
        widget.photo_image = photo
        widget.configure(image=photo)
        widget.after(10, lambda: self.open_camera(widget))


if __name__ == '__main__':
    # config = load_config()
    # print(config)

    root = tk.Tk()
    root.title("Motion Extraction")
    root.geometry("1280x720")
    root.bind('<Escape>', lambda e: root.quit())  # press Esc to close app
    MotionExtraction(root)
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
