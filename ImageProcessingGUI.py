import sys, os
import numpy as np #numerical operations
import cv2 #openCV for image processing
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox,
    QFileDialog, QHBoxLayout
) #GUI
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image #image processing
import imageio #image reading and writing

photoPath = "testimage.png"

#making another change to see what happens

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processor GUI")
        self.setGeometry(100,100,800,600)
        self.original_image = None
        self.modified_image = None
        self.rotation_angle = 0  # Track current rotation angle
        self.blur_intensity = 5
        self.edge_threshold1 = 100
        self.edge_threshold2 = 200

        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter) 
        
        self.load_button = QPushButton("Load image")
        self.load_button.clicked.connect(self.load_image)

        self.process_button = QPushButton("Process the image")
        self.process_button.clicked.connect(self.process_image)

        self.effect_dropdown = QComboBox()
        effectsForDropdown = ["Rotate","Blur","Edge Detection"]
        self.effect_dropdown.addItems(effectsForDropdown)
        self.effect_dropdown.currentTextChanged.connect(self.apply_effect)

        self.restore_button = QPushButton("Restore original image")#Not needed!
        self.restore_button.clicked.connect(self.load_image)

        button_layoutRow1 = QHBoxLayout()
        button_layoutRow1.addWidget(self.load_button)
        #button_layoutRow1.addWidget(self.restore_button)

        button_layoutRow2 = QHBoxLayout()
        button_layoutRow2.addWidget(self.effect_dropdown)
        button_layoutRow2.addWidget(self.process_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layoutRow1)
        layout.addLayout(button_layoutRow2)
        self.setLayout(layout)

    def load_image(self):
        if photoPath:
            self.image_path = photoPath
            self.original_image = cv2.imread(photoPath)
            self.current_image = self.original_image.copy()
            self.debugger(f"Loaded image from {photoPath}")
            self.display_image(self.current_image)

    def process_image(self):       
        try:
            effect = self.effect_dropdown.currentText()
            self.current_image = self.apply_effect(effect)
            self.debugger(f"Processed Image with {effect}!")
            self.display_image(self.current_image)
        except AttributeError:
            print("You have to load an image first!")

    def apply_effect(self,effect):
        img = self.current_image.copy()
        if effect =="Rotate":
            img = self.rotate_image(img)
        elif effect =="Blur":
            img = self.blur_image(img)
        elif effect =="Edge Detection":
            img = self.detect_edges(img)
        return img

    def detect_edges(self,img):
        #print(type(img))
        self.edge_threshold1 = self.edge_threshold1 + 5
        #self.edge_threshold2 = self.edge_threshold1*2 #Using fixed ratio
        if len(img.shape) == 3 and img.shape[2] == 3:
            grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            grayImage = img  # already grayscale
        processedImage =  cv2.Canny(grayImage,self.edge_threshold1,self.edge_threshold1*2)
        return processedImage

    def blur_image(self,img):
        self.blur_intensity = 11
        #self.blur_intensity = (self.blur_intensity + 4)  # Increment blur intensity
        processedImage = cv2.GaussianBlur(img,(11,11),0)
        return processedImage
    
    def rotate_image(self, img):
        self.rotation_angle = (self.rotation_angle + 10) % 360  # Increment angle
        rows,cols = img.shape[:2]
        # cols-1 and rows-1 are the coordinate limits.
        M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),self.rotation_angle,1)
        processedImage = cv2.warpAffine(img,M,(cols,rows))
        return processedImage

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

