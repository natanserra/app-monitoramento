import sys
import psutil
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QFont

# Constants
FONT_SIZE = 18
UPDATE_INTERVAL = 1000  # milliseconds
WINDOW_SIZE = (200, 130)
INITIAL_POSITION = (100, 100)

class TransparentMonitor(QWidget):
    """A transparent widget that displays CPU and memory usage."""

    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_dragging = False
        self.drag_position = QPoint()

    def initUI(self):
        """Initialize the user interface."""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        font = QFont()
        font.setPointSize(FONT_SIZE)

        self.cpu_label = QLabel('CPU Usage: 0%')
        self.cpu_label.setFont(font)
        self.cpu_label.setStyleSheet("color: white;")
        layout.addWidget(self.cpu_label)

        self.memory_label = QLabel('Memory Usage: 0%')
        self.memory_label.setFont(font)
        self.memory_label.setStyleSheet("color: white;")
        layout.addWidget(self.memory_label)

        # Add close button
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("background-color: red; color: white;")
        self.close_button.clicked.connect(self.close_application)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.resize(*WINDOW_SIZE)
        self.move(*INITIAL_POSITION)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(UPDATE_INTERVAL)

    def update_stats(self):
        """Update CPU and memory usage statistics."""
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
            memory_usage = psutil.virtual_memory().percent
            self.cpu_label.setText(f'CPU Usage: {cpu_usage:.1f}%')
            self.memory_label.setText(f'Memory Usage: {memory_usage:.1f}%')
        except Exception as e:
            print(f"Error updating stats: {e}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False

    def close_application(self):
        """Completely close the application."""
        self.timer.stop()  # Stop the update timer
        QApplication.quit()  # Quit the application

if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = TransparentMonitor()
    monitor.show()
    sys.exit(app.exec_())