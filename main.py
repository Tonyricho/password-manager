from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for char in range(randint(8, 10))]
    password_symbols = [choice(symbols) for sym in range(randint(2, 4))]
    password_numbers = [choice(numbers) for num in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters

    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.delete(0, 'end')
    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = web_entry.get().lower()
    user = user_entry.get()
    password = pass_entry.get()
    new_data = {
        web: {
            "email": user,
            "password": password,
        }
    }

    if len(web) == 0 or len(password) == 0:
        messagebox.showinfo(title="Incomplete", message="Please fill all fields")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            web_entry.delete(0, 'end')
            user_entry.delete(0, 'end')
            user_entry.insert(0, "email@email.com")
            pass_entry.delete(0, 'end')


# -----------------------------Search password ------------------------- #
def search_data():
    web = web_entry.get().lower()
    try:
        with open("data.json", "r") as data_file:
            raw_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    if web in raw_data:
        email = raw_data[web]["email"]
        password = raw_data[web]["password"]
        messagebox.showinfo(title=f"{web.capitalize()}", message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Invalid", message=f"No details for {web}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
web_label = Label(text="Website:")
web_label.grid(column=0, row=1)

user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)

pass_label = Label(text="Password:")
pass_label.grid(column=0, row=3)

# Entries
web_entry = Entry(width=21)
web_entry.grid(column=1, row=1)
web_entry.focus()

user_entry = Entry(width=40)
user_entry.grid(column=1, row=2, columnspan=2)
user_entry.insert(0, "email@email.com")

pass_entry = Entry(width=21)
pass_entry.grid(column=1, row=3)

# Buttons
pass_button = Button(text="Generate Password", command=generate_password)
pass_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=search_data)
search_button.grid(column=2, row=1)

window.mainloop()
