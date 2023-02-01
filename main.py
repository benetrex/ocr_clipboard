"""Module to take a screenshot between two clicks
and perform OCR-Analysis on the content of the screenshot,
then saving the result to clipboard"""
import logging

import pyautogui
import pyperclip
import pytesseract
from PIL import ImageGrab
from pynput.mouse import Listener

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)


def get_points() -> list:
    """Returns a list of points"""
    ret_points = []

    def on_click(x_coordinate, y_coordinate, button, pressed):
        if pressed:
            ret_points.append(pyautogui.Point(x=x_coordinate, y=y_coordinate))
            logging.info("Mouse clicked at (%s, %s) with %s", x_coordinate, y_coordinate, button)
            if len(ret_points) >= 2:
                return False

    with Listener(on_click=on_click) as listener:
        logger.info("Ready")
        listener.join()

    return ret_points


def screen_grab(point1: pyautogui.Point, point2: pyautogui.Point):
    """Given a rectangle, return a PIL Image of that part of the screen.
    Handles a Linux installation with and older Pillow by falling-back
    to using XLib"""
    pos_x_0, pos_y_0 = point1.x, point1.y
    pos_x_1, pos_y_1 = point2.x, point2.y
    if pos_x_0 > pos_x_1:
        pos_x_0, pos_x_1 = pos_x_1, pos_x_0
    if pos_y_0 > pos_y_1:
        pos_y_0, pos_y_1 = pos_y_1, pos_y_0

    return ImageGrab.grab(
        bbox=[pos_x_0, pos_y_0, pos_x_1, pos_y_1],
        include_layered_windows=False,
        all_screens=True,
    )


if __name__ == "__main__":
    points = get_points()
    image = screen_grab(points[0], points[1])
    image.show()
    text = pytesseract.image_to_string(image).strip()
    pyperclip.copy(text)
    logger.info("Text in Clipboard:\n%s", text)
