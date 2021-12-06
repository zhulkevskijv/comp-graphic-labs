from Model import Model
from objects import Torus
from paintVoronyi import draw_image
from drawing import draw_image_with_light
if __name__ == '__main__':
    model = Model(r'../objects/african_head.obj')
    # model = Torus(100, 50)
    # draw_image(model, "Starting rotations")
    while True:
        model.rotate_x(-0.1)
        # model.rotate_y(0.1)
        model.rotate_z(-0.1)

        model.sort()
        draw_image_with_light(model, "Rotation", wait_key=1)