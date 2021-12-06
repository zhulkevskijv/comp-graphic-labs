import cv2 as cv
import numpy as np

light_vector = np.array([-1, -1, -1])
see_vect = [1, 0, 0]


def draw_image_with_light(model, nameImage, wait_key=1):
    width = 1200
    height = 1200
    im2 = np.zeros((width + 1, height + 1, 3), dtype="uint8")
    for i in range(model.triangles_length()):
        face = model.triangle(i)
        triangl = [0, 0, 0]
        for j in range(3):
            vert = model.vertex(face[j])
            triangl[j] = width - int((vert[0] + 1) * width / 2), int(abs(height - (vert[1] + 1) * height / 2))
        color = get_face_color(face, model)
        cv.drawContours(im2, [np.array([triangl[0], triangl[1], triangl[2]])], 0, color, -1)

    cv.imshow(nameImage, im2)
    cv.waitKey(wait_key)


def get_color():
    return np.array([240, 240, 240])


def get_face_color(face, vector):
    object_color = get_color()
    light_color = np.array([1, 1, 1])

    x1, y1, z1 = vector.vertex(face[0])
    x2, y2, z2 = vector.vertex(face[1])
    x3, y3, z3 = vector.vertex(face[2])

    xn = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
    yn = (z2 - z1) * (x3 - x1) - (x2 - x1) * (z3 - z1)
    zn = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    normal = np.array([xn, yn, zn])

    if np.linalg.norm(normal).prod() != 0:
        normal = normal / np.linalg.norm(normal)

    # Ambient
    ambient_strength = 0.1
    ambient = ambient_strength * light_color


    #Diffuse
    light_pos = np.array([2.0, 1.0, 1.2])
    light_dir = light_pos - normal
    light_dir = light_dir / np.linalg.norm(light_dir)

    diff = max(np.dot(normal, light_dir), 0.0)
    diffuse = diff * light_color


    # Specular
    specular_strength = 0.3
    view_pos = [0.1, 0.3, 1]
    if np.prod(normal) != 0:
        reff_light_vect = normal * (2 * np.dot(normal, view_pos) / np.dot(normal, normal)) - view_pos
    else:
        return (0,0,0)
        reff_light_vect = normal * (2 * np.dot(normal, view_pos)) - view_pos
    reff_comp = max(np.dot(view_pos, reff_light_vect), 0.0)
    reff_comp = pow(reff_comp, 13)
    specular = reff_comp*specular_strength

    result = (ambient + diffuse + specular) * object_color

    return result
