from platform_piece import *
from player import *

# method to draw text of different styles in a given location
# and allow you to set which point on text its drawn from
def draw_text(text, size, colour, background_colour, x, y ,draw_from):
    text = str(text)
    font = pg.font.Font('freesansbold.ttf', size)
    new_text = font.render(text, True, colour, background_colour)
    textRect = new_text.get_rect()
    if draw_from == 'tr':
        textRect.topright = (x,y)
    elif draw_from == 'center':
        textRect.center = (x,y)
    else:
        textRect.x = x
        textRect.y = y
    win.blit(new_text, textRect)

def check_quit(event):
    if event.type == pg.QUIT:
        pg.quit()
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_q and pg.key.get_mods() & pg.KMOD_CTRL:
            pg.quit()

def check_pause(event):
    pause = False
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_p:
            pause = True
            draw_text('PAUSED', 50  ,GREEN, BLACK, WIDTH / 2, HEIGHT / 2, 'center')
            pg.display.flip()
            wait_for(500)

    while pause:
        clock.tick(30)
        for event in pg.event.get():
            check_quit(event)

            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    pause = False
                    count_in()


# method to allow quitting window and wait for a key or time
def wait_for(time = False, any_key = False):
    key_index = [pg.K_p, pg.K_SPACE]
    if time:
        start_time = pg.time.get_ticks()

    while True:
        clock.tick(FPS)
        for event in pg.event.get():
            check_quit(event)
            if any_key:
                if event.type == pg.KEYUP:
                    return True
        if time:
            now = pg.time.get_ticks()
            if now - start_time >= time:
                return False

def count_in():
    text_list = ['3', '2', '1', 'FIGHT!']
    for i in range(4):
        win.blit(background_img,(0,0))
        all_sprites.draw(win)
        draw_text(text_list[i], 50, GREEN, BLACK, WIDTH/2, HEIGHT/2, 'center')
        pg.display.flip()
        wait_for(700)

# opening title scene display then shows instructions and waits for key
def title_sequence():
    demon_x = -400
    duel_x = WIDTH+400
    alpha = 0
    
    timer = 0
    waiting = True
    while waiting:
        clock.tick(30)
        timer += 1
        if timer >100:
            waiting = False

        # allow quitting
        for event in pg.event.get():
            check_quit(event)
        
        if demon_x < WIDTH/2-140:
            demon_x += 10
            duel_x-=10
        
        # make image fade in by increasing opacity
        if alpha < 255:
            alpha += 1

        background_img.set_alpha(alpha)
        win.blit(background_img,(0,0))
        draw_text('<-----  Demon ', 48 , LIGHT_BLUE, BLUE , demon_x , 100 , 'center')
        draw_text(' Duel  ----->', 48 , LIGHT_ORANGE, RED , duel_x , 100 , 'center')
        pg.display.flip()


    background_img.set_alpha(255)
    # display controls
    draw_text('ICE DEMON CONTROLS' ,18 ,GREEN ,BLACK, 0, 0 , '')
    draw_text('WASD KEYS TO MOVE' ,16 ,GREEN ,BLACK, 0, 30 , '')
    draw_text('SHIFT TO SHOOT' ,16 ,GREEN ,BLACK, 0, 50 , '')
    draw_text('CONTRL TO JUMP' ,16 ,GREEN ,BLACK, 0, 70 , '')
    draw_text('FIRE DEMON CONTROLS' ,18 ,GREEN ,BLACK, 1000, 0 , 'tr')
    draw_text('ARROW KEYS TO MOVE' ,16 ,GREEN ,BLACK, 1000, 30 , 'tr')
    draw_text('M TO SHOOT' ,16 ,GREEN ,BLACK, 1000, 50 , 'tr')
    draw_text('J TO JUMP' ,16 ,GREEN ,BLACK, 1000, 70 , 'tr')
    draw_text('P TO PAUSE' ,16 ,GREEN ,BLACK, WIDTH/2, 10, 'center')
    
    start = False
    while not start:

        draw_text('PRESS ANY KEY TO START' ,22 ,GREEN ,BLACK, 450, HEIGHT - 50 , 'center')
        pg.display.flip()
        start = wait_for(1000, True)

        if not start: # cancel next flash delay if keys been pressed   
            # make press any key text flash     
            draw_text('PRESS ANY KEY TO START' ,22 ,BLACK ,BLACK, 450, HEIGHT - 50 , 'center')
            pg.display.flip()
            start = wait_for(500, True)



def check_game_over():

    if player1.health < 1:
        winner = 1
    elif player2.health < 1:
        winner = 0
    else:
        return

    messages = ['FIRE DEMON WINS!!!', 'ICE DEMON WINS!!!'] 
    all_sprites.draw(win)
    player1.stats.draw_health()
    player2.stats.draw_health()
    player1.stats.draw_ammo(player1.ammo)
    player2.stats.draw_ammo(player2.ammo)

    draw_text('HP: '+ str(player1.health), 26 , RED, LIGHT_ORANGE, 901, 78, 'tr')
    draw_text('HP: '+ str(player2.health), 26 , BLUE, LIGHT_BLUE, 99, 78, '')

    num_flashes = 0
    while num_flashes < 6:
        num_flashes += 1
        draw_text(messages[winner], 48 , PLAYER_COLOURS[winner][1], PLAYER_COLOURS[winner][0] , WIDTH/2 , HEIGHT/2 , 'center')
        pg.display.flip()
        wait_for(500)
        
        # make winner message flash
        draw_text(messages[winner], 48 , PLAYER_COLOURS[winner][0], PLAYER_COLOURS[winner][1] , WIDTH/2 , HEIGHT/2 , 'center')
        pg.display.flip()
        wait_for(500)

    draw_text('PRESS ANY KEY TO QUIT' ,22 ,GREEN ,BLACK, 480, HEIGHT - 60 , 'center')
    pg.display.flip()
    wait_for(any_key=True)
    quit()


win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Demon Duel")
clock = pg.time.Clock()

platform_left = Platform_piece('left', 100, HEIGHT - 101)
platform_middle = Platform_piece('middle',200 , HEIGHT - 101)
platform_middle2 = Platform_piece('middle',400 , HEIGHT - 101)
platform_middle3 = Platform_piece('middle',600 , HEIGHT - 101)
platform_right = Platform_piece('right',800 , HEIGHT - 101)

player1 = Player(0, (WIDTH-150, GROUND_HEIGHT - 150))
player2 = Player(1, (150, GROUND_HEIGHT-150))

player1.other_player = player2
player2.other_player = player1

player1_group.add(player1)
player2_group.add(player2)
all_sprites.add(player1)
all_sprites.add(player2)

pg.mixer.music.play(loops=-1)

title_sequence()
count_in()

def game_loop():
    while True:
        clock.tick(FPS)

        for event in pg.event.get():
            check_pause(event)
            check_quit(event)
        check_game_over()
        
        win.blit(background_img,(0,0))

        all_sprites.update()
        all_sprites.draw(win)
        platforms.draw(win)

        draw_text('HP: '+ str(player1.health), 26 , RED, LIGHT_ORANGE, 901, 78, 'tr')
        draw_text('HP: '+ str(player2.health), 26 , BLUE, LIGHT_BLUE, 99, 78, '')
        pg.display.flip()

game_loop()
