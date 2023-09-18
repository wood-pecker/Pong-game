from tkinter import *
import random
import time
import pickle

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = self.canvas.create_oval(10,10,25,25, fill=color)
        self.canvas.move(self.id, 250,100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def puddle_crush(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    #Функция gamescore отображает текущий счет игры
    score=0
    def gamescore(self):
        self.score = self.score + 1
        canvas.itemconfig(s, text=self.score)
    
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.puddle_crush(pos) == True:
            self.y = -3
            self.gamescore()
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

    ansver = 2
    def bestgamescore(self):
        load_file = open('c:\\programming\\Pong\\best_score.dat', 'rb')
        loaded_game_data = pickle.load(load_file)
        if self.score > loaded_game_data:
            self.ansver = 1
        else:
            self.ansver = 0
        load_file.close()
    
    def gameover(self):
        canvas.itemconfig(self.id, state='hidden')
        canvas.itemconfig(self.paddle.id, state='hidden')
        canvas.create_rectangle(0,0,500,400, fill='black')
        canvas.create_text(250,170, text='GAME', fill='white', font=('Helvetica', 50))
        canvas.create_text(250,214, text='OVER', fill='white', font=('Helvetica', 35))
        
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,100,10, fill=color)
        self.canvas.move(self.id,200,300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

tk = Tk()
tk.title("Pong")
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
canvas.update()

#задержка перед началом игры(обратный отсчет)
sleeping=canvas.create_text(250,200, text='3', font=('Helvetica', 50), fill='red')
canvas.update()
time.sleep(1)
canvas.itemconfig(sleeping, text='2')
canvas.update()
time.sleep(1)
canvas.itemconfig(sleeping, text='1')
canvas.update()
time.sleep(1)
canvas.itemconfig(sleeping, state='hidden')

#задний фон(background)
background = PhotoImage(file='c:\\programming\\Pong\\background.gif')
canvas.create_image(0, 0, anchor=NW, image=background)

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')

canvas.create_text(450,10, text='Your score:', fill='red')
s=canvas.create_text(490,10, text=ball.score, fill='red')

while 1:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    else:
        time.sleep(2)
        ball.bestgamescore()
        if ball.ansver == 1:
            recordsaving = open('c:\\programming\\Pong\\best_score.dat', 'wb')
            pickle.dump(ball.score, recordsaving)
            recordsaving.close()
            canvas.create_rectangle(0,0,500,400, fill='#74a5cd')
            canvas.create_text(250,165, text='New Best', fill='yellow', font=('Times',50))
            canvas.create_text(250,220, text=ball.score, fill='red', font=('Times',38))
        else:
            ball.gameover()
            canvas.create_text(255, 350, text='Your score: %s' % ball.score, fill='white', font=('Helvetica',14))

        tk.update()
        time.sleep(3)
        break
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
