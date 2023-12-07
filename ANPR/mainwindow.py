# This Python file uses the following encoding: utf-8

import os
import re
import sys
from datetime import datetime as dt

import cv2
import easyocr
import imutils
import numpy as np
import pandas as pd
from cv2 import IMREAD_GRAYSCALE, Canny, imread, imwrite, line
from numpy import argwhere as arg
from PIL import Image as im
from PIL import ImageTk
from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtGui import QIcon, QImage, QPixmap, QWindow
from PySide6.QtWidgets import (QApplication, QColorDialog, QFileDialog, QLabel,
                               QMainWindow)

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #-------------------Start of Code-----------------#
        self.setIcon()
        self.ui.select.clicked.connect(self.loadImage)
        self.ui.process.clicked.connect(self.process)
        self.ui.extract.clicked.connect(self.extract_number_plate)
        self.ui.match.clicked.connect(self.match_license_plate_details)
        self.ui.clear.clicked.connect(self.clear)

    def loadImage(self):# gets the image path
        self.clear()
        file_dialog = QFileDialog(self)
        file_path,_ = file_dialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.bmp)")

        if file_path:
            pixmap = QPixmap(file_path)
            self.ui.selectedFrame.setPixmap(pixmap)
            self.last_loaded_path=file_path
            # self.ui.FilePath.setText(f"path:{self.last_loaded_path}")
        self.upload=True

    def process(self):
        img=imread(self.last_loaded_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = im.fromarray(gray)
        width, height = image.size
        bytes_per_line = width
        q_image = QImage(image.tobytes(), width, height, bytes_per_line, QImage.Format_Grayscale8)

        # Convert QImage to QPixmap and set it to your QLabel
        pixmap = QPixmap.fromImage(q_image)
        self.ui.gray_image.setPixmap(pixmap)
        adjusted = cv2.convertScaleAbs(gray, alpha=-1, beta=40)
        
        # bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
        iterations = 2
        bfilter = adjusted.copy()
        for _ in range(iterations):
            bfilter = cv2.bilateralFilter(bfilter, 11, 17, 17)
        edged = cv2.Canny(bfilter, 50, 150)
        image2 = im.fromarray(edged)
        width, height = image2.size
        bytes_per_line = width
        q_image = QImage(image2.tobytes(), width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.ui.edge.setPixmap(pixmap)
        threshold = cv2.adaptiveThreshold(
            bfilter, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        image3 = im.fromarray(threshold)
        width, height = image3.size
        bytes_per_line = width
        q_image = QImage(image3.tobytes(), width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.ui.threshold.setPixmap(pixmap)

        keypoints = cv2.findContours(threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:]
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2 + 1, y1:y2 + 1]
        image4 = im.fromarray(cropped_image)
        width, height = image4.size
        bytes_per_line = width
        q_image = QImage(image4.tobytes(), width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.ui.np.setPixmap(pixmap)

        text_box=[]
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        for i in range(len(result)):
            text_box.append(result[i][-2])
        self.result_string = ''.join(map(str, text_box))
        self.last_string=self.result_string
    
    def extract_number_plate(self):

        license_plate_text = self.result_string.upper()
        # Apply regex and formatting to the license plate text
        license_plate_text1 = re.sub(r"\s+", "", license_plate_text)
        license_plate_text1 = re.sub(r"[^A-Z0-9]+", "", license_plate_text)
        pattern = r"[A-Za-z]{2}\d{2}[A-Za-z]{0,2}\d{4}"
        matches = re.findall(pattern, license_plate_text1)
        self.result = "".join(matches)
        if len(self.result) == 10:
            self.ui.Extract_det.setPlainText(f"Extracted number plate \n {self.result}")
        else:
            self.ui.Extract_det.setPlainText(f"failed")


    def match_license_plate_details(self):
        # Load the license plate details from the RTO dataset
        if len(self.result)==10:
            rto_dataset_path = "assets\\Database\\RTO.csv"
            df = pd.read_csv(rto_dataset_path)
            
            # Search for the license plate details
            matching_rows = df[df["License number"].str.contains(re.escape(self.result), case=False)]
            
            # Display the matching details in the text box
            if not matching_rows.empty:
                details = matching_rows.to_string(index=False)
                self.ui.matched.setPlainText(f"Matched details \n {details}")
            else:
                self.ui.matched.setPlainText(f"No matches")
        else:
            self.ui.matched.setPlainText(f"Extract Number Plate before matching")
    
    def clear(self):
        self.last_loaded_path=""
        self.ui.selectedFrame.setPixmap(QPixmap(""))
        self.ui.gray_image.setPixmap(QPixmap(""))
        self.ui.threshold.setPixmap(QPixmap(""))
        self.ui.edge.setPixmap(QPixmap(""))
        self.ui.np.setPixmap(QPixmap(""))
        self.ui.Extract_det.setPlainText("")
        self.ui.matched.setPlainText("")
        self.result=""
        self.result_string=""
        # extracted_det

    def setIcon(self):
        appicon=QIcon("assets\\Icons\\license-plate.ico")
        self.setWindowIcon(appicon)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.showMaximized()
    sys.exit(app.exec())
