from parse_logs import round_input
from turtle import Screen, Turtle
from tkinter import *
import time

SQUARE_STRETCH =  0.5
SQUARE_SIZE = 20 * SQUARE_STRETCH
START = (-350, 350)
segments = None

def init_game_field(round_input, height, width):
    game_field = round_input['game_field_with_tracing']
    debug_data = round_input['debug_data']
    round_input_data = round_input['round_input']
    round_output_data = round_input['output_data']

    global segments
    segments = [list("."*width) for _ in range(height)]
    

    for i in range(height+1):
        turtle_horizontal = Turtle()
        turtle_horizontal.hideturtle()
        turtle_horizontal.penup()
        turtle_horizontal.color("red")
        turtle_horizontal.goto(START[0] - SQUARE_SIZE / 2, START[1] + SQUARE_SIZE / 2 + 1 - i * (SQUARE_SIZE + 2))
        turtle_horizontal.pendown()
        turtle_horizontal.forward(width * (SQUARE_SIZE + 2))

    for i in range(width+1):
        turtle_vertical = Turtle()
        turtle_vertical.hideturtle()
        turtle_vertical.penup()
        turtle_vertical.color("red")
        turtle_vertical.goto(START[0] - SQUARE_SIZE / 2 + i * (SQUARE_SIZE + 2) - 1, START[1] + SQUARE_SIZE / 2)
        turtle_vertical.pendown()
        turtle_vertical.right(90)
        turtle_vertical.forward(height * (SQUARE_SIZE + 2))

    for i in range(height):
        for j in range(width):
            segment = Turtle("square")
            segment.penup()
            segment.shapesize(stretch_len=SQUARE_STRETCH, stretch_wid=SQUARE_STRETCH)
            if game_field[i][j] == '.':
                segment.color("yellow")
            elif game_field[i][j] == 'P':
                segment.color("green")
            elif game_field[i][j] == 'E':
                segment.color("red")
            elif game_field[i][j] == 'V':
                segment.color("cyan")
            else:
                segment.color("black")
            segment.goto((START[0] + j * (SQUARE_SIZE + 2), START[1] - i * (SQUARE_SIZE + 2)))
            segments[i][j] = segment

    text_field.delete('1.0', END)
    text_field.insert(END, debug_data)
    round_data_label_text.set(round_input_data)
    output_data_label_text.set(round_output_data)

    screen.update()


def update_game_field(game_field, height, width):
    for i in range(height):
        for j in range(width):
            segment = segments[i][j]
            if game_field[i][j] == '.':
                segment.color("yellow")
            elif game_field[i][j] == 'P':
                segment.color("green")
            elif game_field[i][j] == 'E':
                segment.color("red")
            elif game_field[i][j] == 'V':
                segment.color("cyan")
            else:
                segment.color("black")

    screen.update()
            

def play():
    round_input.reset_counter()
    
    try:
        play_button["state"] = DISABLED
        
        while True:
            
            if with_tracing.get():
                update_game_field(round_input.get_next()['game_field_with_tracing'], round_input.height, round_input.width)
            else:
                update_game_field(round_input.get_next()['game_field_without_tracing'], round_input.height, round_input.width)
            text_field.delete('1.0', END)
            text_field.insert(END, round_input.get_current()['debug_data'])
            round_data_label_text.set(round_input.get_current()['round_input'])
            output_data_label_text.set(round_input.get_current()['output_data'])
    except StopIteration:
        play_button["state"] = NORMAL
        pass


def step_forward():
    try:
        if with_tracing.get():
            update_game_field(round_input.get_next()['game_field_with_tracing'], round_input.height, round_input.width)
        else:
            update_game_field(round_input.get_next()['game_field_without_tracing'], round_input.height, round_input.width)
        text_field.delete('1.0', END)
        text_field.insert(END, round_input.get_current()['debug_data'])
        round_data_label_text.set(round_input.get_current()['round_input'])
        output_data_label_text.set(round_input.get_current()['output_data'])
        step_backward_button["state"] = NORMAL
    except StopIteration:
        step_forward_button["state"] = DISABLED


def step_backward():
    try:
        if with_tracing.get():
            update_game_field(round_input.get_previous()['game_field_with_tracing'], round_input.height, round_input.width)
        else:
            update_game_field(round_input.get_previous()['game_field_without_tracing'], round_input.height, round_input.width)
        text_field.delete('1.0', END)
        text_field.insert(END, round_input.get_current()['debug_data'])
        round_data_label_text.set(round_input.get_current()['round_input'])
        output_data_label_text.set(round_input.get_current()['output_data'])
        step_forward_button["state"] = NORMAL
    except StopIteration:
        step_backward_button["state"] = DISABLED


screen = Screen()
screen.tracer(0)
screen.setup(width=800, height=800)

canvas = screen.getcanvas()

slider = Scale(canvas.master, from_=0, to=42, length=300, orient=HORIZONTAL)
slider.pack()
slider.place(x=50, y=420)

with_tracing = IntVar()
check_box = Checkbutton(canvas.master, text='with tracing',variable=with_tracing, onvalue=1, offvalue=0)
check_box.pack()
check_box.place(x=500, y=470)

round_data_label_text = StringVar()
round_data_label = Label(canvas.master, textvariable=round_data_label_text, relief=RAISED)
round_data_label.pack()
round_data_label.place(x=50, y=400)

output_data_label_text = StringVar()
output_data_label = Label(canvas.master, textvariable=output_data_label_text, relief=RAISED)
output_data_label.pack()
output_data_label.place(x=100, y=400)


play_button = Button(canvas.master, text="Play", fg="black", bg="white", command=play)
play_button.pack()
play_button.place(x=95, y=470)

step_forward_button = Button(canvas.master, text=">", fg="black", bg="white", command=step_forward)
step_forward_button.pack()
step_forward_button.place(x=150, y=470)

step_backward_button = Button(canvas.master, text="<", fg="black", bg="white", command=step_backward)
step_backward_button.pack()
step_backward_button.place(x=50, y=470)

text_field = Text(canvas.master, height = 15, width = 80)
text_field.place(x=50, y=530)
text_field.insert(END,"text")

# init
init_game_field(round_input.get_current(), round_input.height, round_input.width)




screen.exitonclick()
