import sys
from datetime import datetime as dt

# import numpy as np
# from cv2 import IMREAD_GRAYSCALE, Canny, imread, imwrite
# from numpy import argwhere as arg
# from PIL import Image as im
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from ui_secondmainwindow import Ui_SecondMainWindow


class SecondMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SecondMainWindow()
        self.ui.setupUi(self)
        
        #self.ui.pushButton_2.clicked.connect(process_image(file_path))
    
    # def display(self,path):
    #     pixmap = QPixmap(path)
    #     print(path)
    #     self.ui.SecondFSO.setPixmap(pixmap)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SecondMainWindow()
    widget.show()
    sys.exit(app.exec())