import tkinter as tk
from tkinter.colorchooser import askcolor
from lipstick_application import VirtualLipstick
from eyeshadow_application import VirtualEyeshadow
from blush_application import VirtualBlush
import cv2
from PIL import Image, ImageTk

class MakeupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Makeup Application")

        self.cap = cv2.VideoCapture(0)
        self.lipstick = VirtualLipstick()
        self.eyeshadow = VirtualEyeshadow()
        self.blush = VirtualBlush()

        self.lipstick_color = (0, 0, 255)
        self.eyeshadow_color = (128, 0, 128)
        self.blush_color = (255, 192, 203)

        self.setup_gui()

    def setup_gui(self):
        self.label = tk.Label(self.root)
        self.label.pack()

        self.lipstick_btn = tk.Button(self.root, text="Choose Lipstick Color", command=self.choose_lipstick_color)
        self.lipstick_btn.pack()

        self.eyeshadow_btn = tk.Button(self.root, text="Choose Eyeshadow Color", command=self.choose_eyeshadow_color)
        self.eyeshadow_btn.pack()

        self.blush_btn = tk.Button(self.root, text="Choose Blush Color", command=self.choose_blush_color)
        self.blush_btn.pack()

        self.update_frame()

    def choose_lipstick_color(self):
        color = askcolor()[0]
        if color:
            self.lipstick_color = tuple(int(c) for c in color)

    def choose_eyeshadow_color(self):
        color = askcolor()[0]
        if color:
            self.eyeshadow_color = tuple(int(c) for c in color)

    def choose_blush_color(self):
        color = askcolor()[0]
        if color:
            self.blush_color = tuple(int(c) for c in color)

    def update_frame(self):
        ret, frame = self.cap.read()
        frame = self.lipstick.apply_lipstick(frame, self.lipstick_color)
        frame = self.eyeshadow.apply_eyeshadow(frame, self.eyeshadow_color)
        frame = self.blush.apply_blush(frame, self.blush_color)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        self.root.after(10, self.update_frame)

def main():
    root = tk.Tk()
    app = MakeupApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()