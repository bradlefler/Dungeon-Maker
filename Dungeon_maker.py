from tkinter import *
import xper
import grid

window = Tk()
photo = PhotoImage(file = "resources/icon.png")
window.iconphoto(False, photo)
w = 450
h = 300
text_displacement = 150
spin_displacement = 50
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.title("Dungeon Builder")

level_select_text = Label(window, text="What level are your players?")
level_select_text.place(x = w/2 - text_displacement, y = 50)
level_spin = Spinbox(window, from_=1, to=20, width=5)
level_spin.place(x = w/2 + spin_displacement, y = 50)

player_amount_text = Label(window, text="How many players are there?")
player_amount_text.place(x = w/2 - text_displacement, y = 100)
player_spin = Spinbox(window, from_=1, to=10, width=5)
player_spin.place(x = w/2 + spin_displacement, y = 100)

options = [
    "Abyssal",
    "Beast",
    "Classic",
    "Elemental",
    "Fey",
    "Infernal",
    "Monstrous",
    "Undead",
    "Random"
]

start = StringVar()
start.set("Random")
monster_type_text = Label(window, text="Pick a monster type:")
monster_type_text.place(x = w/2 - text_displacement, y = 150)
monster_drop = OptionMenu(window, start, *options)
monster_drop.place(x = w/2 + spin_displacement - 60, y = 145)

def clicked_submit():
    thresh_list = xper.experience_threshold(int(player_spin.get()), int(level_spin.get()))
    grid.create_grid(thresh_list, start.get())
    window.destroy()

def clicked_quit():
    window.destroy()

btn = Button(window, text="Submit", command=clicked_submit)
btn2 = Button(window, text="Quit", command=clicked_quit)
btn.place(x = w/2 + 30, y=225)
btn2.place(x = w/2 - 70, y=225)



window.mainloop()
