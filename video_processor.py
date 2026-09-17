import cv2
import mediapipe as mp


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles


def process_video(video_path, rotate=False):
    """
    Lê um vídeo, aplica MediaPipe Pose e devolve uma lista de frames
    já com os pontos do corpo desenhados.
    """

    frames = []

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError("Não foi possível abrir o vídeo.")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps is None or fps <= 0:
        fps = 30

    frame_time = 1.0 / fps

    with mp_pose.Pose(
        model_complexity=1,
        static_image_mode=False,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if rotate:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            frame_marked = frame.copy()

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame_marked,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style()
                )

            frames.append(frame_marked)

    cap.release()

    return frames, frame_time