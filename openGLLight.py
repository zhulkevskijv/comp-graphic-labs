import pygame
from OpenGL.GL import *
from pygame.locals import *
import numpy as np
from math import cos, sin, pi, radians


def translate(vertex, vector):
    return (np.array(vertex) + np.array(vector)).tolist()

def rotate(vertex, theta_x=0., theta_y=0., theta_z=0.):
    arr: np.ndarray  = np.array(
        # X
        [[1, 0, 0],
         [0, cos(-theta_x), -sin(-theta_x)],
         [0, sin(-theta_x), cos(-theta_x)]],
    ).dot(
        # Y
        np.array([
            [cos(-theta_y), 0, sin(-theta_y)],
            [0, 1, 0],
            [-sin(-theta_y), 0, cos(-theta_y)]
        ])
    ).dot(
        # Z
        np.array([
            [cos(-theta_z), -sin(-theta_z), 0],
            [sin(-theta_z), cos(-theta_z), 0],
            [0, 0, 1]
        ])
    ).dot(
        np.transpose(np.array(vertex))
    )
    return arr.tolist()


def circle(r, vertices_count):
    for i in range(vertices_count):
        angle = 2 * pi * i / vertices_count
        yield int(r * cos(angle)), int(r * sin(angle)), 0


def move_cycle(arr: list):
    copy = arr[1:]
    return copy + [arr[0]]


def torus(R, r, vertices_count):
    cut_circles = []
    for i in range(vertices_count):
        angle = 2 * pi * i / vertices_count
        translate_vector = [R * cos(angle), 0, R * sin(angle)]
        cut_circles.append(
            [
                translate(rotate(vertex, theta_y=angle), translate_vector)
                for vertex
                in circle(r, vertices_count)
            ]
        )
    faces = []
    for circle1, circle2 in zip(cut_circles, move_cycle(cut_circles)):
        for v1, v2, v3, v4 in zip(circle1, move_cycle(circle1), circle2, move_cycle(circle2)):
            faces.extend([
                (v1, v2, v3),
                (v2, v4, v3)
            ])
    return faces

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


def ellipsis(a, b, c):
    t=0
    circles = 0
    segments = 0
    t = 0
    step = pi / 10
    vectors = []
    while t < 2 * pi:  # кут тета
        f = 0
        segments = 0
        while f <= pi:  # кут фі
            x = (a * sin(f)) * cos(t)
            y = (b * sin(f)) * sin(t)
            z = c * cos(f)

            vectors.append([x, y, z])
            f += step
            segments += 1
        t += step
        circles += 1

    faces = make_triangles(circles, segments)
    faces = map(lambda face: (vectors[face[0]], vectors[face[1]], vectors[face[2]]), faces)
    return faces

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


def get_z_order(face):
    (v1, v2, v3), face_color = face
    return min(v1[2], v2[2], v3[2])


# noinspection DuplicatedCode
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


def gen_torus(R, r, vertices_count=16):
    faces_normals = []
    for face in torus(R, r, vertices_count):
        faces_normals.append((face, get_normal(*face)))
    return faces_normals

def gen_ellipsis(a, b, c):
    faces_normals = []
    for face in ellipsis(a, b, c):
        faces_normals.append((face, get_normal(*face)))
    return faces_normals


def draw_torus(generated_torus):
    glBegin(GL_TRIANGLES)
    for face, normal in generated_torus:
        yield face
        v1, v2, v3 = face
        glNormal3f(*normal)

        glColor3fv((0.4, 0.8, 0.4))
        glVertex3fv(v1)

        glColor3fv((0.5, 0.3, 0.8))
        glVertex3fv(v2)

        glColor3fv((0.3, 0.5, 0.9))
        glVertex3fv(v3)
    glEnd()


def main():
    width = 1000
    height = 800

    # Viewport Init
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    glOrtho(0, width, 0, height, 2000, -2000)
    glTranslatef(width / 2, height / 2, 0)

    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [4, 4, 4, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [3, 1, 4, 0])

    toruses = [
        # gen_torus(250, 45),
        # gen_torus(150, 37),
        # gen_torus(60, 28),
        gen_ellipsis(80, 70, 60),
        gen_ellipsis(120, 140, 160),
        gen_ellipsis(100, 100, 100)
    ]

    rotations = [0 for t in toruses]
    glRotatef(-40, 1, 0.2, 0)


    n = 30
    i = 0
    while True:
        pygame.time.wait(int(30 / n))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for tor_i, tor in enumerate(toruses):
            glPushMatrix()
            rotations[tor_i] += (tor_i + 1) * 1.5
            # glRotatef(rotations[tor_i], 1, 1, 1)
            # glRotatef(rotations[tor_i], 1, 0, 0)
            if tor_i == 0:
                glTranslatef(200,-100,200)
            elif tor_i==1:
                glTranslatef(-300,-300,0)
            else:
                glTranslatef(-200,200,200)
            glRotatef(rotations[tor_i], 0, 1, 0)
            glRotatef(rotations[tor_i], 1, 0, 1)
            for face in draw_torus(tor):
                rotation = radians(rotations[tor_i])
                # [rotate(v, theta_x=0, theta_y=-rotation, theta_z=-rotation) for v in face]
                #     # [rotate(v, theta_x=rotation) for v in face]
                #     # [rotate(v, theta_y=-rotation) for v in face]
                #     # [rotate(v, theta_z=-rotation) for v in face]
                # )

            glPopMatrix()

        if i == 0:
            glAccum(GL_LOAD, 1.0 / n)
        else:
            glAccum(GL_ACCUM, 1.0 / n)

        i+=1
        pygame.display.flip()
        if i >= n:
            i = 0
            glAccum(GL_RETURN, 1.0)
            pygame.time.wait(30)




if __name__ == '__main__':
    main()

