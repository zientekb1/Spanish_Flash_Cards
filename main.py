from tkinter import *
from pandas import *
import random

current_card = {}

try:
    data = read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = read_csv("data/spanish to english.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(spanish_word, text=f"{current_card['Spanish']}", fill="black")
    canvas.itemconfig(canvas_image, image=front_card_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=back_card_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(spanish_word, text=f"{current_card['English']}", fill="white")


def know_word():
    to_learn.remove(current_card)
    data = DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Spanish Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

front_card_image = PhotoImage(file="images/card_front.png")
back_card_image = PhotoImage(file="images/card_back.png")
x_red_image = PhotoImage(file="images/wrong.png")
check_mark_image = PhotoImage(file="images/right.png")

canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=front_card_image)
canvas.grid(row=0, column=0, columnspan=2)

flip_timer = window.after(3000, flip_card)  # set timer for 3 seconds then execute flip card function

check_mark_button = Button(image=check_mark_image, highlightthickness=0, command=know_word)
check_mark_button.grid(row=1, column=1)
x_red_button = Button(image=x_red_image, highlightthickness=0, command=next_card)
x_red_button.grid(row=1, column=0)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
spanish_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

next_card()

window.mainloop()
