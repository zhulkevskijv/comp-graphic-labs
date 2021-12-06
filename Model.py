import cv2
from math import cos, sin
import numpy as np


class Model:
    def __init__(self, filename):

        self.__vectors = []
        self.__triangles = []
        file = open(filename, "r")
        content = file.readlines()
        max0 = -1000000000
        max1 = -1000000000
        max2 = -1000000000
        min0 = 1000000000
        min1 = 1000000000
        min2 = 1000000000

        for line in content:
            if line[0] == 'v' and line[1] == ' ':
                values = line.split(' ')
                max0 = max(max0, float(values[1]))
                max1 = max(max1, float(values[2]))
                max2 = max(max2, float(values[3]))
                min0 = min(min0, float(values[1]))
                min1 = min(min1, float(values[2]))
                min2 = min(min2, float(values[3]))

                self.__vectors.append([float(values[1]), float(values[2]), float(values[3])])
            elif line[0] == 'f' and line[1] == ' ':
                f = line.split(' ')
                v1 = f[1].split('/')[0]
                v2 = f[2].split('/')[0]
                v3 = f[3].split('/')[0]
                self.__triangles.append([int(v1) - 1, int(v2) - 1, int(v3) - 1])

        scale = max(max0 - min0, max1 - min1, max2 - min2) / 2
        offset = np.array([(max0 + min0) / 2, (max1 + min1) / 2, (max2 + min2) / 2])

        for i in range(len(self.__vectors)):
            self.__vectors[i] = (np.array(self.__vectors[i]) - offset) / scale

    def vertexes_length(self):
        return len(self.__vectors)

    def triangles_length(self):
        return len(self.__triangles)

    def triangle(self, idx):
        return self.__triangles[idx]

    def vertex(self, idx):
        return self.__vectors[idx]

    def triangles(self):
        return self.__triangles

    def vertexes(self):
        return self.__vectors

    def sort(self):
        self.__triangles.sort(key=lambda i: self.vertex(i[0])[2], reverse=False)
        pass

    def rotate_x(self, angle):
        rx = np.array([[1, 0, 0], [0, cos(angle), -sin(angle)], [0, sin(angle), cos(angle)]])
        for id, face in enumerate(self.__vectors):
            y = np.array(face)
            self.__vectors[id] = rx @ y

    def rotate_y(self, angle):
        rx = np.array([[cos(angle), 0, sin(angle)], [0, 1, 0], [-sin(angle), 0, cos(angle)]])
        for id, face in enumerate(self.__vectors):
            y = np.array(face)
            self.__vectors[id] = rx @ y

    def rotate_z(self, angle):
        rx = np.array([[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]])
        for id, face in enumerate(self.__vectors):
            y = np.array(face)
            self.__vectors[id] = rx @ y
