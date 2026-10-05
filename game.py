from ursina import *
import time

app = Ursina()

# --- WINDOW CONFIGURATION ---
window.title = "One Minute Walk - Fixed"
window.borderless = False
window.fullscreen = False
window.color = color.black

# --- LIGHTING & ENVIRONMENT (Fixed darkness issue) ---
# Add a directional light so the 3D world is visible
DirectionalLight().look_at(Vec3(1, -1, -1))
AmbientLight(color=color.rgb(100, 100, 100))

# Create a ground floor
ground = Entity(model='plane', scale=(50, 1, 50), color=color.dark_gray, texture='white_cube')

# Add some simple 3D obstacles/walls
wall1 = Entity(model='cube', position=(0, 1.5, 10), scale=(10, 3, 1), color=color.light_gray)
wall2 = Entity(model='cube', position=(-10, 1.5, 0), scale=(1, 3, 10), color=color.light_gray)
wall3 = Entity(model='cube', position=(10, 1.5, 0), scale=(1, 3, 10), color=color.light_gray)

# --- PLAYER SETUP ---
from ursina.prefabs.first_person_controller import FirstPersonController
player = FirstPersonController()
player.x = 0
player.z = -5
player.y = 2
player.cursor.visible = True

# --- UI ELEMENTS ---
timer_text = Text(text='Time Left: 60s', position=(-0.85, 0.45), scale=2, color=color.white)

# --- JUMP SCARE SETUP (Fixed to guarantee visibility) ---
# Create a giant red/white screen directly attached in front of the camera view
scare_bg = Entity(parent=camera.ui, model='quad', scale=(2, 2), color=color.red, z=-1, enabled=False)
scare_text = Text(parent=camera.ui, text='BOO!', position=(-0.22, 0.1), scale=6, color=color.yellow, enabled=False)

# --- GAME VARIABLES ---
start_time = time.time()
game_duration = 60  # 60 seconds
jump_scare_triggered = False

def update():
    global jump_scare_triggered
    
    if jump_scare_triggered:
        return

    # Calculate remaining time
    elapsed_time = time.time() - start_time
    time_left = int(game_duration - elapsed_time)
    
    if time_left > 0:
        timer_text.text = f'Time Left: {time_left}s'
    else:
        # Time is up! Trigger the jump scare
        timer_text.enabled = False
        trigger_jump_scare()

def trigger_jump_scare():
    global jump_scare_triggered
    jump_scare_triggered = True
    
    # Freeze player movement and unlock mouse
    player.enabled = False
    mouse.locked = False
    
    # Enable jump scare visual elements instantly
    scare_bg.enabled = True
    scare_text.enabled = True
    
    # Play an audio beep for shock effect if audio is supported
    try:
        Audio('click.wav', pitch=0.5, volume=2)
    except:
        pass
    
    # Strobe flashing effect loop
    def flash(count):
        if count > 0:
            # Swap colors rapidly
            if scare_bg.color == color.red:
                scare_bg.color = color.black
                scare_text.color = color.red
            else:
                scare_bg.color = color.red
                scare_text.color = color.yellow
            # Repeat flash every 0.1 seconds
            invoke(flash, count - 1, delay=0.1)

    # Start flashing 15 times
    flash(15)

app.run()