import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt


class MarketRoundup(QWidget):
    def __init__(self):
        super().__init__()

        # Setting window properties
        self.setWindowTitle("Market Roundup")
        self.setFixedSize(800, 400)

        # Load the background image
        self.setAutoFillBackground(True)
        palette = self.palette()
        background_image = QPixmap("image.png")  # Background image path
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.setPalette(palette)

        # Main layout
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Market Roundup")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignLeft)

        # Horizontal layout for Stock Name
        h_layout_stock = QHBoxLayout()

        stock_label = QLabel("Stock Name")
        stock_label.setFont(QFont("Arial", 16))
        stock_label.setStyleSheet("color: white;")
        stock_label.setAlignment(Qt.AlignLeft)

        stock_input = QLineEdit()
        stock_input.setText("Apple")
        stock_input.setFont(QFont("Arial", 16))
        stock_input.setStyleSheet("background-color: #1f1f1f; color: white; border: 1px solid white;")
        stock_input.setFixedWidth(200)

        # Adding stock label and input to the horizontal layout
        h_layout_stock.addWidget(stock_label)
        h_layout_stock.addWidget(stock_input)

        # Get News Button
        get_news_button = QPushButton("Get News")
        get_news_button.setFont(QFont("Arial", 14))
        get_news_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: 1px solid white;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        get_news_button.setFixedWidth(150)

        # Adding widgets to the main layout
        layout.addWidget(title_label)
        layout.addLayout(h_layout_stock)
        layout.addWidget(get_news_button)

        # Add space around the elements
        layout.addStretch()

        # Set the layout to the widget
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarketRoundup()
    window.show()
    sys.exit(app.exec_())
