import sys, os
import numpy as np #numerical operations
import cv2 #openCV for image processing
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QHBoxLayout
) #GUI
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image #image processing
import imageio #image reading and writing

photoPath = "testimage.png"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processor GUI")
        self.setGeometry(100,100,800,600)
        self.image = None
        self.image_path = photoPath

        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter) 
        
        self.load_button = QPushButton("Load image")
        self.load_button.clicked.connect(self.load_image)

        self.process_button = QPushButton("Process the image")
        self.process_button.clicked.connect(self.process_image)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.process_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def process_image(self):
        if photoPath:
            self.image = cv2.imread(photoPath)
            newImage = self.image.copy()
            # Perform image processing here
            newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)

            # Perform image processing here
            self.display_image(newImage)




    def load_image(self):
        if photoPath:
            self.image_path = photoPath
            self.image = cv2.imread(photoPath)
            self.display_image(self.image)

    def display_image(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
