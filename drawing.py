import cv2 as cv
import numpy as np





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


def get_face_color(face, model, ambient_coef=0.2, diffuse_coef=0.6, specular_coef=0.3, brightness=26):
    x1, y1, z1 = model.vertex(face[0])
    x2, y2, z2 = model.vertex(face[1])
    x3, y3, z3 = model.vertex(face[2])

    original_color = get_color()

    light_vector_pos = np.array([-2.0, 1, 1])
    see_vect = [1, 0, 0]

    res_color = np.zeros(3)

    normal_vect = np.array([
        (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1),
        (z2 - z1) * (x3 - x1) - (x2 - x1) * (z3 - z1),
        (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    ])

    normal_vect = normal_vect / np.linalg.norm(normal_vect)

    # Ambient
    res_color += original_color * ambient_coef

    # Diffuse
    diff_comp = max(np.dot(normal_vect, light_vector_pos), 0.0)
    res_color += diff_comp*diffuse_coef*original_color

    # Specular
    reff_light_vect = normal_vect*(2*np.dot(normal_vect, see_vect)/np.dot(normal_vect,normal_vect)) - see_vect
    reff_comp = max(np.dot(see_vect, reff_light_vect), 0.0)
    reff_comp = pow(reff_comp, brightness)
    res_color += reff_comp*specular_coef*original_color

    return [min(c, 255) for c in res_color]
