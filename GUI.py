from tkinter import *
import tkinter as tk
import urllib.request
import io
from PIL import ImageTk, Image

#Variable to hold user values
#Variable to hold user values
list_of_users = []
num_books = []

window = tk.Tk()
window.geometry("1000x600")

link = "https://knowledgequest.aasl.org/wp-content/uploads/2019/05/GoodReads-logo.jpg"

class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        #self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image

img = WebImage(link).get()

#add image to top center
label_img= Label(window, image=img, width=270)
label_img.grid(row = 0, column = 0, columnspan = 4)

#add title below image
topLabel = Label(window, text = "GoodReads Book Recommender System", font = 'Helvetica 18 bold', width=65)
topLabel.grid(row = 1, column = 0, columnspan = 4)

#label for returning user
RetUserLabel = Label(window, text = "\n\nReturning User", font = 'Helvetica 12 bold')
RetUserLabel.grid(row = 5, column = 0)
#enter userID text
RetUserEnter = Label(window, text = "\t\t\tEnter Returning UserID", font = 'Helvetica 10')
RetUserEnter.grid(row = 6, column = 0)
#place to enter the ID
RetUserID = Entry(window, width = 20, borderwidth = 6, font = 'Helvetica 12')
RetUserID.grid(row = 6, column = 0, columnspan=4)

#label for new user
NewUserLabel = Label(window, text = "\nNew User", font = 'Helvetica 12 bold')
NewUserLabel.grid(row = 8, column = 0)
#enter userID text
NewUserEnter = Label(window, text = "\t\t\tEnter a New UserID", font = 'Helvetica 10')
NewUserEnter.grid(row = 9, column = 0)
#place to enter the ID
NewUserID = Entry(window, width = 20, borderwidth = 6, font = 'Helvetica 12')
NewUserID.grid(row = 9, column = 0, columnspan=4)

#label for new user
NumberBooksLabel = Label(window, text = "\n\tNo. of Books to Recommend", font = 'Helvetica 12 bold')
NumberBooksLabel.grid(row = 11, column = 0)
#label for number of books
NumBookEnter = Label(window, text = "\t\t\tEnter Number of Books", font = 'Helvetica 10')
NumBookEnter.grid(row = 12, column = 0)
#place to enter the ID
NumBooks = Entry(window, width = 20, borderwidth = 6, font = 'Helvetica 12')
NumBooks.grid(row = 12, column = 0, columnspan=4)

# Button Logic
def RetUserOnClick():
    inputval1 = RetUserID.get()
    list_of_users.append(int(inputval1))
    RetUserID.delete(0, END)
    
def NewUserOnClick():
    inputval1 = NewUserID.get()
    list_of_users.append(int(inputval1))
    NewUserID.delete(0, END)

def numBooks():
    inputval1 = NumBooks.get()
    num_books.append(int(inputval1))
    NumBooks.delete(0, END)

# Buttons
Button(window, text = "Enter", font = 'Helvetica 10 bold', command = RetUserOnClick).grid(row = 6, column = 1, sticky = E)
Button(window, text = "Enter", font = 'Helvetica 10 bold', command = NewUserOnClick).grid(row = 9, column = 1, sticky = E)
Button(window, text = "Enter", font = 'Helvetica 10 bold', command = numBooks).grid(row = 12, column = 1, sticky = E)

window.mainloop()

#list_of_users
#num_books