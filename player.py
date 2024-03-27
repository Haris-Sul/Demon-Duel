from setup import *
from stats import *
from lasers import *

# load player 1 images
player_imgs = [[],[]]
player1_list = ["dvl1_fr1.gif","dvl1_lf1.gif","dvl1_lf2.gif","dvl1_rt1.gif","dvl1_rt2.gif","dvl1_lf_grdpnd.gif","dvl1_rt_grdpnd.gif","dvl1_death.gif"]
for img in player1_list:
    temp = pg.image.load(os.path.join(img_folder, img)).convert()
    temp.set_colorkey(WHITE)
    player_imgs[0].append(pg.transform.scale(temp, (PLAYER_WIDTH, PLAYER_HEIGHT)))
    
# load player 2 images
player2_list = ["dvl2_fr1.gif","dvl2_lf1.gif","dvl2_lf2.gif","dvl2_rt1.gif","dvl2_rt2.gif","dvl2_lf_grdpnd.gif","dvl2_rt_grdpnd.gif","dvl2_death.gif"]
for img in player2_list:
    temp = pg.image.load(os.path.join(img_folder, img)).convert()
    temp.set_colorkey(WHITE)
    player_imgs[1].append(pg.transform.scale(temp, (PLAYER_WIDTH, PLAYER_HEIGHT)))

# type determines if its player1 or player2
class Player(pg.sprite.Sprite):
    # sprite for the Player
    def __init__(self, type, start_pos):
        pg.sprite.Sprite.__init__(self)

        self.type = type
        # both players controls
        controls = [[pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_m],
                    [pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_LSHIFT]]
        
        # this players controls
        self.controls = controls[type]
        self.image = player_imgs[type][0]
        self.other_player = None

        self.stats = Stats(self.type)

        self.jumping = False
        self.jump_count = MAX_JUMP
        self.jump_reset_count = 0
        self.fall_count = 0
        self.off_edge = False
        self.space_is_pressed = False
        self.space_was_pressed = False

        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.start_pos = start_pos
        self.health = MAX_HEALTH
        self.ammo = MAX_AMMO
        self.ammo_counter = 0
        self.bonus_ammo = 0
        self.walking = False
        self.neutral = False
        self.walk_count = 0


    def move(self):
        key = pg.key.get_pressed()
        # if the key was the left button
        if key[self.controls[0]] and self.rect.x > 0:
            self.walking = True
            self.neutral = 'left'
            # update player animation frame
            if self.walk_count < 4:
                self.image = player_imgs[self.type][1]
                self.walk_count += 1
            elif self.walk_count > 3:
                self.image = player_imgs[self.type][2]
                self.walk_count += 1
                if self.walk_count == 8:
                    self.walk_count = 0
            
            # change x position by speed
            # checking for collisions on the way
            for i in range(PLAYER_SPEED):
                if self.rect.left > 0:
                    self.rect.x -= 1
                self.check_impacts()

        # if the key was the right button
        if key[self.controls[1]] and self.rect.right < WIDTH:                                                   
            self.walking = True
            self.neutral = 'right'
            # update player animation frame
            if self.walk_count < 4:
                self.image = player_imgs[self.type][3]
                self.walk_count += 1
            elif self.walk_count > 3:
                self.image = player_imgs[self.type][4]
                self.walk_count += 1
                if self.walk_count == 8:
                    self.walk_count = 0

            # change x position by speed
            # checking for collisions on the way
            for i in range(PLAYER_SPEED):
                if self.rect.right < WIDTH:
                    self.rect.x += 1
                self.check_impacts()

        # stop walking if left or right buttons were released
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if event.key == self.controls[0] or event.key == self.controls[1]:
                    self.walking = False

    def jump(self):
        key = pg.key.get_pressed()
        self.space_is_pressed = False

        # if the key was the up button
        if key[self.controls[2]]:
            self.space_is_pressed = True
            if not self.jumping:
                self.space_was_pressed = True
        
        # checking if space was already pressed allows for variable jump height
        if self.space_is_pressed and self.space_was_pressed:
            if self.jump_count > 0:
                self.jumping = True
                # vary jump height change quadratically
                change = ((self.jump_count**2))/2

                # checking for collisions on the way
                for i in range (int(change)):
                    self.rect.y -= 1
                    self.check_impacts()
                self.jump_count -= 1

        # if space is released or jump ends
        if self.space_was_pressed and (not self.space_is_pressed or self.jump_count == 0):
            self.jump_count = 0
            # keep track of fall after jump
            temp = self.fall_count * 2
            for i in range(temp):
                if self.rect.bottom < GROUND_HEIGHT:
                    self.rect.y += 1
                    self.check_impacts()

            # reset jump parameters after jump phase is over
            self.fall_count += 1
            if self.fall_count == 4:
                self.space_was_pressed = False
                self.fall_count = 0
                self.jump_count = False
                self.jumping = False

    # reset jump capabilities after reaching lower surface
    def jump_reset(self):
        platform_collisions = pg.sprite.spritecollide(self, platforms, False)
        if platform_collisions:
            if self.rect.bottom == GROUND_HEIGHT:
                self.jump_reset_count += 1
                if self.jump_reset_count == 5:
                    self.jump_reset_count = 0
                    self.jump_count = MAX_JUMP


    def shoot(self):                                                                                    
        key = pg.key.get_pressed()
        if self.ammo > 0:
            # if the shoot key was pressed and the direction is set 
            if key[self.controls[4]] and self.neutral:
                pg.mixer.Channel(0).play(pg.mixer.Sound(laser_snd))
                # set laser direction based on arrow key combination
                if key[self.controls[0]] and key[self.controls[2]]:
                    laser_speed_x = -15
                    laser_speed_y = -15
                elif key[self.controls[0]] and key[self.controls[3]]:
                    laser_speed_x = -15
                    laser_speed_y = 15
                elif key[self.controls[1]] and key[self.controls[2]]:
                    laser_speed_x = 15
                    laser_speed_y = -15
                elif key[self.controls[1]] and key[self.controls[3]]:
                    laser_speed_x = 15
                    laser_speed_y = 15
                elif key[self.controls[2]]:
                    laser_speed_x = 0
                    laser_speed_y = -20
                elif key[self.controls[3]]:
                    laser_speed_x = 0
                    laser_speed_y = 20

                # shoot in current direction if no arrow keys are pressed 
                elif self.neutral == 'left':
                    laser_speed_x = -20
                    laser_speed_y = 0
                elif self.neutral == 'right':
                    laser_speed_x = 20
                    laser_speed_y = 0
                if self.neutral  == 'right':
                    temp = self.rect.right
                elif self.neutral == 'left':
                    temp = self.rect.left
                laser = Lasers(self.type, temp, self.rect.centery, laser_speed_x, laser_speed_y)
                self.ammo -= 1
                all_sprites.add(laser)
                player_lasers[self.type].add(laser)
                all_lasers.add(laser)

        # reload 1 ammo after timer
        if self.ammo < MAX_AMMO + self.bonus_ammo:
            self.ammo_counter += 1
            if self.ammo_counter == AMMO_REGEN_TIME:
                self.ammo_counter = 0
                self.ammo += 1

    def check_impacts(self):
        direction = False
        # check collisions between this  player and the other players group
        impacts = pg.sprite.spritecollide(self, pg.sprite.Group(self.other_player), False)
        if impacts:

            x_difference = self.rect.centerx - self.other_player.rect.centerx
            y_difference = self.rect.centery - self.other_player.rect.centery
            if x_difference > 47: #this player to right
                direction = 'right'
                for i in range(5):
                    if self.rect.right < WIDTH:
                        self.rect.x += 1
                for i in range(5):
                    if self.other_player.rect.left > 0:
                        self.other_player.rect.x -= 1

            elif x_difference < -47: #this player to left
                direction = 'left'
                for i in range(5):
                    if self.rect.left > 0:
                        self.rect.x -= 1
                for i in range(5):
                    if self.rect.right < WIDTH:
                        self.other_player.rect.x += 1

            if y_difference > 47: #this player below
                direction = 'below'                                                     
                for i in range(5):
                    if self.rect.bottom < GROUND_HEIGHT:
                        self.rect.y += 1
                self.other_player.rect.y -= 5

            elif y_difference < -47: #this player above
                direction = 'above'
                self.rect.y -= 5
                self.jump_count = MAX_JUMP
                for i in range(5):
                    if self.other_player.rect.bottom < GROUND_HEIGHT:
                        self.other_player.rect.y += 1

            # If one player is on top but to the side of the other
            if direction == 'above' and x_difference > 25:
                self.rect.x += 2
            elif direction == 'above' and x_difference < -25:
                self.rect.x -= 2
            elif direction == 'below' and x_difference < -25:
                self.other_player.rect.x += 2
            elif direction == 'below' and x_difference < -25:
                self.other_player.rect.x -= 2

    # when falling off edge avoids collision problems
    # but allows movement and applies edgefall health loss
    def edgefall(self):

        self.move()
        self.rect.y += 30
        if self.rect.top > HEIGHT:
            self.jump_count = False
            for i in range(5):
                if self.health > 0:
                    self.health -= 1
                    self.stats.lose_health()
            self.rect.center = self.start_pos
            self.neutral = 'left'
            self.image = player_imgs[self.type][1]
            self.image.set_colorkey(WHITE)
            self.off_edge = False

    def gravity(self):
        if self.rect.bottom < GROUND_HEIGHT:
            for i in range(20):
                if self.rect.bottom < GROUND_HEIGHT or self.rect.right < EDGES or self.rect.left > WIDTH - EDGES:
                    self.check_impacts()
                    self.rect.y += 1

    # players main loop and method calls 
    def update(self):
        if not self.off_edge:
            self.move()
            if self.rect.right < EDGES or self.rect.left > WIDTH - EDGES:
                if self.rect.bottom > GROUND_HEIGHT - 20:
                    self.off_edge = True
            self.jump()

        else:
            self.edgefall()
            self.gravity()
        if not self.jumping and not self.off_edge:
            self.jump_reset()
            self.gravity()
        self.shoot()
        self.check_impacts()

        # check collisions of this player and the other players lasers
        hits = pg.sprite.spritecollide(self, player_lasers[not self.type], True)                                      
        if hits:
            if self.health > 0:
                self.health -= 1
                self.stats.lose_health()

        self.stats.draw_health()
        self.stats.draw_ammo(self.ammo)

        if self.health < 1:
            self.image = player_imgs[self.type][7]