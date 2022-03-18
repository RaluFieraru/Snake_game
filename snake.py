from tkinter import *
import random

#Se creaza niste parametrii generali, care isi vor pastra valoarea (constante)
BOARD_WIDTH = 700
BOARD_HEIGHT = 700
BACKGROUND_COLOR = "#4D9EB6"
SPEED_GAME = 100
SPACE_SIZE = 50
SNAKE_BODY = 3
SNAKE_COLOR = "#36B35B"
FOOD_COLOR = "#FF423C"

class Snake:
    #Definim clasa Snake si constructorul
    def __init__(self):
        self.body_size = SNAKE_BODY
        self.coordinates = []
        self.squares = []
    #Se creaza o lista si se adauga coordonatele initiale ale sarpelui
        for i in range(0, SNAKE_BODY):
            self.coordinates.append([0, 0])
    #Se creaza partile sarpelui in forma de patrat
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        x = random.randint(0, (BOARD_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (BOARD_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
        #vom crea mancarea in forma ovala si o vom distribui aleator pe tabla de joc
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
    #in cazul in care miscarea este permisa si sarpele va ajunge la mancare, acesta va creste
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, SPEED_GAME
        score += 1 #modificam scorul in cazul in care sarpele atinge hrana
        SPEED_GAME -=10 #modificam viteza in cazul in care sarpele atinge hrana
        label.config(text="Score:{}".format(score))
        canvas.delete("food") #se sterge mancarea curenta
        food = Food()   #se genereaza alta mancare

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over() #se genereaza un sfarsit de joc

    else:
        window.after(SPEED_GAME, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    #se verifica ce tasta a fost apasata si se conditioneaza sa nu fie o miscare de 180 de grade
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction   #se modifica directia cu cea noua
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= BOARD_WIDTH:   #se verifica daca sarpele depaseste limitele orizontale
        return True
    elif y < 0 or y >= BOARD_HEIGHT:    #se verifica daca sarpele depaseste limitele verticale
        return True
    for body_part in snake.coordinates[1:]: #se verifica daca sarpele se atinge
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")

#se creaza fereastra de lucru
window = Tk()
window.title("Snake game- FRAM")
window.resizable(False, False)

score = 0   #vom defini score initial cu valoarea 0
direction = 'down'  #vom defini initial directia in jos

#vom crea o eticheta de score care sa il afiseze
label = Label(window, text=f"Score:{score}", font=('calibri', 40))
label.pack()

#definim dimensiunile ferestrei
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=BOARD_HEIGHT, width=BOARD_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#ajustam cat va fi pozitia ferestrei de joc din fereastra de lucru
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#vom crea legatura intre comenzile de la tastatura si pozitia sarpelui
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
