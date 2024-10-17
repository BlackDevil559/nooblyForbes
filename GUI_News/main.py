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
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw white rounded rectangle
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
        painter.drawText(QRect(30, 60, self.width() - 60, self.height() - 80), Qt.TextWordWrap, self.summary)


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

    def toggle_news_page(self):
        self.is_youtube_news = not self.is_youtube_news
        if self.is_youtube_news:
            self.load_youtube_news()
            self.youtube_button.setText("General News")
        else:
            self.clear_news_layout()

    def load_youtube_news(self):
        self.clear_news_layout()

        # API call for YouTube news
        try:
            response = requests.get("http://localhost:8001/get-summary")
            response.raise_for_status()
            youtube_news = response.json()
            print("YouTube News Response:", youtube_news)

            # Display the news content
            for news_item in youtube_news:
                news_box = RoundedBox(stock_name=news_item["stock_name"], summary=news_item["summary"])
                self.news_layout.addWidget(news_box)
        except requests.RequestException as e:
            print(f"Error fetching YouTube news: {e}")

    def fetch_news(self):
        stock_name = self.stock_input.text()
        if not stock_name:
            return

        # Fetch stock news from your API
        url = f"http://127.0.0.1:8000/get-news?stock={stock_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            news_data = response.json()
            # print(news_data)
            self.clear_news_layout()

            # Iterate through all sources in the received data
            all_news = {
                "AlphaVantage": news_data.get("AlphaVantage", {}),
                "CNBC": news_data.get("CNBC", {}),
                "Marketaux": news_data.get("Marketaux", {}),
                "NewsAPI": news_data.get("NewsAPI", {}),
                "Reuters": news_data.get("Reuters", {})
            }

            # Loop through each source and display news items
            for source, data in all_news.items():
                news_list = data.get("news", [])
                avg_sentiment = data.get("average_sentiment", None)
                print("Hello 1",news_list)
                if news_list:  # Only display sources with available news
                    # Add source label with sentiment score
                    source_label = QLabel(f"{source} (Sentiment: {avg_sentiment:.2f})" if avg_sentiment is not None else source, self)
                    source_label.setFont(QFont('Poppins', 20, QFont.Bold))
                    source_label.setStyleSheet("color: #007bff; margin: 20px 0 10px 10px;")
                    self.news_layout.addWidget(source_label)

                    # Combine the top 5 news items into a single summary
                    combined_summary = "\n\n".join(news_list[:5])
                    print(combined_summary)
                    news_box = RoundedBox(stock_name="", summary=combined_summary)
                    self.news_layout.addWidget(news_box)

        except requests.RequestException as e:
            print(f"Error fetching news: {e}")

    def clear_news_layout(self):
        # Properly clear all items in the news layout
        while self.news_layout.count():
            child = self.news_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
