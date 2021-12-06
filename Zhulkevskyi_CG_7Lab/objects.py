import numpy as np
import math


def make_triangles(circles, segments):
    triangles = []
    for i in range(circles - 1):
        for j in range(segments - 1):

            a = [i * segments + j,
                 (i + 1) * segments + j,
                 i * segments + (j + 1)]

            b = [(i + 1) * segments + j + 1,
                 i * segments + (j + 1),
                 (i + 1) * segments + j]

            triangles.append(a)
            triangles.append(b)

    i = circles - 1
    for j in range(segments - 1):
        a = [i * segments + j, j, i * segments + j + 1]
        b = [j + 1, i * segments + j + 1, j]
        triangles.append(a)
        triangles.append(b)
    return triangles


class Torus:
    def __init__(self, R, r):
        self.__vectors = []

        parts = 0
        segments = 0
        step = math.pi / 10
        t = 0
        max0 = -1000000000
        max1 = -1000000000
        max2 = -1000000000
        min0 = 1000000000
        min1 = 1000000000
        min2 = 1000000000

        while t < 2 * math.pi:
            f = -1.0 * math.pi
            segments = 0
            while f < math.pi:
                x = (R + r * math.cos(f)) * math.cos(t)
                y = (R + r * math.cos(f)) * math.sin(t)
                z = r * math.sin(f)

                max0 = max(max0, float(x))
                max1 = max(max1, float(y))
                max2 = max(max2, float(z))
                min0 = min(min0, float(x))
                min1 = min(min1, float(y))
                min2 = min(min2, float(z))

                self.__vectors.append([x, y, z])
                f += step
                segments += 1
            t += step
            parts += 1

        self.__triangles = make_triangles(parts, segments)

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

    def sort(self):
        self.__triangles.sort(key=lambda i: self.vertex(i[0])[2], reverse=False)
        pass

    def rotate_x(self, angle):
        rx = np.array([[1, 0, 0], [0, math.cos(angle), -math.sin(angle)], [0, math.sin(angle), math.cos(angle)]])
        for id, face in enumerate(self.__vectors):
            y = np.array(face)
            self.__vectors[id] = rx @ y

    def rotate_y(self, angle):
        rx = np.array([[math.cos(angle), 0, math.sin(angle)], [0, 1, 0], [-math.sin(angle), 0, math.cos(angle)]])
        for id, face in enumerate(self.__vectors):
            y = np.array(face)
            self.__vectors[id] = rx @ y

    def rotate_z(self, angle):
        rx = np.array([[math.cos(angle), -math.sin(angle), 0], [math.sin(angle), math.cos(angle), 0], [0, 0, 1]])
        for id, face in enumerate(self.__vectors):
            y = np.array(face)
            self.__vectors[id] = rx @ y


class Ellipsis:

    def __init__(self, a,b,c):
        self.__vectors = []

        circles = 0
        segments = 0
        t = 0
        step = math.pi/10

        max0 = -1000000000
        max1 = -1000000000
        max2 = -1000000000
        min0 = 1000000000
        min1 = 1000000000
        min2 = 1000000000
        while t < 2 * math.pi:  # кут тета
            f = 0
            segments = 0
            while f <= math.pi:  # кут фі
                x = (a * math.sin(f)) * math.cos(t)
                y = (b * math.sin(f)) * math.sin(t)
                z = c * math.cos(f)

                max0 = max(max0, float(x))
                max1 = max(max1, float(y))
                max2 = max(max2, float(z))
                min0 = min(min0, float(x))
                min1 = min(min1, float(y))
                min2 = min(min2, float(z))
                self.__vectors.append([x,y,z])  # задопомогою параметричного рівняння еліпса
                f += step
                segments += 1
            t += step
            circles += 1

        self.__triangles = make_triangles(circles, segments)

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

    def sort(self):
        self.__triangles.sort(key=lambda i: self.vertex(i[0])[2], reverse=False)
        pass

    def rotate_x(self, angle):
        rx = np.array([[1, 0, 0], [0, math.cos(angle), -math.sin(angle)], [0, math.sin(angle), math.cos(angle)]])
        for id, face in enumerate(self.__vectors):
            y = np.array(face)
            self.__vectors[id] = rx @ y

    def rotate_y(self, angle):
        rx = np.array([[math.cos(angle), 0, math.sin(angle)], [0, 1, 0], [-math.sin(angle), 0, math.cos(angle)]])
        for id, face in enumerate(self.__vectors):
            y = np.array(face)
            self.__vectors[id] = rx @ y

    def rotate_z(self, angle):
        rx = np.array([[math.cos(angle), -math.sin(angle), 0], [math.sin(angle), math.cos(angle), 0], [0, 0, 1]])
        for id, face in enumerate(self.__vectors):
            y = np.array(face)
            self.__vectors[id] = rx @ y