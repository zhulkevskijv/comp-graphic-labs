import numpy as np
import cv2 as cv


pmin, pmax, qmin, qmax = -2.5, 1.5, -2, 2

width, height = 400, 400

max_iterations = 300
max_zoom = 300000
infinity_border = 10

def mandelbrot(pmin, pmax, qmin, qmax,
               max_iterations=122, infinity_border=10):
    image = np.zeros((width, height, 3), dtype=np.uint8)
    p, q = np.mgrid[pmin:pmax:(width*1j), qmin:qmax:(height*1j)]
    c = p + 1j*q
    z = np.zeros_like(c)
    for k in range(max_iterations):
        z = z**2 + c
        mask = (np.abs(z) > infinity_border) & (np.add.reduce(image, axis=2) == 0)
        image[mask] = (k*2, 160, 180)
        z[mask] = np.nan
    return image


p_center, q_center = -0.793191078177363, 0.16093721735804

def getFrames():
    frames = []
    for i in range(1, max_iterations):
        print(i)
        zoom = (i / max_iterations * 2) ** 3 * max_zoom + 1
        scalefactor = i / zoom
        pmin_ = (pmin - p_center) * scalefactor + p_center
        qmin_ = (qmin - q_center) * scalefactor + q_center
        pmax_ = (pmax - p_center) * scalefactor + p_center
        qmax_ = (qmax - q_center) * scalefactor + q_center
        frame = mandelbrot(pmin_, pmax_, qmin_, qmax_)
        frames.append(cv.cvtColor(frame, cv.COLOR_HSV2BGR))
    return frames


if __name__ == '__main__':
    frames = getFrames()
    cv.imshow('fractal', frames[0])
    cv.waitKey(0)
    while True:
        for f in frames:
            cv.imshow('fractal', f)
            cv.waitKey(2)
        for f in reversed(frames):
            cv.imshow('fractal', f)
            cv.waitKey(2)