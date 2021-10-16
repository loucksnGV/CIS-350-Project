from pymongo import MongoClient
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QPainter
import sys, math, urllib.request

client = MongoClient('mongodb+srv://client:default@cluster0.psr24.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.BookDB


class DefaultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initDefault()
        
    def initDefault(self):
        self.setWindowTitle("Book Recommendation Service")
        
        grid = QGridLayout(self)

        for i, v in enumerate(db.recs.find({})):
            button = RecTitle(v)
            grid.addWidget(button, math.floor(i / 10), i % 10)
            
        self.setLayout(grid)
        self.show()



class RecTitle(QAbstractButton):
    def __init__(self, rec_data, parent=None):
        super(RecTitle, self).__init__(parent)
        self.biblio_data = db.biblio.find_one({'_id': rec_data['book_id']})
        
        #image loading hangs the UI and really needs to be made async at some point
        url = self.biblio_data['image_url']
        img_data = urllib.request.urlopen(url).read()
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(img_data)
        
        self.setMinimumSize(113, 170)
        self.setMaximumSize(113, 170)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    #def sizeHint(self):
    #    return self.pixmap.size()
    
    def enterEvent(self, event):
        print(self.biblio_data['title'])


def main():
    app = QApplication([])
    window = DefaultWindow()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
