# 1536x864
# Basic settings:
# move with arrows, press spacebar to pause the game
# press return to enter cheat codes(SHRINK1, SHRINK3 OR SHRINK5)

from tkinter import *
import random
import sys


def growSnake():
    lastElement = len(snake) - 1
    lastElementPos = canvas.coords(snake[lastElement])
    snake.append(canvas.create_rectangle(0, 0, snakeSize, snakeSize,
                 fill="#FDF3F3"))
    if direction == "left":
        canvas.coords(snake[lastElement+1], lastElementPos[0]+snakeSize,
                      lastElementPos[1], lastElementPos[2]+snakeSize,
                      lastElementPos[3])
    elif (direction == "right"):
        canvas.coords(snake[lastElement+1], lastElementPos[0] -
                      snakeSize, lastElementPos[1], lastElementPos[2] -
                      snakeSize, lastElementPos[3])
    elif (direction == "up"):
        canvas.coords(snake[lastElement+1], lastElementPos[0],
                      lastElementPos[1]+snakeSize, lastElementPos[2],
                      lastElementPos[3]+snakeSize)
    else:
        canvas.coords(snake[lastElement+1], lastElementPos[0],
                      lastElementPos[1]-snakeSize, lastElementPos[2],
                      lastElementPos[3]-snakeSize)
    global score
    score += 1
    txt = "Score: " + str(int(score))
    canvas.itemconfigure(scoreText, text=txt)


def moveFood():
    global food, foodX, foodY
    canvas.move(food, (foodX*(-1)), (foodY*(-1)))
    foodX = random.randint(0, width-snakeSize)
    foodY = random.randint(0, height-snakeSize)
    canvas.move(food, foodX, foodY)


def overlapping(a, b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False


def storeLeaderboard():
    """updates the leaderboard"""
    global username_entry, leaderboard_scores, leaderboard_names, button
    username = username_entry.get()
    copy_leaderboard_scores = leaderboard_scores.copy()
    copy_leaderboard_names = leaderboard_names.copy()
    for i in range(5):
        if (score > int(leaderboard_scores[i])):
            for x in range(i, 4):
                leaderboard_scores[x+1] = copy_leaderboard_scores[x]
                leaderboard_names[x+1] = copy_leaderboard_names[x]
            leaderboard_scores[i] = score
            leaderboard_names[i] = username
            break
    button.destroy()


def topScore():
    """gets a name from the user and passes it onto storeLeaderboard"""
    enter_name_window = setWindowDimensions(width, height, "Enter name")
    username_label = Label(enter_name_window, text="Enter your name: ",
                           bg="black", fg="white", font="Times 20 italic bold",
                           pady=15).pack()
    global username_entry, button
    username_entry = Entry(enter_name_window, bg="black", fg="white",
                           font="Times 20 italic bold")
    username_entry.pack()
    username_entry.focus_set()
    button = Button(enter_name_window, bg="black", fg="white", text="ENTER",
                    font="Times 20 italic bold", command=storeLeaderboard)
    button.pack()
    game_over_label = Label(enter_name_window, text="GAME OVER", fg="white",
                            font="Times 24 italic bold", bg="black",
                            pady=15).pack()
    enter_name_window.wait_window(button)
    enter_name_window.destroy()
    window.focus_set()


def gameOver():
    """when the game is over it checks whether the score is in the top 5"""
    canvas.create_text(width/2, height/2, fill="white",
                       font="Times 36 italic bold", text="Game Over")
    game_over = True
    global leaderboard_scores, leaderboard_names
    top_score = False
    for i in range(5):
        if (score > int(leaderboard_scores[i])):
            top_score = True
            topScore()
            break
    if not top_score:
        game_over_window = setWindowDimensions(width, height, "Game over")
        Label(game_over_window, text="GAME OVER", fg="white",
              font="Times 26 italic bold", bg="black", pady=15).pack()
        button = Button(game_over_window, bg="black", fg="white",
                        text="BACK TO MENU", font="Times 30 italic bold",
                        width=15, height=3, bd=7,
                        command=game_over_window.destroy).pack()
        game_over_window.wait_window(button)
    file = open("leaderboard.txt", "w")
    for i in range(5):
        file.write(str(leaderboard_scores[i]) + "," +
                   leaderboard_names[i] + "\n")
    file.close()
    return game_over


def moveSnake():
    global positions
    if not paused:
        canvas.delete("paused_text")
        canvas.pack()
        positions = []
        positions.append(canvas.coords(snake[0]))
        if positions[0][0] < 0:
            canvas.coords(snake[0], width, positions[0][1],
                          width-snakeSize, positions[0][3])
        elif positions[0][2] > width:
            canvas.coords(snake[0], 0-snakeSize, positions[0][1],
                          0, positions[0][3])
        elif positions[0][3] > height:
            canvas.coords(snake[0], positions[0][0],
                          0-snakeSize, positions[0][2], 0)
        elif positions[0][1] < 0:
            canvas.coords(snake[0], positions[0][0], height,
                          positions[0][2], height-snakeSize)
        positions.clear()
        positions.append(canvas.coords(snake[0]))
        if direction == "left":
            canvas.move(snake[0], -snakeSize, 0)
        elif direction == "right":
            canvas.move(snake[0], snakeSize, 0)
        elif direction == "up":
            canvas.move(snake[0], 0, -snakeSize)
        elif direction == "down":
            canvas.move(snake[0], 0, snakeSize)
        sHeadPos = canvas.coords(snake[0])
        foodPos = canvas.coords(food)
        if overlapping(sHeadPos, foodPos):
            moveFood()
            growSnake()
        for i in range(1, len(snake)):
            positions.append(canvas.coords(snake[i]))
        for i in range(len(snake) - 1):
            canvas.coords(snake[i+1], positions[i][0], positions[i][1],
                          positions[i][2], positions[i][3])
        for i in range(1, len(snake)):
            if overlapping(sHeadPos, canvas.coords(snake[i])):
                game_over = gameOver()
                canvas.destroy()
                menu()
                break
    else:
        canvas.create_text(width/2, height/2, fill="white",
                           font="Times 28 italic bold", text="Game Paused",
                           tag="paused_text")
        canvas.create_text(85, 35, fill="white", font="Times 20 italic bold",
                           text="Leaderboard:\n", tag="paused_text")
        for i in range(5):
            leaderboard_text = str(leaderboard_scores[i]) + "\t"
            leaderboard_text += leaderboard_names[i] + "\n"
            canvas.create_text(15, i*25+30, fill="white", font="Times 20 bold",
                               text=leaderboard_text, tag="paused_text",
                               anchor=NW)
    if 'game_over' not in locals():
        window.after(90, moveSnake)


def placeFood():
    global food, foodX, foodY
    food = canvas.create_rectangle(0, 0, snakeSize, snakeSize, fill="#0DE33F")
    foodX = random.randint(0, width-snakeSize)
    foodY = random.randint(0, height-snakeSize)
    canvas.move(food, foodX, foodY)


def menu():
    global canvas, scoreText, snake, score
    canvas = Canvas(window, bg="black", width=width, height=height)
    snake = []
    score = 0
    txt = "Score:" + str(score)
    canvas.bind("<Left>", leftKey)
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.bind("<s>", saveGame)
    canvas.bind("<space>", pauseGame)
    canvas.bind("<b>", bossKey)
    canvas.bind("<Return>", cheatCodes)
    canvas.focus_set()
    snake.append(canvas.create_rectangle(snakeSize, snakeSize, snakeSize * 2,
                 snakeSize * 2, fill="white"))
    scoreText = canvas.create_text(width/2, 10, fill="white",
                                   font="Times 20 italic bold", text=txt)

    start_game_button = Button(window, fg="white", bg="black",
                               text="START GAME",
                               font="Times 24 bold", width=15, height=3, bd=5,
                               command=lambda: [startGame(),
                                                load_game_button.destroy(),
                                                settings_button.destroy(),
                                                start_game_button.destroy(),
                                                leaderboard_button.destroy(),
                                                exit_button.destroy()])
    start_game_button.pack()
    load_game_button = Button(window, fg="white", bg="black", text="LOAD GAME",
                              font="Times 24 bold", width=15, height=3, bd=5,
                              command=lambda: [loadGame(),
                                               load_game_button.destroy(),
                                               settings_button.destroy(),
                                               start_game_button.destroy(),
                                               leaderboard_button.destroy(),
                                               exit_button.destroy()])
    load_game_button.pack()
    leaderboard_button = Button(window, fg="white", bg="black",
                                text="LEADERBOARD",
                                font="Times 24 bold", width=15, height=3, bd=5,
                                command=leaderboard)
    leaderboard_button.pack()
    settings_button = Button(window, fg="white", bg="black", text="SETTINGS",
                             font="Times 24 bold", width=15, height=3, bd=5,
                             command=settings)
    settings_button.pack()
    exit_button = Button(window, fg="white", bg="black", text="EXIT GAME",
                         font="Times 24 bold", width=15, height=3, bd=5,
                         command=sys.exit)
    exit_button.pack()


def startGame():
    placeFood()
    moveSnake()


def loadGame():
    """loads a saved game and starts it"""
    global snake, positions, score
    file = open("savegame.txt", "r")
    score = int(file.readline().strip())
    file.close()
    for i in range(score):
        growSnake()
    score = score / 2
    print(score)
    startGame()


def leaderboard():
    """shows the leaderboard"""
    leaderboard_window = setWindowDimensions(width, height, "Leaderboard")
    Label(leaderboard_window, fg="white", bg="black", text="Leaderboard:",
          font="Times 32 bold", pady=10).pack()
    for i in range(5):
        leaderboard_text = str(leaderboard_scores[i]) + "\t"
        leaderboard_text += leaderboard_names[i] + "\n"
        Label(leaderboard_window, fg="white", bg="black",
              text=leaderboard_text, font="Times 24 bold").pack()
    Button(leaderboard_window, fg="white", bg="black", text="BACK",
           font="Times 32 bold", width=10, height=4, bd=10,
           command=leaderboard_window.destroy).pack()


def settings():
    """change the bindings of the keys"""
    settings_window = setWindowDimensions(width, height, "Settings")
    Label(settings_window, fg="white", bg="black", text="Change key settings",
          font="Times 32 bold", pady=20).grid(row=0, column=1)
    Button(settings_window, fg="white", bg="black", text="MOVE LEFT",
           font="Times 24 bold", width=12, height=1, bd=5,
           command=setLeftKey).grid(row=1, column=0)
    Button(settings_window, fg="white", bg="black", text="MOVE RIGHT",
           font="Times 24 bold", width=12, height=1, bd=5,
           command=setRightKey).grid(row=2, column=0)
    Button(settings_window, fg="white", bg="black", text="MOVE DOWN",
           font="Times 24 bold", width=12, height=1, bd=5,
           command=setDownKey).grid(row=3, column=0)
    Button(settings_window, fg="white", bg="black", text="MOVE UP",
           font="Times 24 bold", width=12, height=1, bd=5,
           command=setUpKey).grid(row=4, column=0)
    Button(settings_window, fg="white", bg="black", text="PAUSE",
           font="Times 24 bold", width=12, height=1, bd=5,
           command=setPauseKey).grid(row=5, column=0)
    Button(settings_window, fg="white", bg="black", text="SAVE",
           font="Times 24 bold", width=12, height=1, bd=5,
           command=setSaveKey).grid(row=6, column=0)
    Button(settings_window, fg="white", bg="black", text="BOSS KEY",
           font="Times 24 bold", width=12, height=1, bd=5,
           command=setBossKey).grid(row=7, column=0)
    Button(settings_window, fg="white", bg="black", text="BACK",
           font="Times 28 bold", width=10, height=2, bd=8,
           command=settings_window.destroy).grid(row=8, column=1)


def getKey():
    get_key_window = setWindowDimensions(width, height, "Get key")
    Label(get_key_window, fg="white", bg="black",
          text="Please press the chosen character and press DONE",
          font="Times 24 bold", pady=20).pack()
    which_key = Entry(get_key_window, bg="black", fg="white",
                      font="Times 20 italic bold")
    which_key.pack()
    which_key.focus_set()
    get_input_button = Button(get_key_window, bg="black", fg="white",
                              text="DONE", font="Times 28 italic bold",
                              width=10, height=3, bd=8,
                              command=lambda: [get_input_button.destroy()])
    get_input_button.pack()
    get_key_window.wait_window(get_input_button)
    which_key_get = which_key.get()
    get_key_window.destroy()
    return which_key_get


def setLeftKey():
    which_key = getKey()
    canvas.unbind("<Left>")
    canvas.bind(which_key, leftKey)


def setRightKey():
    which_key = getKey()
    canvas.unbind("<Right>")
    canvas.bind(which_key, rightKey)


def setDownKey():
    which_key = getKey()
    canvas.unbind("<Down>")
    canvas.bind(which_key, downKey)


def setUpKey():
    which_key = getKey()
    canvas.unbind("<Up>")
    canvas.bind(which_key, upKey)


def setPauseKey():
    which_key = getKey()
    canvas.unbind("<space>")
    canvas.bind(which_key, pauseGame)


def setSaveKey():
    which_key = getKey()
    canvas.unbind("<s>")
    canvas.bind(which_key, saveGame)


def setBossKey():
    which_key = getKey()
    canvas.unbind("<b>")
    canvas.bind(which_key, bossKey)


def pauseGame(event):
    global paused
    if not paused:
        paused = True
    else:
        paused = False


def bossKey(event):
    """switches to an excel image when pressed"""
    global paused, boss_key_on, boss_key_window
    if not boss_key_on:
        boss_key_photo = PhotoImage(file="boss_key.gif")
        boss_key_window = Toplevel()
        label = Label(master=boss_key_window, image=boss_key_photo)
        label.image = boss_key_photo  # screenshot
        label.pack()
        boss_key_on = True
        paused = True
        boss_key_window.wait_window()
    else:
        boss_key_on = False
        boss_key_window.destroy()


def saveGame(event):
    file = open("savegame.txt", "w")
    print(score)
    file.write(str(score))
    file.close()


def leftKey(event):
    global direction
    direction = "left"


def rightKey(event):
    global direction
    direction = "right"


def upKey(event):
    global direction
    direction = "up"


def downKey(event):
    global direction
    direction = "down"


def cheatCodes(event):
    """shrinks the snake if the correct code was entered"""
    global paused, snake, canvas
    paused = True
    cheat_codes_window = setWindowDimensions(width, height,
                                             "Enter Cheat Code")
    cheat_code_entered = Entry(cheat_codes_window, bg="black",
                               fg="white", font="Times 20 italic bold")
    cheat_code_entered.pack()
    cheat_code_entered.focus_set()
    enter_button = Button(cheat_codes_window, fg="white", bg="black",
                          text="ENTER", font="Times 28 bold",
                          width=12, height=1, bd=7,
                          command=lambda: [enter_button.destroy()])
    enter_button.pack()
    cheat_codes_window.wait_window(enter_button)
    cheat_code = cheat_code_entered.get()
    if(cheat_code == "SHRINK1"):
        canvas.delete(snake[-1])
        del snake[-1]
    elif(cheat_code == "SHRINK3"):
        canvas.delete(snake[-1])
        del snake[-1]
        canvas.delete(snake[-1])
        del snake[-1]
        canvas.delete(snake[-1])
        del snake[-1]
    elif(cheat_code == "SHRINK5"):
        for i in range(5):
            canvas.delete(snake[-1])
            del snake[-1]
    cheat_codes_window.destroy()


def setWindowDimensions(w, h, title):
    window = Tk()
    window.title(title)
    window.config(bg="black")
    window.geometry('%dx%d+%d+%d' % (w, h, 0, 0))
    return window

width = 700
height = 700

window = setWindowDimensions(width, height, "Snake game")
snakeSize = 15

try:
    file = open("leaderboard.txt", "r")
except:
    leaderboard_scores = [0, 0, 0, 0, 0]
    print("leaderboard file did not exist yet")
    leaderboard_names = ["", "", "", "", ""]
else:
    leaderboard_names = ["", "", "", "", ""]
    leaderboard_scores = [0, 0, 0, 0, 0]
    for i in range(5):
        line = file.readline()
        splitted_line = line.split(",")
        leaderboard_scores[i] = splitted_line[0]
        leaderboard_names[i] = splitted_line[1].strip()
    file.close()

paused = False
boss_key_on = False

direction = "right"

menu()

window.mainloop()