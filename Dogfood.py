from pymongo import MongoClient
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QPainter
import sys, math, urllib.request
from PyQt6.uic.Compiler.qtproxies import QtWidgets

client = MongoClient('mongodb+srv://client:default@cluster0.psr24.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.BookDB


class DefaultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initDefault()
        
    def initDefault(self):
        self.setWindowTitle("Book Recommendation Service")
        self.setFixedSize(1200, 800)
        
        main_view = TitleGrid()
        recs_view = QWidget()
        info_view = QWidget()
        
        main_view.setFixedSize(865, 550)
        recs_view.setFixedSize(865, 250)
        info_view.setFixedSize(335, 800)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(main_view)
        layout.addWidget(info_view)
        layout.addWidget(recs_view)
        
        self.show()
        
        
class TitleGrid(QScrollArea):
    def __init__(self):
        super().__init__()
        
        contents = QWidget()
        grid = QGridLayout(self)
        for i, v in enumerate(db.recs.find({})):
            button = RecTitle(v)
            grid.addWidget(button, math.floor(i / 7), i % 7)
            
        contents.setLayout(grid)
        self.setWidget(contents)
        self.setWidgetResizable(False)


class RecTitle(QAbstractButton):
    def __init__(self, rec_data, parent=None):
        super(RecTitle, self).__init__(parent)
        self.biblio_data = db.biblio.find_one({'_id': rec_data['book_id']})
        self.setFixedSize(113, 170) #these things aren't scaling correctly atm. look into sizepolicy?
        
        #image loading hangs the UI and really needs to be made async at some point
        url = self.biblio_data['image_url']
        img_data = urllib.request.urlopen(url).read()
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(img_data)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)
    
    def enterEvent(self, event):
        print(self.biblio_data['title'])


def main():
    app = QApplication([])
    window = DefaultWindow()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
