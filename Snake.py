from tkinter import *
import random
import time

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 110
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, high_score, speed

        score += 1

        if score > high_score:
            high_score = score
            high_score_label.config(text="High Score:{}".format(high_score))

        score_label.config(text="Score:{}".format(score))

        if score % 5 == 0:
            speed -= 10

        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 80,
                       font=('consolas', 30), text="Press 'R' to Restart", fill="white")
    
def restart_game():
    global score, speed, direction, snake, food, running
    score = 0
    speed = SPEED
    direction = 'down'
    snake = Snake()
    food = Food()
    score_label.config(text="Score:{}".format(score))
    high_score_label.config(text="High Score:{}".format(high_score))
    next_turn(snake, food)

def restart_game():
    global score, speed, direction, snake, food, running
    score = 0
    speed = SPEED
    direction = 'down'
    snake = Snake()
    food = Food()
    score_label.config(text="Score:{}".format(score))
    high_score_label.config(text="High Score:{}".format(high_score))
    next_turn(snake, food)

def switch_theme():
    global BACKGROUND_COLOR, SNAKE_COLOR, FOOD_COLOR

    if background_color_button.cget("text") == "Dark Mode":
        background_color_button.config(text="Light Mode")
        BACKGROUND_COLOR = "#FFFFFF"
        SNAKE_COLOR = "#000000"
        FOOD_COLOR = "#0000FF"
    else:
        background_color_button.config(text="Dark Mode")
        BACKGROUND_COLOR = "#000000"
        SNAKE_COLOR = "#00FF00"
        FOOD_COLOR = "#FF0000"

    canvas.config(bg=BACKGROUND_COLOR)

def pause_game():
    global running
    running = False
    pause_button.config(text="Resume", command=resume_game)

def resume_game():
    global running
    running = True
    pause_button.config(text="Pause", command=pause_game)
    next_turn(snake, food)

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
high_score = 0
direction = 'down'
speed = SPEED

score_label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
score_label.pack()

high_score_label = Label(window, text="High Score:{}".format(high_score), font=('consolas', 40))
high_score_label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Binding for W, A, S, D keys
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<s>', lambda event: change_direction('down'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<r>', lambda event: restart_game() if not running else None)

background_color_button = Button(window, text="Dark Mode", command=switch_theme)
background_color_button.pack()

snake = Snake()
food = Food()

next_turn(snake, food)

running = True
pause_button = Button(window, text="Pause", command=pause_game)
pause_button.pack()

def timed_mode():
    global speed
    speed = 100
    score_label.config(text="Score:{}".format(score))
    window.after(1000, timed_mode)

start_time = time.time()
timed_mode_button = Button(window, text="Timed Mode", command=timed_mode)
timed_mode_button.pack()

window.mainloop()
