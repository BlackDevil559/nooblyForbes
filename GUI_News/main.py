import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, QSizePolicy
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRect

class RoundedBox(QWidget):
    def __init__(self, stock_name, summary, parent=None):
        super().__init__(parent)
        self.stock_name = stock_name
        self.summary = summary
        self.initUI()

    def initUI(self):
        # Let layout control size
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(150)  # Set a minimum height
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw white rounded rectangle with shadow
        rect = QRect(10, 10, self.width() - 20, self.height() - 20)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(255, 255, 255)))  # White color
        painter.drawRoundedRect(rect, 15, 15)

        # Set text font and color
        painter.setPen(QPen(QColor(30, 30, 30)))  # Dark font color
        painter.setFont(QFont("Poppins", 18, QFont.Bold))

        # Draw stock name
        painter.drawText(QRect(30, 20, self.width() - 60, 30), Qt.AlignLeft, self.stock_name)

        # Set smaller font for summary
        painter.setFont(QFont("Poppins", 14))
        # Draw summary
        painter.drawText(QRect(30, 60, self.width() - 300, self.height() - 80), Qt.TextWordWrap, self.summary)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.is_youtube_news = False  # Track page toggle
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Market Roundup')
        self.setStyleSheet("background-color: #f3f6fb;")
        self.showMaximized()  

        # Title Label
        title_label = QLabel('MARKET TODAY', self)
        title_label.setFont(QFont('Poppins', 32, QFont.Bold))
        title_label.setStyleSheet("color: #333; margin-bottom: 20px;")

        # Button to switch to YouTube news
        self.youtube_button = QPushButton('YouTube News', self)
        self.youtube_button.setFont(QFont('Poppins', 16))
        self.youtube_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border-radius: 8px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.youtube_button.clicked.connect(self.toggle_news_page)

        # Search Box
        stock_label = QLabel('Stock Name:', self)
        stock_label.setFont(QFont('Poppins', 16))
        stock_label.setStyleSheet("color: #333;")

        # Set default stock name to "Apple"
        self.stock_input = QLineEdit(self)
        self.stock_input.setText("Apple")  # Default stock name
        self.stock_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px;
            }
        """)
        self.stock_input.textChanged.connect(self.on_stock_name_change)

        # Get News Button
        self.get_news_button = QPushButton('Get News', self)
        self.get_news_button.setFont(QFont('Poppins', 16))
        self.get_news_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border-radius: 8px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.get_news_button.clicked.connect(self.fetch_news)
        self.get_news_button.setEnabled(True)  # Enable by default since "Apple" is set

        # Layout for title and buttons
        top_layout = QHBoxLayout()
        top_layout.addWidget(title_label)
        top_layout.addStretch(1)
        top_layout.addWidget(stock_label)
        top_layout.addWidget(self.stock_input)
        top_layout.addWidget(self.get_news_button)
        top_layout.addWidget(self.youtube_button)

        # Scroll area for displaying news
        self.news_layout = QVBoxLayout()
        self.news_layout.setAlignment(Qt.AlignTop)
        self.news_layout.setContentsMargins(20, 20, 20, 20)
        self.news_layout.setSpacing(15)

        scroll_content = QWidget()
        scroll_content.setLayout(self.news_layout)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        scroll_area.setStyleSheet("border: none;")

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

        # Load initial news with the default stock name
        self.load_general_news("Apple")

    def toggle_news_page(self):
        self.is_youtube_news = not self.is_youtube_news
        if self.is_youtube_news:
            self.load_youtube_news()
            self.youtube_button.setText("General News")
        else:
            # Load general news without filtering when switching back
            self.load_general_news("Apple")
            self.youtube_button.setText("YouTube News")

    def load_general_news(self, stock_name=None):
        self.clear_news_layout()

        # Use the stock name in the API call if provided
        try:
            # Construct the query parameter if a stock name is given
            url = "http://localhost:8000/get-news"
            if stock_name:
                url += f"?stock={stock_name}"

            print(f"Fetching from URL: {url}")  # Debugging statement
            response = requests.get(url)
            response.raise_for_status()

            # Debugging: Print the response
            print(f"Response Status: {response.status_code}")
            print(f"Response Data: {response.text}")

            news_data = response.json()  # Assuming the response is in JSON format

            if not news_data:
                print("No news found for this stock.")  # Debugging statement

            for channel, news_list in news_data.items():
                channel_label = QLabel(channel, self)
                channel_label.setFont(QFont('Poppins', 20, QFont.Bold))
                channel_label.setStyleSheet("color: #007bff; margin: 20px 0 10px 10px;")
                self.news_layout.addWidget(channel_label)

                for news_item in news_list:
                    news_box = RoundedBox(stock_name=channel, summary=news_item)
                    self.news_layout.addWidget(news_box)
        except requests.RequestException as e:
            print(f"Error fetching general news: {e}")

    def load_youtube_news(self):
        self.clear_news_layout()

        # API call for YouTube news
        try:
            response = requests.get("http://localhost:8001/get-summary")
            response.raise_for_status()
            youtube_news = response.json()  # Assuming the response is in JSON format

            for news_item in youtube_news:
                news_box = RoundedBox(stock_name=news_item["stock_name"], summary=news_item["summary"])
                self.news_layout.addWidget(news_box)
        except requests.RequestException as e:
            print(f"Error fetching YouTube news: {e}")

    def clear_news_layout(self):
        # Properly clear all items in the news layout
        while self.news_layout.count():
            item = self.news_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def fetch_news(self):
        # Get stock name from the input
        stock_name = self.stock_input.text().strip()
        # Load general news for the given stock name
        if stock_name:
            self.load_general_news(stock_name)

    def on_stock_name_change(self, text):
        # Enable the 'Get News' button only if there's text in the stock name input
        self.get_news_button.setEnabled(bool(text.strip()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
