from PIL import Image
import pytesseract
import argparse
import cv2
import os
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to image of idcard")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image, 1024, 665)
# image = image[100:340,190:560]
cv2.imshow('image0', image)
cv2.waitKey(0)
h0, w0 = image.shape[:2]
h = int(h0/4) + 5

strs = ["" for x in range(4)]

for i in range(4):
    im = image[h*i:h*(i+1), :]
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1]
    gray = cv2.medianBlur(gray, 3)
    cv2.imshow('gray', gray)
    cv2.waitKey(0)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename))
    print("Text Extracted - {}: {}".format(i, text))

    os.remove(filename)
    strs[i] = text