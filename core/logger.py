import os
import logging
from datetime import datetime


def newLogger(filename: str, format='%(name)s - %(levelname)s - %(message)s') -> logging:
    if not os.path.exists("log"):
        os.mkdir("log")
    logging.basicConfig(
        filename=os.path.join("log", filename + "_" + datetime.now().strftime("%Y.%m.%d") + ".log"),
        filemode='w+', format=format)
    return logging


logger = newLogger("log")
