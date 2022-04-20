from tkinter import *
import tkinter as tk

window = tk.Tk()
window.geometry("800x500")

# Top Title
topLabel = Label(window, justify = tk.CENTER, text = "GoodReads Book Recommender System", font = 'Helvetica 18 bold')
topLabel.grid(row = 0, column = 1)
space1 = Label(window, text = "")
space1.grid(row = 1, column = 0)

# Labels
#Label(window, text = "Test test").pack()
NewUserLabel = Label(window, text = "New User", font = 'Helvetica 12 bold')
NewUserLabel.grid(row = 3, column = 0)
NewUserEnter = Label(window, justify = tk.LEFT, text = "Enter New UserID", font = 'Helvetica 10')
NewUserEnter.grid(row = 5, column = 0)

# Whitespace
space2 = Label(window, text = "")
space2.grid(row = 6, column = 0)

RetUserLabel = Label(window, text = "Returning User", font = 'Helvetica 12 bold')
RetUserLabel.grid(row = 7, column = 0)
RetUserEnter = Label(window, text = "Enter Returning UserID", font = 'Helvetica 10')
RetUserEnter.grid(row = 8, column = 0)

# Text Input
NewUserID = Entry(window, width = 60, borderwidth= 5, font = 'Helvetica 12')
NewUserID.grid(row = 5, column = 1)
RetUserID = Entry(window, width = 60, borderwidth= 5, font = 'Helvetica 12')
RetUserID.grid(row = 8, column = 1)

# Button Logic
def NewUserOnClick():
    inputval1 = NewUserID.get()
    print(inputval1)

def RetUserOnClick():
    inputval1 = RetUserID.get()
    print(inputval1)

    



# Buttons
Button(window, text = "Enter", font = 'Helvetica 10 bold', command = NewUserOnClick).grid(row = 5, column = 3)
Button(window, text = "Enter", font = 'Helvetica 10 bold', command = RetUserOnClick).grid(row = 8, column = 3)


window.mainloop()

