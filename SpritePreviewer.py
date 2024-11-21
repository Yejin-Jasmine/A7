import math
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QFrame, \
    QMenuBar, QMenu
from PyQt6.QtCore import QTimer, Qt


class SpritePreview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")

        # Load sprite frames
        self.num_frames = 20  # Adjust as per your sprites
        self.frames = self.load_sprite('spriteImages', self.num_frames)

        # Animation-related attributes
        self.current_frame = 0
        self.is_animating = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)

        # Set up the UI
        self.setupUI()

    def load_sprite(self, sprite_folder_name, number_of_frames):
        frames = []
        padding = math.ceil(math.log(number_of_frames - 1, 10))
        for frame in range(number_of_frames):
            folder_and_file_name = f"{sprite_folder_name}/sprite_{str(frame).zfill(padding)}.png"
            frames.append(QPixmap(folder_and_file_name))
        return frames

    def setupUI(self):
        # Central frame and layout
        frame = QFrame()
        layout = QVBoxLayout(frame)

        # Sprite display
        self.sprite_label = QLabel()
        self.sprite_label.setPixmap(self.frames[0])
        layout.addWidget(self.sprite_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # FPS slider and labels
        fps_layout = QHBoxLayout()
        self.fps_label = QLabel("Frames per second: 1")
        fps_static_label = QLabel("Frames per second")
        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setRange(1, 60)
        self.fps_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fps_slider.setTickInterval(5)
        self.fps_slider.valueChanged.connect(self.update_fps)

        fps_layout.addWidget(fps_static_label)
        fps_layout.addWidget(self.fps_slider)
        fps_layout.addWidget(self.fps_label)
        layout.addLayout(fps_layout)

        # Start/Stop button
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.clicked.connect(self.toggle_animation)
        layout.addWidget(self.start_stop_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Menu
        menu_bar = QMenuBar()
        file_menu = QMenu("File", self)
        pause_action = file_menu.addAction("Pause")
        exit_action = file_menu.addAction("Exit")
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

        # Menu actions
        pause_action.triggered.connect(self.pause_animation)
        exit_action.triggered.connect(self.close)

        self.setCentralWidget(frame)

    def update_fps(self):
        fps = self.fps_slider.value()
        self.fps_label.setText(f"Frames per second: {fps}")
        if self.is_animating:
            self.timer.setInterval(int(1000 / fps))

    def toggle_animation(self):
        if self.is_animating:
            self.timer.stop()
            self.start_stop_button.setText("Start")
        else:
            fps = self.fps_slider.value()
            self.timer.start(int(1000 / fps))
            self.start_stop_button.setText("Stop")
        self.is_animating = not self.is_animating

    def pause_animation(self):
        self.timer.stop()
        self.start_stop_button.setText("Start")
        self.is_animating = False

    def update_animation(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.sprite_label.setPixmap(self.frames[self.current_frame])


def main():
    app = QApplication([])
    window = SpritePreview()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
