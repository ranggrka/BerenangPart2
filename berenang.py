from ursina import *
from random import randint

#Rangga
app = Ursina()
bg = Entity(model='quad', texture='assets/Background', scale=(96, 24), z=1)
bg2 = duplicate(bg, x=96)
player = Animation('assets/shark', fps=10, collider='box', scale=(6, 2), y=0, enabled=False)
shark = Entity(model=Animation('assets/player', fps=6), collider='box', scale=(12, 7), x=28, enabled=False)

window.fullscreen = True
camera.z = -57

music = Audio('assets/music.wav', loop=True)

sharks = []
score = 0
score_text = Text(text=f'Score: {score}', position=(-0.75, 0.45), origin=(0, 0), scale=2, enabled=False)

#Zidan
# Start menu
start_menu = Entity(parent=camera.ui, enabled=True)
start_bg = Entity(parent=start_menu, model='quad', texture='assets/Background', scale=(1.5, 0.75), z=0)
title = Text(parent=start_menu, text='Shark Game', origin=(0, 0), scale=3, y=0.2)
start_button = Button(parent=start_menu, text='Start Game', scale=(0.3, 0.1), y=-0.1, color=color.azure)

# Game over menu
game_over_menu = Entity(parent=camera.ui, enabled=False)
game_over_bg = Entity(parent=game_over_menu, model='quad', texture='assets/Background', scale=(1.5, 0.75), z=0)
game_over_text = Text(parent=game_over_menu, text='Game Over', origin=(0, 0), scale=3, y=0.2, color=color.red)
restart_button = Button(parent=game_over_menu, text='Restart', scale=(0.3, 0.1), y=-0.1, color=color.azure)

#Ahmad Sopyan
def newShark():
    if not player.enabled:
        return  # Hanya mengeluarkan hiu saat game sedang berjalan
    new = duplicate(shark)
    new.y = randint(-11, 11)
    side = randint(0, 1)  
    if side == 0:
        new.x = -30  
        new.rotation_z = 180  
    else:
        new.x = 30
    new.enabled = True
    sharks.append(new)
    invoke(newShark, delay=1)

#Haikal
def start_game():
    global score
    score = 0
    score_text.text = f'Score: {score}'
    score_text.enabled = True
    start_menu.enabled = False
    game_over_menu.enabled = False
    player.enabled = True
    player.position = (0, 0)
    music.play()
    newShark()

start_button.on_click = start_game
restart_button.on_click = start_game

def reset_game():
    for shark in sharks:
        destroy(shark)
    sharks.clear()
    
    player.enabled = False
    score_text.enabled = False

    music.stop()
    game_over_menu.enabled = True

#Bima
def input(key):
    if key == 'escape':
        exit()

def update():
    if not player.enabled:
        return

    global score
    bg.x -= 2 * time.dt
    bg2.x -= 2 * time.dt
    if bg.x < -96:
        bg.x = 96
    if bg2.x < -96:
        bg2.x = 96
    
    player.y += held_keys['w'] * 6 * time.dt
    player.y -= held_keys['s'] * 6 * time.dt
    player.x += held_keys['d'] * 6 * time.dt
    player.x -= held_keys['a'] * 6 * time.dt
    a = held_keys['w'] * -20
    b = held_keys['s'] * 20
    
    # Define the upper and lower bounds for the player's y position
    upper_bound = 11
    lower_bound = -11
    
    # Ensure the player's y position is within the bounds
    if player.y > upper_bound:
        player.y = upper_bound
    if player.y < lower_bound:
        player.y = lower_bound
    
    a = held_keys['w'] * -20
    b = held_keys['s'] * 20    
    if a != 0:
        player.rotation_z = a
    else:
        player.rotation_z = b

    for shark in sharks:
        if shark.x < -30 or shark.x > 30:
            sharks.remove(shark)
            destroy(shark)
        else:
            if shark.rotation_z == 180:
                shark.x += 10 * time.dt 
            else:
                shark.x -= 10 * time.dt 
            
        if player.intersects(shark).hit:
            reset_game()
        elif shark.x < -30 or shark.x > 30:
            score += 1
            score_text.text = f'Score: {score}'
            sharks.remove(shark)
            destroy(shark)

app.run()