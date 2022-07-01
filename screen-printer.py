import time
from datetime import datetime

from PIL import Image

from mss.linux import MSS as mss
from mss.screenshot import ScreenShot


def compress_image(mss_image: ScreenShot, size: tuple[int, int] = None) -> Image:
    image = Image.frombytes("RGB", mss_image.size,
                            mss_image.bgra, "raw", "BGRX")
    if size:
        image = image.resize(size, resample=Image.Resampling.LANCZOS)
    # image = image.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
    return image


def capture_screen(fps: float = 1) -> None:
    with mss() as sct:
        sct.compression_level = 7
        # monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        monitor = sct.monitors[1]
        n_screens = 0
        try:
            while "Screen Capturing":
                timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")

                screenshot = sct.grab(monitor)

                image = compress_image(screenshot, size=(1280, 720))
                # image = compress_image(screenshot)
                image.save(f"screenshots/screenshot-{timestamp}.png")
                print(f"Screens captured: {n_screens}", end='\r')
                n_screens += 1
                time.sleep(1/fps)
                
        except KeyboardInterrupt:
            print("\nEnding screen print.")
            sct.close()
            print("Bye!")

if __name__ == "__main__":
    capture_screen()