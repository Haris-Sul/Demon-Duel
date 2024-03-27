from setup import *

edge_platforms = pg.sprite.Group()

platform_left_img = pg.image.load(os.path.join(img_folder,"platform_left.png")).convert()
platform_middle_img = pg.image.load(os.path.join(img_folder,"platform_middle.png")).convert()
platform_right_img = pg.image.load(os.path.join(img_folder,"platform_right.png")).convert()

class Platform_piece(pg.sprite.Sprite):
    def __init__(self, part, x, y):
        pg.sprite.Sprite.__init__(self)
        
        # platforms split into segments to avoid distortion
        # and allow variable length platforms
        self.part = part
        if self.part == 'left':
            self.image = platform_left_img
            edge_platforms.add(self)
        elif self.part == 'middle':
            self.image = platform_middle_img
        elif self.part ==  'right':
            edge_platforms.add(self)
            self.image = platform_right_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        platforms.add(self)
        all_sprites.add(self)