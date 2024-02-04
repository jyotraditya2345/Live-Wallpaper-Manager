import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import cv2

def change_wallpaper(image_path):
    applescript_command = f'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
    subprocess.run(['osascript', '-e', applescript_command])

def extract_frames(video_path, output_folder, target_fps):
    cap = cv2.VideoCapture(video_path)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))  # Get the frame rate of the video
    success, image = cap.read()
    count = 0

    while success:
        frame_path = os.path.join(output_folder, f"frame_{count}.jpg")
        cv2.imwrite(frame_path, image)
        count += 1

        # Skip frames to achieve target_fps
        for _ in range(int(frame_rate / target_fps) - 1):
            cap.read()

        success, image = cap.read()

    cap.release()
    return frame_rate, count

class ImageSliderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Slider")
        self.image_list = []
        self.current_index = 0

        # Create and configure widgets
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.load_images_button = tk.Button(root, text="Load Images", command=self.load_images)
        self.load_images_button.pack(pady=10)

    def load_images(self):
        file_path = filedialog.askopenfilename(title="Select File")
        if file_path:
            file_extension = os.path.splitext(file_path)[-1].lower()

            if file_extension == '.mp4':
                folder_path = os.path.join(os.path.dirname(file_path), "frames")
                os.makedirs(folder_path, exist_ok=True)
                frame_rate, total_frames = extract_frames(file_path, folder_path, target_fps=120)
                self.image_list = [os.path.join(folder_path, f"frame_{i}.jpg") for i in range(total_frames)]
                interval = int(1000 / 240)  # Set interval for running at 240 fps
            else:
                self.image_list = [file_path]
                interval = int(1000 / 240)  # Set interval for running at 240 fps

            self.current_index = 0  # Reset index when loading new images
            self.show_current_image()

            # Schedule the show_next function to be called again at the calculated interval
            self.root.after(interval, self.show_next)

    def show_current_image(self):
        if self.image_list:
            image_path = self.image_list[self.current_index]
            # image = Image.open(image_path)
            # image.thumbnail((400, 400))  # Resize image for display
            # tk_image = ImageTk.PhotoImage(image)

            # self.image_label.config(image=tk_image)
            # self.image_label.image = tk_image
            change_wallpaper(image_path)

    def show_next(self):
        if self.image_list:
            self.current_index = (self.current_index + 1) % len(self.image_list)
            self.show_current_image()

            # Schedule the show_next function to be called again at the calculated interval
            self.root.after(int(1000 / 240), self.show_next)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSliderApp(root)
    root.mainloop()
