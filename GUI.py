from tkinter import *
import tkinter as tk
from tkinter import messagebox
import urllib.request
import io
from PIL import ImageTk, Image

#count number of times the a user id/number of books entered correctly
correct_entries = []

total = 0

def sum_of_entries(l):
    global total
    total = 0
    for val in l:
        total = total + val
    return(total)

class WebImage():
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        #self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image

class FirstWindow():
    #Create the tkinter object called window
    global window
    window = tk.Tk()
    #call the window the title below
    window.title('GoodReadsBookRecommender')
    #provide the window dimensions
    window.geometry("1000x600")

    #this is the link to the image that is used in the window
    link = "https://knowledgequest.aasl.org/wp-content/uploads/2019/05/GoodReads-logo.jpg"

    #call above class to get the image correctly to put on the window
    img = WebImage(link).get()

    #START ADDING COMPONENTS TO THE WINDOW!
    #add image to top center
    label_img= Label(window, image=img, width=270)
    label_img.grid(row = 0, column = 0, columnspan = 4)

    #add title below image
    topLabel = Label(window, text = "GoodReads Book Recommender System", font = 'Helvetica 18 bold', width=65)
    topLabel.grid(row = 1, column = 0, columnspan = 4)
    
    #GET RETURNING USER ID
    #label for returning user
    lab_ret_user = Label(window, text = "\n\nReturning User", font = 'Helvetica 12 bold')
    lab_ret_user.grid(row = 5, column = 0)
    #Label to describe what to enter
    lab_ret_id_ent = Label(window, text = "\t\t\tEnter Returning User ID", font = 'Helvetica 10')
    lab_ret_id_ent.grid(row = 6, column = 0)
    #Place to enter the returning user id
    global ret_id_entry
    ret_id_entry = Entry(window, width = 20, borderwidth = 6, font = 'Helvetica 12')
    ret_id_entry.grid(row = 6, column = 0, columnspan=4)
    # Button Logic when press enter
    def ret_user_button():
        global user_id
        #get the entered returning user id
        user_id = ret_id_entry.get()
        #check if entry is a digit
        if not user_id.isdigit():
            messagebox.showerror(title = 'Python Error', message = "Error: Entered User ID is not a number.\nTry again.")
            user_id = ""
            ret_id_entry.delete(0, END)
            return()
        #check if entered user id is too large
        elif(int(user_id) > 567806):
            messagebox.showerror(title = 'Python Error', message = 'Error: The provided User ID does not exist!\nPlease enter a value smaller than 567806.')
            user_id = ""
            ret_id_entry.delete(0, END)
            return()
        #check if new user id was already entered
        elif(new_id_entry.index("end") != 0):
            messagebox.showerror(title = 'Python Error', message = "Error: A new user ID was entered.\nCannot get recommendations for both a new user and a returning user.\n\nThe new user ID will be used.")
            user_id = ""
            ret_id_entry.delete(0, END)
            return()
        else:
            correct_entries.append(1)
            sum_of_entries(correct_entries) 
 
    #GET NEW USER ID
    #label for new user
    lab_new_user = Label(window, text = "\nNew User", font = 'Helvetica 12 bold')
    lab_new_user.grid(row = 8, column = 0)
    #enter userID text
    lab_new_id_ent = Label(window, text = "\t\t\tEnter a New User ID", font = 'Helvetica 10')
    lab_new_id_ent.grid(row = 9, column = 0)
    #place to enter the ID
    global new_id_entry
    new_id_entry = Entry(window, width = 20, borderwidth = 6, font = 'Helvetica 12')
    new_id_entry.grid(row = 9, column = 0, columnspan=4)
    #Button logic when push enter
    def new_user_button():
        global new_user_id
        new_user_id = new_id_entry.get()
        #check if entry is a digit
        if not new_user_id.isdigit():
            messagebox.showerror(title = 'Python Error', message = "Error: Entered User ID is not a number.\nTry again.")
            new_user_id = ""
            new_id_entry.delete(0, END)
            return()
        #Make sure new user id is big enough
        elif(int(new_user_id) < 567806):
            messagebox.showerror(title = 'Python Error', message = "Error: The provided User ID is already in use!\nPlease enter a value larger than 567806.")
            new_user_id = ""
            new_id_entry.delete(0, END)
            return()
        #Check if a returning user was previously entered
        elif(ret_id_entry.index("end") != 0):
            messagebox.showerror(title = 'Python Error', message = "Error: A returing user ID was entered.\nCannot get recommendations for both a new user and a returning user.\n\nThe returning user ID will be used.")
            new_user_id = ""
            new_id_entry.delete(0, END)
            return()
        else:
            correct_entries.append(1)
            sum_of_entries(correct_entries) 
   
    #GET NUMBER OF BOOKS TO RECOMMEND
    #label for new user
    lab_book_rec = Label(window, text = "\n\tNo. of Books to Recommend", font = 'Helvetica 12 bold')
    lab_book_rec.grid(row = 11, column = 0)
    #label for number of books
    lab_num_books = Label(window, text = "\t\t\tEnter Number of Books", font = 'Helvetica 10')
    lab_num_books.grid(row = 12, column = 0)
    #place to enter the ID
    global num_books_entry
    num_books_entry = Entry(window, width = 20, borderwidth = 6, font = 'Helvetica 12')
    num_books_entry.grid(row = 12, column = 0, columnspan=4)
    #Button logic when press enter
    def num_books_button():
        global num_books
        num_books = num_books_entry.get()
        #check if entry is a digit
        if not num_books.isdigit():
            messagebox.showerror(title = 'Python Error', message = "Error: Entered number of books is not a number.\nTry again.")
            num_books = ""
            num_books_entry.delete(0, END)
            return()
        elif(int(num_books) > 10):
            messagebox.showwarning(title = 'Python Warning', message = 'Warning: The entered number of books to recommend is larger than 10.\nEnter a smaller number.')
            num_books = ""
            num_books_entry.delete(0, END)
            return()
        else:
            correct_entries.append(1)
            sum_of_entries(correct_entries)

    #space
    lab_space = Label(window, text = "\n\n\n\n", font = 'Helvetica 10')
    lab_space.grid(row = 12, column = 0)

    #create new window for listing recommendations
    def create():
        if(total < 2):
            messagebox.showerror(title = 'Python Error', message = 'Error: The user ID and number of books needs to be entered first. ')
        else:
            win = Toplevel(window)

    # Buttons
    Button(window, text = "Enter", font = 'Helvetica 10 bold', command = ret_user_button).grid(row = 6, column = 1, sticky = E)
    Button(window, text = "Enter", font = 'Helvetica 10 bold', command = new_user_button).grid(row = 9, column = 1, sticky = E)
    Button(window, text = "Enter", font = 'Helvetica 10 bold', command = num_books_button).grid(row = 12, column = 1, sticky = E)
    Button(window, text = "Click Here to Get Book Recommendations!", font = 'Helvetica 12 bold', command = create).grid(row = 15, column = 0, columnspan = 4)
        

    #this opens the window and keeps it open until someone closes the window
    window.mainloop()