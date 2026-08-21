import io
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import mss
from PIL import Image

HOST = "0.0.0.0"
PORT = 8080

FPS = 10
JPEG_QUALITY = 70

class ScreenStream:
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]

    def get_frame(self):
        screenshot=self.sct.grab(self.monitor)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        buffer = io.BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=JPEG_QUALITY
        )
        return buffer.getvalue()

streamer = ScreenStream()

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            self.send_html()

        elif self.path == "/video":
            self.send_video()

        else:
            self.send_error(404)

    def send_html0(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Desktop Streamer</title>
        </head>

        <body>

            <h1>Desktop Streamer</h1>

            <p>Рабочий стол:</p>

            <img src="/video">

        </body>
        </html>
        """
        data = html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(data)
        

    def send_html(self):

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">

            <meta name="viewport"
                content="width=device-width, initial-scale=1.0">

            <title>Desktop Streamer</title>

            <style>

                html, body {
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                }

                body {
                    background: #000;
                    overflow: hidden;
                }

                .video {
                    width: 100vw;
                    height: 100vh;

                    object-fit: contain;

                    display: block;
                }

            </style>

        </head>

    <body>

        <img
            class="video"
            src="/video"
        >

    </body>
    </html>
    """

        data = html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(data)

    def send_video(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "multipart/x-mixed-replace; boundary=frame"
        )

        self.send_header("Cache-Control", "no-cache")
        self.send_header("Pragma", "no-cache")

        self.end_headers()

        delay = 1 / FPS

        try:

            while True:

                frame = streamer.get_frame()

                self.wfile.write(b"--frame\r\n")

                self.wfile.write(
                    b"Content-Type: image/jpeg\r\n"
                )

                self.wfile.write(
                    f"Content-Length: {len(frame)}\r\n\r\n".encode()
                )

                self.wfile.write(frame)
                self.wfile.write(b"\r\n")

                self.wfile.flush()

                time.sleep(delay)

        except (BrokenPipeError, ConnectionResetError):
            pass


def main():

    server = ThreadingHTTPServer(
        (HOST, PORT),
        RequestHandler
    )

    print()
    print("Desktop Streamer")
    print("----------------")
    print(f"Server: http://localhost:{PORT}/")
    print(f"Video:  http://localhost:{PORT}/video")
    print()
    print("Для остановки нажмите Ctrl+C")
    print()

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nОстановка...")

    finally:
        server.server_close()
        streamer.sct.close()


if __name__ == "__main__":
    main()