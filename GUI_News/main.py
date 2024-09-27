import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen, QPixmap
from PyQt5.QtCore import Qt, QRect

class RoundedBox(QWidget):
    def __init__(self, title, summary, parent=None):
        super().__init__(parent)
        self.title = title
        self.summary = summary
        self.initUI()

    def initUI(self):
        self.setFixedSize(700, 250)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw rounded rectangle
        rect = QRect(0, 0, self.width(), self.height())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(50, 50, 50, 180)))
        painter.drawRoundedRect(rect, 30, 30)

        # Set text font and color
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 20, QFont.Bold))

        # Draw title
        painter.drawText(QRect(20, 20, self.width() - 40, 50), Qt.AlignLeft, self.title)

        # Set smaller font for summary
        painter.setFont(QFont("Arial", 16))
        # Draw summary
        painter.drawText(QRect(20, 80, self.width() - 40, 150), Qt.TextWordWrap, self.summary)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Market Roundup')
        self.showFullScreen()

        # Set background image (drawn manually in paintEvent)
        self.background_image = QPixmap('image.png')

        # Title Label
        title_label = QLabel('Market Roundup', self)
        title_label.setFont(QFont('Arial', 40))
        title_label.setStyleSheet("color: white;")

        # Stock Input Box
        stock_label = QLabel('Stock Name', self)
        stock_label.setFont(QFont('Arial', 16))
        stock_label.setStyleSheet("color: white;")
        stock_input = QLineEdit(self)

        # Get News Button
        get_news_button = QPushButton('Get News', self)
        get_news_button.setFont(QFont('Arial', 16))
        get_news_button.setStyleSheet("background-color: #333; color: white; padding: 10px; border-radius: 10px;")
        
        # Rounded Boxes (simulating the news content)
        box1 = RoundedBox("Is It Too Late to Buy Apple Stock?", "Apple has been on a roll lately. Will the good times last?")
        box2 = RoundedBox("Forget Apple: This Stock Has Made Far More Millionaires", "Celsius minted more millionaires than Apple over the past decade.")
        box3 = RoundedBox("These 5 Artificial Intelligence (AI) Stocks Make Up 27.1% of the Entire S&P 500 Index", 
                          "The S&P 500 is a diversified index, but a mere handful of technology stocks currently have a big influence over its performance.")

        # Layout management
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        
        form_layout = QHBoxLayout()
        form_layout.addWidget(stock_label)
        form_layout.addWidget(stock_input)
        form_layout.addWidget(get_news_button)

        news_layout = QVBoxLayout()
        news_layout.addWidget(box1)
        news_layout.addWidget(box2)
        news_layout.addWidget(box3)

        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(news_layout)

        self.setLayout(main_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
