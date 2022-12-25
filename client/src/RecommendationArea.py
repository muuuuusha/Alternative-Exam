from PyQt5.QtWidgets import QScrollArea, QFrame, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

import src.RecommendationWidget as RecommendationWidget

class RecommendationArea(QScrollArea):
    def __init__(self, articles: list):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.widgets = []
        for (id, title) in articles:
            self.addWidget(id, title)

        self.setLayout(self.layout)
        self.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        self.setWidgetResizable(True)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        
        self.setFrameStyle(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
    def clear(self):
        for widget in self.widgets:
            self.layout.removeWidget(widget)
            widget.deleteLater()
        self.widgets.clear()
        
    def addWidget(self, articleID, articleTitle):
        recommendation = RecommendationWidget.RecommendationWidget(articleID, articleTitle)
        self.layout.addWidget(recommendation)
        self.widgets.append(recommendation)
        
    def removeWidget(self, articleID):
        for widget in self.widgets:
            if widget.articleID == articleID:
                self.layout.removeWidget(widget)
                widget.deleteLater()
                self.widgets.remove(widget)
                break
        