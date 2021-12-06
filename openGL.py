import pygame as pg
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from math import cos, sin
import numpy as np


def get_normal(v1, v2, v3):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    x3, y3, z3 = v3
    normal_vector: np.ndarray = np.array([
        (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1),
        (z2 - z1) * (x3 - x1) - (x2 - x1) * (z3 - z1),
        (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    ])
    return normal_vector.tolist()

def rotate_x(angle, vectors):
    rx = np.array([[1, 0, 0], [0, cos(angle), -sin(angle)], [0, sin(angle), cos(angle)]])
    for id, face in enumerate(vectors):
        y = np.array(face)
        vectors[id] = rx @ y
    return vectors

def rotate_y(angle, vectors):
    rx = np.array([[cos(angle), 0, sin(angle)], [0, 1, 0], [-sin(angle), 0, cos(angle)]])
    for id, face in enumerate(vectors):
        y = np.array(face)
        vectors[id] = rx @ y
    return vectors


def rotate_z(angle, vectors):
    rx = np.array([[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]])
    for id, face in enumerate(vectors):
        y = np.array(face)
        vectors[id] = rx @ y
    return vectors

def make_ellipse(a, b, c):
    vectors = []
    circles = 0
    segments = 0
    t = 0
    step = math.pi/13

    while t < 2 * math.pi:
        f = 0
        segments = 0
        while f <= math.pi:
            vectors.append([a * math.sin(f) * math.cos(t),
                            b * math.sin(f) * math.sin(t),
                            c * math.cos(f)])
            f += step
            segments += 1
        t += step
        circles += 1

    faces = make_face(circles, segments)

    return faces, vectors


def make_face(circles, segments):
    faces = []
    for i in range(circles - 1):
        for j in range(segments - 1):

            a = [i * segments + j,
                 (i + 1) * segments + j,
                 i * segments + (j + 1)]

            b = [(i + 1) * segments + j + 1,
                 i * segments + (j + 1),
                 (i + 1) * segments + j]

            faces.append(a)
            faces.append(b)

    i = circles - 1
    for j in range(segments - 1):
        a = [i * segments + j, j, i * segments + j + 1]
        b = [j + 1, i * segments + j + 1, j]
        faces.append(a)
        faces.append(b)
    return faces


def make_torus(R, r):
    vectors = []

    parts = 0
    segments = 0
    step = math.pi/10
    t = 0
    while t < 2 * math.pi:
        f = -1.0*math.pi
        segments = 0
        while f < math.pi:
            x = (R + r*math.cos(f))*math.cos(t)
            y = (R + r*math.cos(f))*math.sin(t)
            z = r * math.sin(f)
            vectors.append([x, y, z])
            f += step
            segments += 1
        t += step
        parts += 1

    faces = make_face(parts, segments)

    return faces, vectors


def sort(faces, vector):
    return sorted(faces, key=lambda i: vector[int(i[0])][2], reverse=True)


def draw_figure(faces, vectors):
    glBegin(GL_TRIANGLES)
    for face in faces:
        v1, v2, v3 = face
        glNormal3f(*get_normal(vectors[v1], vectors[v2], vectors[v3]))
        glColor3fv([1.0, 0.62, 0.25])
        glVertex3fv(vectors[v1])
        glColor3fv([0.4, 0.28, 0.84])
        glVertex3fv(vectors[v2])
        glColor3fv([0.59, 0.95, 0.24])
        glVertex3fv(vectors[v3])
    glEnd()


if __name__ == '__main__':
    width = 700
    height = 700

    pg.init()
    display = (width, height)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    # glEnable(GL_BLEND)
    glEnable(GL_NORMALIZE)
    # glShadeModel(GL_SMOOTH)
    ambient = 0.1

    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [ambient, ambient, ambient, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [4, 4, 4, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

    lightPos = [1.0, -1.0, -1.0, 0.0]
    # glLightfv(GL_LIGHT0, GL_POSITION, lightPos)


    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_EXP)
    glFogf(GL_FOG_DENSITY, 0.2)
    glFogfv(GL_FOG_COLOR, [0.1, 0.1, 0.1, 1])

    glTranslatef(0,0,-4)

    # еліпс
    a1, a2 = make_ellipse(0.3, 0.2, 0.4)
    rotation1 = 0.05
    # тор
    t1, t2 = make_ellipse(0.3, 0.2, 0.2)
    rotation2 = 0.05
    # куля
    c1, c2 = make_ellipse(0.3, 0.3, 0.3)
    rotation3 = 0.05
    left = True
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        # clear all
        if lightPos[0] < -3:
            left=False
        if lightPos[0] > 3:
            left= True
        if left:
            lightPos = [lightPos[0]-0.1, -0.2, -5.0, 1.0]
        else:
            lightPos = [lightPos[0] + 0.1, -0.2, -5.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # ellipsis
        glPushMatrix()
        glTranslatef(-1, 0, 0)
        a2 = rotate_x(rotation1, a2)
        a2 = rotate_z(rotation1, a2)
        draw_figure(a1, a2)
        glPopMatrix()
        # torus
        glPushMatrix()
        glTranslatef(0, 0, 0)
        t2 = rotate_z(rotation2, t2)
        t2 = rotate_y(rotation2, t2)

        draw_figure(t1, t2)
        glPopMatrix()
        # sphere
        glPushMatrix()
        glTranslatef(1, 0, 0)
        c2 = rotate_y(rotation3, c2)
        c2 = rotate_x(rotation3, c2)
        draw_figure(c1, c2)
        glPopMatrix()

        pg.display.flip()
        pg.time.wait(10)
