import sys
import requests
import threading

from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction

CURRENT_VERSION = "1.0"


# ---------- OTA ----------
def check_update():
    try:
        url = "https://raw.githubusercontent.com/USER/REPO/main/version.txt"
        latest = requests.get(url).text.strip()

        if latest != CURRENT_VERSION:
            print("Van új verzió!")
            download_update()

    except Exception as e:
        print("Update hiba:", e)


def download_update():
    url = "https://github.com/USER/REPO/releases/latest/download/browser.exe"

    r = requests.get(url, stream=True)
    with open("update.exe", "wb") as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

    print("Frissítés letöltve")


# ---------- BROWSER ----------
class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Browser")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # toolbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction("←", self)
        back_btn.triggered.connect(lambda: self.current().back())
        navbar.addAction(back_btn)

        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(lambda: self.current().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(lambda: self.current().reload())
        navbar.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.go_to_url)
        navbar.addWidget(self.url_bar)

        new_tab = QAction("+", self)
        new_tab.triggered.connect(self.add_tab)
        navbar.addAction(new_tab)

        self.add_tab()

    def add_tab(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl("https://www.google.com"))

        i = self.tabs.addTab(browser, "Új fül")
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()))

    def close_tab(self, i):
        self.tabs.removeTab(i)

    def current(self):
        return self.tabs.currentWidget()

    def go_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.current().setUrl(QUrl(url))


# ---------- RUN ----------
app = QApplication(sys.argv)

check_update()

window = Browser()
window.show()

sys.exit(app.exec())