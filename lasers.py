from setup import *

red_laser_img = pg.image.load(os.path.join(img_folder,"new_red_laser_x1.png")).convert()
blue_laser_img = pg.image.load(os.path.join(img_folder,"new_blue_laser_x1.png")).convert()

red_circle_laser_img = pg.image.load(os.path.join(img_folder,"red_circle_laser.png")).convert()
blue_circle_laser_img = pg.image.load(os.path.join(img_folder,"blue_circle_laser.png")).convert()
red_circle_laser_img.set_colorkey(WHITE)
blue_circle_laser_img.set_colorkey(WHITE)

vertical_red_laser_img = pg.image.load(os.path.join(img_folder,"vertical_red_laser.png")).convert()
vertical_blue_laser_img = pg.image.load(os.path.join(img_folder,"vertical_blue_laser.png")).convert()
vertical_red_laser_img.set_colorkey(BLACK)
vertical_blue_laser_img.set_colorkey(BLACK)

laser_imgs = [[red_laser_img,blue_laser_img], [vertical_red_laser_img,vertical_blue_laser_img], [red_circle_laser_img, blue_circle_laser_img]]


# type determines if its player1 or player2's bullet
class Lasers(pg.sprite.Sprite):
    def __init__(self, type, x, y, speed_x, speed_y):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        self.speed_x = speed_x
        self.speed_y = speed_y

        # laser image depends on speed
        if speed_y == 15 or speed_y == -15:
            # diagonal laser
            self.image = laser_imgs[2][self.type]
        elif speed_x == 0:
            # vertical laser
            self.image = laser_imgs[1][self.type]
            self.spawn_position = False
        else:
            # horizontal laser
            self.image = laser_imgs[0][self.type]

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left > WIDTH:
            self.kill()
        elif self.rect.right < 0:
            self.kill()