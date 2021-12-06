import cv2 as cv
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

if __name__ == '__main__':
    # img = cv.imread("original.tif", cv.IMREAD_COLOR)
    # img = cv.imread("IMS.png", cv.IMREAD_COLOR)
    img = cv.imread("images/sunmoon.webp", cv.IMREAD_COLOR)
    cv.imshow("Original image", img)
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    im = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    cv.imshow("YCbCr", im)
    # Y = (0.299 * R) + (0.587 * G) + (0.114 * B)
    # Cb = (-0.169 * R) - (0.331 * G) + (0.500 * B)
    # Cr = (0.500 * R) - (0.418 * G) - (0.082 * B)

    Y = (0.299 * R) + (0.587 * G) + (0.114 * B)
    Cb = 256 - ((-0.169 * R) - (0.331 * G) + (0.500 * B) + 128)
    Cr = (0.500 * R) - (0.418 * G) - (0.082 * B) + 128

    dst = np.zeros((306, 306, 3), dtype=img.dtype)
    print(Cb)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            dst[int(25+Cb.item((i, j))), int(25+Cr.item((i, j)))] = np.array([R.item((i, j)), G.item((i, j)), B.item((i, j))])

    color = (30, 165, 255)
    dst = cv.circle(dst, (153, 153), 153, color, 1)
    dst = cv.line(dst, (153, 0), (153, 306), color, 1)
    dst = cv.line(dst, (0, 153), (306, 153), color, 1)

    cv.imshow("Vectorscope", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()