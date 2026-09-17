import cv2
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage


class VideoDisplay:
    def __init__(self, video_label, master_frame=None):
        self.video_label = video_label

        self.frames = []
        self.frame_idx = 0
        self.frame_time = 33
        self.paused = True
        self.scale = 0.5
        self.num_frames = 0

        if master_frame is not None:
            self.prev_button = ctk.CTkButton(
                master_frame,
                text="◀",
                width=40,
                command=self.prev_frame
            )
            self.prev_button.pack(side="left", padx=5)

            self.slider = ctk.CTkSlider(
                master_frame,
                from_=0,
                to=1,
                command=self.on_slider_move,
                number_of_steps=1
            )
            self.slider.pack(side="left", fill="x", expand=True, padx=5)

            self.next_button = ctk.CTkButton(
                master_frame,
                text="▶",
                width=40,
                command=self.next_frame
            )
            self.next_button.pack(side="left", padx=5)

            self.play_pause_button = ctk.CTkButton(
                master_frame,
                text="Play",
                command=self.toggle_play_pause
            )
            self.play_pause_button.pack(side="left", padx=5)
        else:
            self.slider = None
            self.play_pause_button = None

    def start(self, frames, frame_time):
        self.frames = frames
        self.frame_time = int(frame_time * 1000)
        self.num_frames = len(frames)
        self.frame_idx = 0
        self.paused = True

        if self.slider is not None:
            self.slider.configure(
                from_=0,
                to=max(self.num_frames - 1, 1),
                number_of_steps=max(self.num_frames - 1, 1)
            )
            self.slider.set(0)

        if self.play_pause_button is not None:
            self.play_pause_button.configure(text="Play")

        self.update_frame()

    def update_frame(self):
        if not self.frames:
            return

        frame = self.frames[self.frame_idx]

        if self.scale != 1.0:
            frame = cv2.resize(
                frame,
                (
                    int(frame.shape[1] * self.scale),
                    int(frame.shape[0] * self.scale)
                )
            )

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image_rgb)

        ctk_img = CTkImage(
            dark_image=img,
            light_image=img,
            size=(img.width, img.height)
        )

        self.video_label.configure(text="", image=ctk_img)
        self.video_label.image = ctk_img

        if self.slider is not None:
            self.slider.set(self.frame_idx)

        if not self.paused:
            self.frame_idx += 1

            if self.frame_idx >= self.num_frames:
                self.frame_idx = 0

            self.video_label.after(self.frame_time, self.update_frame)

    def toggle_play_pause(self):
        if not self.frames:
            return

        self.paused = not self.paused

        if self.paused:
            self.play_pause_button.configure(text="Play")
        else:
            self.play_pause_button.configure(text="Pause")
            self.update_frame()

    def next_frame(self):
        if not self.frames:
            return

        self.paused = True
        self.play_pause_button.configure(text="Play")

        self.frame_idx = min(self.frame_idx + 1, self.num_frames - 1)
        self.update_frame()

    def prev_frame(self):
        if not self.frames:
            return

        self.paused = True
        self.play_pause_button.configure(text="Play")

        self.frame_idx = max(self.frame_idx - 1, 0)
        self.update_frame()

    def on_slider_move(self, value):
        if not self.frames:
            return

        self.paused = True
        self.play_pause_button.configure(text="Play")

        self.frame_idx = int(float(value))
        self.update_frame()