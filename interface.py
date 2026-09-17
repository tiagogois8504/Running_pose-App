import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from video_processor import process_video
from video_display import VideoDisplay


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Running Pose Analyser")
        self.geometry("1200x800")

        self.video_path = None
        self.video_display = None

        self._create_layout()

    def _create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.video_frame = ctk.CTkFrame(self)
        self.video_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.video_label = ctk.CTkLabel(
            self.video_frame,
            text="Carrega um vídeo para começar",
            font=ctk.CTkFont(size=22)
        )
        self.video_label.pack(expand=True, fill="both")

        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        self.upload_button = ctk.CTkButton(
            self.controls_frame,
            text="Carregar vídeo",
            command=self.load_video
        )
        self.upload_button.pack(side="left", padx=5)

        self.process_button = ctk.CTkButton(
            self.controls_frame,
            text="Processar vídeo",
            command=self.process_selected_video
        )
        self.process_button.pack(side="left", padx=5)

        self.video_controls_frame = ctk.CTkFrame(self.controls_frame)
        self.video_controls_frame.pack(side="left", fill="x", expand=True, padx=10)

        self.video_display = VideoDisplay(
            video_label=self.video_label,
            master_frame=self.video_controls_frame
        )

    def load_video(self):
        path = filedialog.askopenfilename(
            title="Escolher vídeo",
            filetypes=[
                ("Vídeos", "*.mp4 *.avi *.mov *.mkv"),
                ("Todos os ficheiros", "*.*")
            ]
        )

        if not path:
            return

        self.video_path = path
        self.video_label.configure(
            text=f"Vídeo selecionado:\n{path}",
            image=None
        )

    def process_selected_video(self):
        if self.video_path is None:
            messagebox.showwarning(
                "Sem vídeo",
                "Escolhe primeiro um vídeo."
            )
            return

        self.video_label.configure(text="A processar vídeo...")

        thread = threading.Thread(
            target=self._process_video_thread,
            daemon=True
        )
        thread.start()

    def _process_video_thread(self):
        try:
            frames, frame_time = process_video(self.video_path, rotate=False)

            self.after(
                0,
                lambda: self.video_display.start(frames, frame_time)
            )

        except Exception as e:
            error_message = f"{type(e).__name__}: {e}"

            print("[ERRO NO PROCESSAMENTO DO VÍDEO]")
            print(error_message)

            self.after(
                0,
                lambda msg=error_message: messagebox.showerror("Erro", msg)
            )