"""Standalone desktop window — web UI inside the app, no external browser."""

import os, sys, threading
from . import config

HAS_PYWEBVIEW = False
try:
    import webview
    HAS_PYWEBVIEW = True
except ImportError:
    pass

HAS_TRAY = False
try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    pass

_window = None

def _make_icon(size=64):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r = size // 2 - 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(92, 214, 255, 255), width=2)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(92, 214, 255, 255))
    return img

def _on_closing():
    if HAS_TRAY and _window:
        _window.hide()
        return True
    return False

def _tray_open(icon, item):
    if _window:
        _window.show()

def _tray_quit(icon, item):
    icon.stop()
    os._exit(0)

def _run_tray():
    menu = (
        pystray.MenuItem("Open EbayDekho", _tray_open, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", _tray_quit),
    )
    pystray.Icon("ebaydekho", _make_icon(), "EbayDekho", menu).run()

def start(port):
    global _window
    if not HAS_PYWEBVIEW:
        import webbrowser
        webbrowser.open(f"http://127.0.0.1:{port}")
        return
    try:
        _window = webview.create_window(
            "EbayDekho", f"http://127.0.0.1:{port}",
            width=1200, height=800, min_size=(900, 600),
            text_select=True, on_close=_on_closing)
        if HAS_TRAY:
            threading.Thread(target=_run_tray, daemon=True).start()
        webview.start(gui="edgechromium" if sys.platform == "win32" else None)
    except Exception as e:
        print(f"[desktop] window failed: {e}", flush=True)
        import webbrowser
        webbrowser.open(f"http://127.0.0.1:{port}")
