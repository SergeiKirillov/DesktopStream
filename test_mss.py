from mss import mss
from PIL import Image


with mss() as sct:
    monitor = sct.monitors[1]
    screenshot = sct.grab(monitor)

    image = Image.frombytes(
        "RGB",
        screenshot.size,
        screenshot.rgb
    )

    image.save("test.png")

print("OK")