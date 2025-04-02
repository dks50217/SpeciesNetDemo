import os
from control.ctr_image import Ctr_Image

if __name__ == "__main__":

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ctr_image = Ctr_Image()
    ctr_image.crop_images()