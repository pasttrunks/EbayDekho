"""Standalone desktop window — Chromium inside the app (Qt5 WebEngine), no external browser."""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QPainter, QColor, QPixmap


def _make_pixmap(size=64):
    pix = QPixmap(size, size)
    pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(QColor(92, 214, 255))
    cx, cy = size // 2, size // 2
    r = size // 2 - 2
    p.drawEllipse(cx - r, cy - r, r * 2, r * 2)
    p.drawEllipse(cx - 4, cy - 4, 8, 8)
    p.end()
    return pix


def start(port):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication.instance() or QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    win = QMainWindow()
    win.setWindowTitle("EbayDekho")
    win.resize(1200, 800)
    win.setMinimumSize(900, 600)
    win.setWindowIcon(QIcon(_make_pixmap()))

    browser = QWebEngineView()
    browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    dpr = app.primaryScreen().devicePixelRatio()
    browser.setZoomFactor(dpr)
    browser.setUrl(QUrl(f"http://127.0.0.1:{port}"))
    win.setCentralWidget(browser)

    tray = QSystemTrayIcon(QIcon(_make_pixmap()), app)
    tray.setToolTip("EbayDekho")
    menu = QMenu()
    show_a = menu.addAction("Open EbayDekho")
    show_a.triggered.connect(win.show)
    menu.addSeparator()
    quit_a = menu.addAction("Quit")
    quit_a.triggered.connect(app.quit)
    tray.setContextMenu(menu)
    tray.activated.connect(lambda r: win.show() if r == QSystemTrayIcon.DoubleClick else None)

    def _on_close(event):
        event.ignore()
        win.hide()

    win.closeEvent = _on_close
    tray.show()
    win.show()
    sys.exit(app.exec_())
