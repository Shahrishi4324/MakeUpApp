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

        self.lipstick_intensity = 50
        self.eyeshadow_intensity = 50
        self.blush_intensity = 50

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

        tk.Label(self.root, text="Lipstick Intensity").pack()
        self.lipstick_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_lipstick_intensity)
        self.lipstick_slider.set(self.lipstick_intensity)
        self.lipstick_slider.pack()

        tk.Label(self.root, text="Eyeshadow Intensity").pack()
        self.eyeshadow_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_eyeshadow_intensity)
        self.eyeshadow_slider.set(self.eyeshadow_intensity)
        self.eyeshadow_slider.pack()

        tk.Label(self.root, text="Blush Intensity").pack()
        self.blush_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_blush_intensity)
        self.blush_slider.set(self.blush_intensity)
        self.blush_slider.pack()

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

    def update_lipstick_intensity(self, value):
        self.lipstick_intensity = int(value)

    def update_eyeshadow_intensity(self, value):
        self.eyeshadow_intensity = int(value)

    def update_blush_intensity(self, value):
        self.blush_intensity = int(value)

    def apply_transparent_overlay(self, img, overlay, alpha):
        return cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    def update_frame(self):
        ret, frame = self.cap.read()
        
        # Apply makeup with intensity control
        lipstick_overlay = self.lipstick.apply_lipstick(frame.copy(), self.lipstick_color)
        frame = self.apply_transparent_overlay(frame, lipstick_overlay, self.lipstick_intensity / 100)
        
        eyeshadow_overlay = self.eyeshadow.apply_eyeshadow(frame.copy(), self.eyeshadow_color)
        frame = self.apply_transparent_overlay(frame, eyeshadow_overlay, self.eyeshadow_intensity / 100)

        blush_overlay = self.blush.apply_blush(frame.copy(), self.blush_color)
        frame = self.apply_transparent_overlay(frame, blush_overlay, self.blush_intensity / 100)

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