from itertools import cycle
from random import randrange
from tkinter import Tk, Canvas, messagebox, font, TclError

# Game setup variables
canvas_width = 800
canvas_height = 400

# Initialize the main window
win = Tk()
win.title("Egg Catcher")
c = Canvas(win, width=canvas_width, height=canvas_height, background='deep sky blue')
c.create_rectangle(-5, canvas_height - 100, canvas_width + 5, canvas_height + 5, fill='sea green', width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

# Game design variables
color_cycle = cycle(['light blue', 'light pink', 'light yellow', 'light green', 'red', 'blue', 'green', 'black'])
egg_width = 45
egg_height = 55
egg_score = 10

# Tracking variables to hold active .after() IDs so we can cancel them on reset
create_eggs_id = None
move_eggs_id = None
catch_check_id = None

# Catcher setup
catcher_color = 'blue'
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height - catcher_height - 20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

catcher = c.create_arc(catcher_start_x, catcher_start_y, catcher_start_x2, catcher_start_y2, start=200, extent=140, style='arc', outline=catcher_color, width=3)

# Score and lives setup
score = 0
score_text = c.create_text(10, 10, anchor='nw', font=('Arial', 18, 'bold'), fill='darkblue', text='Score : ' + str(score))

lives_remaning = 3
lives_text = c.create_text(canvas_width - 10, 10, anchor='ne', font=('Arial', 18, 'bold'), fill='darkblue', text='Lives : ' + str(lives_remaning))

eggs = []

# Function to create eggs at random positions
def create_eggs():
    global create_eggs_id
    if not c.winfo_exists(): return  # Safety check
    
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    create_eggs_id = win.after(egg_interval, create_eggs)

# Function to move eggs downwards
def move_eggs():
    global move_eggs_id
    if not c.winfo_exists(): return  # Safety check
    
    # FIX: Loop through a COPY of the list (eggs[:]) so removing items doesn't break the loop
    for egg in eggs[:]:
        try:
            (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
            c.move(egg, 0, 10)
            if egg_y2 > canvas_height:
                egg_dropped(egg)
        except TclError:
            return

    move_eggs_id = win.after(egg_speed, move_eggs)

# Function to handle egg drop events
def egg_dropped(egg):
    global lives_remaning
    if egg in eggs:
        eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    
    if lives_remaning <= 0:
        # Stop everything instantly before showing the pop-up box
        stop_game_loops()
        
        response = messagebox.askyesno('GAME OVER!', 'Final Score: ' + str(score) + '\nDo you want to play again?')
        if response:
            reset_game()  
        else:
            win.destroy()  

# Function to cancel old timers to prevent speed multiplication bugs
def stop_game_loops():
    global create_eggs_id, move_eggs_id, catch_check_id
    if create_eggs_id: win.after_cancel(create_eggs_id)
    if move_eggs_id: win.after_cancel(move_eggs_id)
    if catch_check_id: win.after_cancel(catch_check_id)

# Function to reset the game state for a new game
def reset_game():
    global score, lives_remaning, eggs, egg_speed, egg_interval
    
    stop_game_loops() # Clean up all ghost background timers
    
    for egg in eggs:
        c.delete(egg)
    eggs = []
    
    # Reset speeds to default base levels
    egg_speed = 500
    egg_interval = 4000
    score = 0
    lives_remaning = 3
    
    c.itemconfigure(score_text, text='Score : ' + str(score))
    c.itemconfigure(lives_text, text='Lives : ' + str(lives_remaning))
    
    # Move catcher back to the center position
    c.coords(catcher, catcher_start_x, catcher_start_y, catcher_start_x2, catcher_start_y2)
    
    # Restart fresh game loops
    start_game_loops()

# Function to decrease lives
def lose_a_life():
    global lives_remaning
    lives_remaning -= 1
    c.itemconfigure(lives_text, text='Lives : ' + str(lives_remaning))

# Function to check if eggs are caught
def catch_check():
    global catch_check_id, eggs
    if not c.winfo_exists(): return  # Safety check
    
    try:
        (catcher_x, catcher_y, catcher_x2, catcher_y2) = c.coords(catcher)
        for egg in eggs[:]: # Loop through a copy here too
            (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
            if catcher_x < egg_x and egg_x2 < catcher_x2 and catcher_y2 - egg_y2 < 40:
                eggs.remove(egg)
                c.delete(egg)
                increase_score(egg_score)
    except TclError:
        return
        
    catch_check_id = win.after(100, catch_check)

# Function to increase the score
def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    c.itemconfigure(score_text, text='Score : ' + str(score))

# Event handlers for moving the catcher
def move_left(event):
    if not c.winfo_exists(): return
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    if not c.winfo_exists(): return
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.focus_set()

def start_game_loops():
    global create_eggs_id, move_eggs_id, catch_check_id
    create_eggs_id = win.after(1000, create_eggs)
    move_eggs_id = win.after(1000, move_eggs)
    catch_check_id = win.after(1000, catch_check)

# Run initialization variables 
egg_speed = 500
egg_interval = 4000
difficulty_factor = 0.95

# Start the game processes
start_game_loops()
win.mainloop()