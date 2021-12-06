#
# Developed by Zhulkevskyi Vladyslav
# 31.01.2021
import cv2 as cv
import math
import numpy as np

def draw_line(x0, y0, x1, y1, image, color):
    steep = False
    if abs(x0-x1) < abs(y0-y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    derror2 = abs(dy)*2
    error2 = 0
    y = y0
    for x in range(x0, x1+1):
        if steep:
            image[y, x] = color
        else:
            image[x, y] = color
        error2 += derror2
        if error2 > dx:
            y += 1 if y1 > y0 else -1
            error2 -= dx*2

    return image


def draw_circle(x1, y1, radius, image, color):
    x = 0
    y = radius
    delta = 1 - 2*radius
    error = 0
    while y >= 0:
        image[int(x1 + x), int(y1 + y)] = color
        image[int(x1 - x), int(y1 + y)] = color
        image[int(x1 + x), int(y1 - y)] = color
        image[int(x1 - x), int(y1 - y)] = color
        error = 2 * (delta + y) - 1
        if delta < 0 and error <= 0:
            x += 1
            delta += 2 * x + 1
            continue
        error = 2 * (delta - x) - 1
        if delta > 0 and error > 0:
            y -= 1
            delta += 1 - 2 * y
            continue
        x += 1
        delta += 2 * (x - y)
        y -= 1

    return image


def read_model(filename):
    vectors = []
    triangles = []
    file = open(filename, "r")
    content = file.readlines()
    max0 = 1
    max1 = 1
    max2 = 1
    min0 = -1
    min1 = -1
    min2 = -1

    for line in content:
        if line[0] == 'v' and line[1] == ' ':
            values = line.split(' ')
            if float(values[1]) > max0:
                max0 = float(values[1])
            if float(values[2]) > max1:
                max1 = float(values[2])
            if float(values[1]) < min0:
                min0 = float(values[1])
            if float(values[2]) < min1:
                min1 = float(values[2])
            if float(values[3]) > max2:
                max2 = float(values[3])
            if float(values[3]) < min2:
                min2 = float(values[3])
            vectors.append([float(values[1]), float(values[2]), float(values[3])])
        elif line[0] == 'f' and line[1] == ' ':
            f = line.split(' ')
            v1 = f[1].split('/')[0]
            v2 = f[2].split('/')[0]
            v3 = f[3].split('/')[0]
            triangles.append([int(v1)-1, int(v2)-1, int(v3)-1])
    avg0 = (max0 + min0) / 2
    avg1 = (max1 + min1) / 2
    avg2 = (max2 + min2) / 2
    scale0 = max0 - min0
    scale1 = max1 - min1
    scale2 = max2 - min2

    max_scale = max(scale0, scale1, scale2)

    avg_v = np.array([avg0, avg1, avg2])

    for i in range(len(vectors)):
        vectors[i] = np.array(vectors[i]) - avg_v
        vectors[i] = [vectors[i][0]/max_scale, vectors[i][1]/max_scale, vectors[i][2]/max_scale]
    return vectors, triangles


def print_model(vectors, triangles, image):
    img2 = image.copy()
    img1 = image.copy()
    height, width, trash = image.shape
    color1 = (255, 255, 255)
    color2 = (255, 255, 0)

    for i in range(len(triangles)):
        f = triangles[i]

        for j in range(3):
            v0 = vectors[f[j]]
            v1 = vectors[f[(j+1) % 3]]
            length0 = math.pow(v0[0], 2) + math.pow(v0[1], 2)
            length1 = math.pow(v1[0], 2) + math.pow(v1[1], 2)


            # if v0[0] > 1 or v0[0] < -1 or v0[1] > 1 or v0[1] < -1:
            #     v0[0] = v0[0] / length0
            #     v0[1] = v0[1] / length0 * 2
            #
            # if v1[0] > 1 or v1[0] < -1 or v1[1] > 1 or v1[1] < -1:
            #     v1[0] = v1[0] / length1 * 2
            #     v1[1] = v1[1] / length1 * 2

            x0 = int((v0[0] + 1) * width / 2) - 1
            y0 = int((v0[1] + 1) * height / 2) - 1
            x1 = int((v1[0] + 1) * width / 2) - 1
            y1 = int((v1[1] + 1) * height / 2) - 1
            img1 = draw_line(y0, x0, y1, x1, img1, color1)
            img2 = cv.line(img2, (x0, y0), (x1, y1), color2, 1)

    cv.imshow("My obj", img1)
    cv.imshow("CV obj", img2)


def my_algos(image):
    img = image.copy()
    img = draw_line(0, 0, img.shape[0]-1, img.shape[1]-1, img, (255, 255, 255))
    img = draw_circle(img.shape[0]/2, img.shape[1]/2, 100, img, (255, 255, 255))
    cv.imshow("My image", img)


def cv_algos(image):
    img = image.copy()
    img = cv.line(img, (0, 0), (img.shape[1], img.shape[0]), (255, 0, 255), 1)
    img = cv.circle(img, (int(img.shape[1]/2), int(img.shape[0]/2)), 100, (255, 0, 255), 1)
    cv.imshow("CV image", img)


if __name__ == '__main__':
    img111 = cv.imread("images/black-vertical.png", cv.IMREAD_COLOR)
    img333 = np.zeros((700, 600, 3), dtype="uint8")
    img222 = cv.imread("images/black.jpg", cv.IMREAD_COLOR)
    my_algos(img222)
    cv_algos(img222)
    vects, face = read_model('objects/african_head.obj')
    print_model(vects, face, img333)
    cv.waitKey(0)


