import pygame as pg
import os
from os import path

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0 ,0)
LIGHT_ORANGE = (255, 220, 180)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 200, 240)
GREEN = (0, 255, 50)
PLAYER_COLOURS = [[RED, LIGHT_ORANGE], [BLUE, LIGHT_BLUE]]

FPS = 20
WIDTH = 1000
HEIGHT = 600
EDGES = 100  # size of gaps at edges of platform
GROUND_HEIGHT = 500  # y coordinate of top of platform

MAX_HEALTH = 30
MAX_AMMO = 5
AMMO_REGEN_TIME = 8  # out of the FPS value 
MAX_JUMP = 10
PLAYER_SPEED = 16 # must be integer
PLAYER_HEIGHT = 50
PLAYER_WIDTH = 50

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
snd_folder = os.path.join(path.dirname(__file__),'sound')

pg.init()
pg.mixer.pre_init()
pg.mixer.init()
win = pg.display.set_mode((1000, 600))

background_img = pg.image.load(os.path.join(img_folder,"background v2.png")).convert()

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

# load sound/music
pg.mixer.music.load(path.join(snd_folder,'bgd_music.ogg'))
pg.mixer.music.set_volume(0.15)
laser_snd = pg.mixer.Sound(path.join(snd_folder,'laser_sound.wav'))
laser_snd2 = pg.mixer.Sound(path.join(snd_folder,'laser_sound2.wav'))
hurt_snd= pg.mixer.Sound(path.join(snd_folder,'hurt_sound.wav'))
hurt_snd2 = pg.mixer.Sound(path.join(snd_folder,'hurt_sound2.wav'))

all_sprites = pg.sprite.Group()
platforms = pg.sprite.Group()

player1_group = pg.sprite.Group()
player2_group = pg.sprite.Group()

red_lasers = pg.sprite.Group()
blue_lasers = pg.sprite.Group()
player_lasers = [red_lasers, blue_lasers]
all_lasers = pg.sprite.Group()

