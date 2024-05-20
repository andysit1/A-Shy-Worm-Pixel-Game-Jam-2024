
from pygame import pg





# def rotate_surf()


def blitRotate2(surf, image, topleft, angle):
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    pg.draw.rect(surf, (255, 0, 0), new_rect, 2)