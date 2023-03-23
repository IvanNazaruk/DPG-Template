import os
import sys

from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
    # ../src/settings -> ../src
    application_path, _ = os.path.split(application_path)
