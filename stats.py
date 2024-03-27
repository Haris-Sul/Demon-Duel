from setup import *

red_profile_img = pg.image.load(os.path.join(img_folder,"player1 profile new.png")).convert()
red_profile_img.set_colorkey(WHITE)
red_health_bar_left_img = pg.image.load(os.path.join(img_folder,"player1 health bar left.png")).convert()
red_health_bar_left_img.set_colorkey(WHITE)
red_health_bar_right_img = pg.image.load(os.path.join(img_folder,"player1 health bar right.png")).convert()
red_health_bar_right_img.set_colorkey(WHITE)

blue_profile_img = pg.image.load(os.path.join(img_folder,"player2 profile new.png")).convert()
blue_profile_img.set_colorkey(WHITE)
blue_health_bar_left_img = pg.image.load(os.path.join(img_folder,"player2 health bar left.png")).convert()
blue_health_bar_left_img.set_colorkey(WHITE)
blue_health_bar_right_img = pg.image.load(os.path.join(img_folder,"player2 health bar right.png")).convert()
blue_health_bar_right_img.set_colorkey(WHITE)

health_bar_middle_img = pg.image.load(os.path.join(img_folder,"health bar middle.png")).convert()
health_bar_middle_img.set_colorkey(WHITE)

class Stats(pg.sprite.Sprite):
    def __init__(self, type):
        pg.sprite.Sprite.__init__(self)

        self.type = type
        health_bar_length = MAX_HEALTH
        while health_bar_length <= 100:
            health_bar_length = health_bar_length *2
        self.health_bar_middle = pg.transform.scale(health_bar_middle_img, (health_bar_length -17, 24))
        self.hb_middle_length = health_bar_length -17

        self.health_colour = 255
        self.health_length = health_bar_length
        self.one_health_length = self.health_length// MAX_HEALTH
        self.colour_count = 0
        self.health_darkness = 255

    # update colour and size of healthbar when you lose health
    def lose_health(self):
        pg.mixer.Channel(1).play(pg.mixer.Sound(hurt_snd))
        
        self.health_length -= self.one_health_length
        self.health_colour -= self.one_health_length
        # if type is not 0 colour change is doubled
        # to give correct colour change for player 2's healthbar
        if self.colour_count == 0 or self.type:
            self.health_darkness -= self.one_health_length
        self.colour_count +=1
        if self.colour_count == 3:
            self.colour_count = 0

    # display health related stats and profile background images
    def draw_health(self):
        if self.type == 0:
            win.blit(red_profile_img, (WIDTH - 320,0))
            colour = (self.health_darkness, self.health_colour, 0)
            pg.draw.polygon(win, colour, ((900 - self.health_length,51),(915 - self.health_length, 66),(915 , 66),(900,51)))
            win.blit(red_health_bar_right_img, (900, 47))
            win.blit(self.health_bar_middle, (900 - self.hb_middle_length, 47))
            win.blit(red_health_bar_left_img, (900 - self.hb_middle_length -21,47))
        else:
            win.blit(blue_profile_img, (0,0))
            win.blit(blue_health_bar_left_img, (80,47))
            win.blit(self.health_bar_middle, (100, 47))
            win.blit(blue_health_bar_right_img, (self.hb_middle_length + 100, 47))
            colour = (0, self.health_colour, self.health_darkness)
            pg.draw.polygon(win, colour, ((100,51),(85, 66),(self.health_length + 85 , 66),(self.health_length + 100,51)))

        

    # display laser count stat to show reloading
    def draw_ammo(self, ammo_count):
        x_pos = [789,201].pop(self.type)

        for i in range(ammo_count):
            win.blit(laser_imgs[1][self.type], (x_pos, 79))
            # add offset and invert for player 2
            if self.type == 0:
                x_pos -= 12
            else:
                x_pos += 12