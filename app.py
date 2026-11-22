"""NXT27 · Neural eXecution Terminal — ventana de escritorio.

Abre index.html (la demo visual, sin funcionalidad real) en una ventana
nativa usando el motor web del sistema (Edge WebView2 en Windows).
"""
import os
import sys
import webview


def resource(path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, path)


def main():
    webview.create_window(
        "NXT27 · Neural eXecution Terminal",
        resource("index.html"),
        width=1120,
        height=740,
        min_size=(760, 520),
        background_color="#000000",
    )
    webview.start()


if __name__ == "__main__":
    main()
