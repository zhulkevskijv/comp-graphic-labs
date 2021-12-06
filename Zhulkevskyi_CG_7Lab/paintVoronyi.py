import cv2 as cv
import numpy as np
import random
from Model import Model


def get_rand_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_some_color(triangle):
    return ((triangle[0]) % 255, (triangle[1]) % 255, (triangle[2]) % 255)


def triangle(x0, y0, x1, y1, x2, y2, img, color):
    if y0 > y2:
        x0, x2 = x2, x0
        y0, y2 = y2, y0
    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    if y1 > y2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    if y2 != y0:
        dx02 = (x2 - x0) / (y2 - y0)
    else:
        dx02 = 0

    if y1 != y0:
        dx01 = (x1 - x0) / (y1 - y0)
    else:
        dx01 = 0

    if y2 != y1:
        dx12 = (x2 - x1) / (y2 - y1)
    else:
        dx12 = 0

    wx0 = x0
    wx1 = wx0

    _dx02 = dx02

    if dx02 > dx01:
        dx01, dx02 = dx02, dx01

    if _dx02 < dx12:
        _dx02, dx12 = dx12, _dx02

    for i in range(y0, y1):
        for j in range(int(wx0), int(wx1) + 1):
            img[i - 1, j] = color
        wx0 += dx02
        wx1 += dx01

    if y0 == y1:
        wx0 = x0
        wx1 = x1

    for y in range(y1, y2 + 1):
        for x in range(int(wx0), int(wx1) + 1):
            img[y - 1, x] = color

        wx0 += _dx02
        wx1 += dx12

    return img


if __name__ == '__main__':
    width = 1000
    height = 1000
    im1 = np.zeros(( width + 1, height + 1, 3), dtype="uint8")
    im2 = np.zeros((width + 1, height + 1, 3), dtype="uint8")

    model = Model('../objects/african_head.obj')

    for i in range(model.triangles_length()):
        face = model.triangle(i)
        triangl = [0, 0, 0]
        for j in range(3):
            vert = model.vertex(face[j])
            triangl[j] = width - int((vert[0] + 1) * width / 2), int(abs(height - (vert[1] + 1) * height / 2))
        color = get_rand_color()
        im1 = triangle(triangl[0][0], triangl[0][1], triangl[1][0],
                       triangl[1][1], triangl[2][0], triangl[2][1],
                       im1, color)
        cv.drawContours(im2, [np.array([triangl[0], triangl[1], triangl[2]])], 0, color, -1)

    cv.imshow('My triangle', im1)
    cv.imshow('Default triangle', im2)
    cv.waitKey(0)
    cv.destroyAllWindows()

def draw_image(model, nameImage, wait_key=1):
    width = 1200
    height = 1200
    im2 = np.zeros((width + 1, height + 1, 3), dtype="uint8")
    for i in range(model.triangles_length()):
        face = model.triangle(i)
        triangl = [0, 0, 0]
        for j in range(3):
            vert = model.vertex(face[j])
            triangl[j] = width - int((vert[0] + 1) * width / 2), int(abs(height - (vert[1] + 1) * height / 2))
        color = get_rand_color()
        cv.drawContours(im2, [np.array([triangl[0], triangl[1], triangl[2]])], 0, color, -1)

    cv.imshow(nameImage, im2)
    cv.waitKey(wait_key)
