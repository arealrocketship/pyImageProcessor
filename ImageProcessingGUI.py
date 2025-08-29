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
        self.rotation_angle = 0  # Track current rotation angle

        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter) 
        
        self.load_button = QPushButton("Load image")
        self.load_button.clicked.connect(self.load_image)

        self.process_button = QPushButton("Process the image")
        self.process_button.clicked.connect(self.process_image)

        self.restore_button = QPushButton("Restore original image")
        self.restore_button.clicked.connect(self.restore_image)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.restore_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def restore_image(self):
        # Restore the image to its original state and reset rotation
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.rotation_angle = 0
            self.debugger("Restored Original Image")
            self.display_image(self.image)

    def process_image(self):       
        if self.image is not None:
            self.rotation_angle = (self.rotation_angle + 10) % 360  # Increment angle
            newImage = self.image.copy()
            newImage = self.rotate_image(newImage, self.rotation_angle)
            self.debugger("Processed Image")
            self.display_image(newImage)

    def rotate_image(self, img, numDegrees):
        rows,cols = img.shape[:2]
        # cols-1 and rows-1 are the coordinate limits.
        M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),numDegrees,1)
        dst = cv2.warpAffine(img,M,(cols,rows))
        return dst
    
    def load_image(self):
        if photoPath:
            self.image_path = photoPath
            self.image = cv2.imread(photoPath)
            self.originalImage = self.image.copy()
            self.debugger(f"Loaded image from {self.image_path}")
            self.display_image(self.image)

    def debugger(self,message):
        print(f"{message}")

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

