import time
from datetime import datetime
import os
from typing import Optional

from PIL import Image
from mss.linux import MSS as mss
from mss.screenshot import ScreenShot
import typer


def print_size_mb(size: int) -> None:
    # print(f"Total size: {round(size / (1024 * 1024), 3)} MB", end='\r')
    typer.echo(f" Total size: {round(size / (1024 * 1024), 3)} MB\r", nl=False)


def resize_image(mss_image: ScreenShot, size: tuple[int, int] = None) -> Image:
    image = Image.frombytes("RGB", mss_image.size,
                            mss_image.bgra, "raw", "BGRX")
    image = image.resize(size, resample=Image.Resampling.LANCZOS)
    return image


def main(output: Optional[str] = typer.Argument(None),
         fps: float = 1,
         size: str = typer.Option("1280x720", help="Output image size in format: WIDTHxHEIGHT")):

    with mss() as sct:
        sct.compression_level = 7
        # monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        monitor = sct.monitors[1]
        n_screens: int = 0
        total_screens_size: int = 0

        try:
            while "Screen Capturing":
                timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")

                screenshot = sct.grab(monitor)
                width, height = [int(x) for x in size.split("x")]
                image = resize_image(screenshot, size=(width, height))
                if output:
                    os.makedirs(output, exist_ok=True)
                    file_path = f"{output}/screenshot-{timestamp}.png"
                else:
                    file_path = f"screenshots/screenshot-{timestamp}.png"

                image.save(file_path)
                # print(f"Screens captured: {n_screens}", end='\r')
                n_screens += 1

                total_screens_size += os.path.getsize(f'./{file_path}')
                print_size_mb(total_screens_size)
                time.sleep(1/fps)

        except KeyboardInterrupt:
            print("\nEnding screen print.")
            sct.close()
            print("Bye!")


if __name__ == '__main__':
    typer.run(main)
