import math
import numpy as np
import numpy_indexed as npi 
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

from tkinter import *
import tkinter as tk
from tkinter import messagebox
import urllib.request
import io
from PIL import ImageTk, Image

# Read books data
books = pd.read_csv('red_books.csv')
# Read sparse matrix encoding into df
sparse_df = pd.read_csv('users_sparse.csv')

#gets n random books from the books with an average rating of 4.5 or higher
def getRand(num_rec):
    topBooks = books[books['avg_rating'] > 4.5]
    if num_rec > len(topBooks.avg_rating):
        num_rec = len(topBooks.avg_rating)
    randomIds = np.random.choice(np.array(topBooks.book_id),num_rec)
    return(randomIds)

# gets num_rec book recommendations for user_id
def getRec(user_id, num_rec):
    # Create Scipy sparse matrix and convert to compressed sparse row format for operations
    row = np.array(sparse_df.r_index)
    col = np.array(sparse_df.c_index)
    dat = np.array(sparse_df.data)
    users = coo_matrix((dat,(row,col)),shape=(np.unique(row).size,np.unique(col).size))
    users = users.tocsr()
    
    # Get number of users and calculate k
    n_users = np.unique(row).size
    k = math.ceil((math.sqrt(n_users))/2)

    # Calculate pairwise cosine similarities between current user and all other users
    similarities = cosine_similarity(users.getrow(user_id),users)

    # Get top k similar users that are not equal to 1
    sim_index = pd.DataFrame({'sim':similarities.flatten()})
    sim_index = sim_index.sort_values(['sim'])
    sim_index = sim_index[sim_index['sim'] < 1]
    nbrs = sim_index.iloc[-k:]
    nbrs = nbrs.reset_index()

    # Books read by the user_id
    user_books = np.array(sparse_df[sparse_df['r_index']==user_id].c_index)

    # Loop through each neighbor and find set difference between it and the user. Union the subsets.
    set_diff = np.empty(0,dtype=int)
    for ind in nbrs['index']:
        nbr_books = np.array(sparse_df[sparse_df['r_index']==ind].c_index)
        set_diff = np.union1d(set_diff,np.setdiff1d(nbr_books,user_books))

    # Get rows from users cooresponding to nbrs
    nbrs_books = users[nbrs['index']]

    # Get columns cooresponding to books read by neighbors but not user
    nbrs_books = nbrs_books[:,set_diff]

    # Convert to dataframe for ease of computation
    nbrs_books = pd.DataFrame.sparse.from_spmatrix(nbrs_books)
    nbrs_books = nbrs_books.set_axis(set_diff,axis=1)
    nbrs_books = nbrs_books.set_axis(np.array(nbrs['index']),axis=0)

    # Calculate weighted adjusted averages for each book
    weighted_adj_averages = np.empty(len(set_diff))
    i = 0
    for book in set_diff:
        curr_ratings = pd.DataFrame(nbrs_books[book])
        curr_ratings = curr_ratings[curr_ratings[book] != 0]
        curr_ratings['sim'] = np.array(nbrs[nbrs['index'].isin(curr_ratings.index)].sim)
        tot_sim = sum(curr_ratings.sim)
        curr_average = 0
        for rating, sim in zip(curr_ratings[book], curr_ratings['sim']):
            curr_average = curr_average + (sim/tot_sim) * rating
        curr_average = curr_average - 1/len(curr_ratings.index)
        weighted_adj_averages[i] = curr_average
        i += 1
    
    # Get top m rated books where m = num_rec
    book_scores = pd.DataFrame({'b_index':set_diff,'rating':weighted_adj_averages})
    top_m = book_scores.sort_values(by=['rating']).tail(num_rec)

    # Map between index and book ids
    book_ids = np.array(books.book_id)
    book_index = np.array(range(len(book_ids)))
    book_map = dict(zip(book_index,book_ids))    
    
    # Map to book ids
    rec_books = npi.remap(top_m.b_index, list(book_map.keys()), list(book_map.values())) 

    return(rec_books)

#EVERYTHING BELOW CREATES THE GUI
#count number of times the a user id/number of books entered correctly
correct_entries = []

#used to determine how many entires have been entered properly
    #if a user only enters a user Id but not the number of books to recommend an error message will be displayed
total = 0
def sum_of_entries(l):
    global total
    total = 0
    for val in l:
        total = total + val
    return(total)

#class used to get a image from an online source to use in the GUI
#https://stackoverflow.com/questions/65635835/displaying-image-from-url-in-python-tkinter
class WebImage():
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        #self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image

#class to create the first window that is displayed in the GUI
class FirstWindow():
    #https://www.youtube.com/watch?v=_PHJvjQJa3w
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
    global img
    img = WebImage(link).get()

    #START ADDING COMPONENTS TO THE WINDOW!
    #add image to top center
    label_img= Label(window, image=img, width=270)
    label_img.grid(row = 0, column = 0, columnspan = 4)

    #add title below image
    topLabel = Label(window, text = "Source: https://knowledgequest.aasl.org/wp-content/uploads/2019/05/GoodReads-logo.jpg", font = 'Helvetica 8', width=72)
    topLabel.grid(row = 1, column = 0, columnspan = 4)

    #add title below image
    topLabel = Label(window, text = "Goodreads Book Recommender System", font = 'Helvetica 18 bold', width=65)
    topLabel.grid(row = 3, column = 0, columnspan = 4)
    
    #GET RETURNING USER ID
    #label for returning user
    lab_ret_user = Label(window, text = "\n\nReturning User", font = 'Helvetica 12 bold')
    lab_ret_user.grid(row = 6, column = 0)
    #Label to describe what to enter
    lab_ret_id_ent = Label(window, text = "\t\t\tEnter Returning User ID", font = 'Helvetica 10')
    lab_ret_id_ent.grid(row = 7, column = 0)
    #Place to enter the returning user id
    global ret_id_entry
    ret_id_entry = Entry(window, width = 20, borderwidth = 6, font = 'Helvetica 12')
    ret_id_entry.grid(row = 7, column = 0, columnspan=4)
    # Button Logic when press enter
    def ret_user_button():
        #get the entered returning user id
        global user_id
        user_id = ret_id_entry.get()
        #check if entry is a digit
        if not user_id.isdigit():
            #messagebox displays a new window with the error message
            #https://docs.python.org/3/library/tkinter.messagebox.html
            messagebox.showerror(title = 'Python Error', message = "Error: Entered User ID is not a number.\nTry again.")
            user_id = ""
            #This deleted the user entry in the box once the button is clicked
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
        #the user Id has been entered correctly
        #add a 1 to the correct _entries list variable and sum up the values in that list
        #set new_user to False since a returning user id was entered
        else:
            correct_entries.append(1)
            sum_of_entries(correct_entries)
            ret_id_entry.delete(0, END)
            global new_user
            new_user = False

    #GET NEW USER ID
    #label for new user
    lab_new_user = Label(window, text = "\nNew User", font = 'Helvetica 12 bold')
    lab_new_user.grid(row = 9, column = 0)
    #enter userID text
    lab_new_id_ent = Label(window, text = "\t\t\tEnter a New User ID", font = 'Helvetica 10')
    lab_new_id_ent.grid(row = 10, column = 0)
    #place to enter the ID
    global new_id_entry
    new_id_entry = Entry(window, width = 20, borderwidth = 6, font = 'Helvetica 12')
    new_id_entry.grid(row = 10, column = 0, columnspan=4)
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
        #the user Id has been entered correctly
        #add a 1 to the correct _entries list variable and sum up the values in that list
        #set new_user to True since a new user id was entered
        else:
            correct_entries.append(1)
            sum_of_entries(correct_entries)
            new_id_entry.delete(0, END) 
            #global varaible to determine if a new user is using the GUI
            global new_user
            new_user = True
   
    #GET NUMBER OF BOOKS TO RECOMMEND
    #label for new user
    lab_book_rec = Label(window, text = "\n\tNo. of Books to Recommend", font = 'Helvetica 12 bold')
    lab_book_rec.grid(row = 12, column = 0)
    #label for number of books
    lab_num_books = Label(window, text = "\t\t\tEnter Number of Books", font = 'Helvetica 10')
    lab_num_books.grid(row = 13, column = 0)
    #place to enter the ID
    global num_books_entry
    num_books_entry = Entry(window, width = 20, borderwidth = 6, font = 'Helvetica 12')
    num_books_entry.grid(row = 13, column = 0, columnspan=4)
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
        elif(int(num_books) > 20):
            messagebox.showwarning(title = 'Python Warning', message = 'Warning: The entered number of books to recommend is larger than 20.\nEnter a smaller number.')
            num_books = ""
            num_books_entry.delete(0, END)
            return()
        else:
        #the number of books has been entered correctly
        #add a 1 to the correct _entries list variable and sum up the values in that list
            correct_entries.append(1)
            sum_of_entries(correct_entries)
            num_books_entry.delete(0, END)

    #space
    lab_space = Label(window, text = "\n\n\n\n", font = 'Helvetica 10')
    lab_space.grid(row = 13, column = 0)

    #function to display the second window that will list the books that are being recommended
    def SecondWindow():
        #if there were not 2 correct entires given an error is displayed
        if(total < 2):
            messagebox.showerror(title = 'Python Error', message = 'Error: The user ID and number of books needs to be entered first. ')
        #if two entries are correctly given create the new window with the same dimensions as the previous window
        else:
            win = tk.Tk()
            win.title('GoodReadsBookRecommendations')
            win.geometry("1000x600")
            
            #will need to convert the user given data to integers instead of string variables to properly use the 
                #previously defined function (getRec() and getRand()) to get the list of books
            num_books_int = int(num_books)

            #if a returning user id is provided (aka new_user = False)
            if not new_user:
                user_id_int = int(user_id)
                rec_books = getRec(user_id_int, num_books_int)
                
                #loop over the returned list of books from the getRec function
                #https://stackoverflow.com/questions/38559778/tkinter-print-specified-item-from-list-in-loop
                for i in range(rec_books.size):
                    #get the title of the book using the book id
                    rec = books[books['book_id']==rec_books[rec_books.size - (i + 1)]].title.to_string(index=False)
                    #add a listing number (1, 2, 3, etc.) and a : before the title of the book
                    rec_list = str(i+1) + ": " + rec
                    book_title = rec_list
                    #create the label that will display the book titles
                    book_list = Label(win, text=book_title, font = 'Helvetica 12 bold', width = 100)
                    book_list.grid(row = i+1, column = 0, columnspan = 5, sticky = E)
                #use a lambda function to recursively print each of the book titles
                def connect_callback(title):
                    book_list.bind('<Enter>', lambda event:print(title))
                    connect_callback(title)
            else:
                #if a random id is entered use the getRand function to get the list of books 
                    #(see above comments for further explanation as process is quite similar)
                randomIds = getRand(num_books_int)
                for i in range(randomIds.size):
                    rand_rec = books[books['book_id']==randomIds[randomIds.size - (i + 1)]].title.to_string(index=False)
                    rec_list = str(i+1) + ": " + rand_rec
                    rand_book_title = rec_list
                    rand_book_list = Label(win, text=rand_book_title, font = 'Helvetica 12 bold', width = 100)
                    rand_book_list.grid(row = i+1, column = 0, columnspan = 5, sticky = E)
                def connect_callback(rand_title):
                    rand_book_list.bind('<Enter>', lambda event:print(rand_title))
                    connect_callback(rand_title)
                    #use the returning user id to list the book recommendations
            win.mainloop()

    # Buttons that are displayed on the first window (Enter button etc.)
    Button(window, text = "Enter", font = 'Helvetica 10 bold', command = ret_user_button).grid(row = 7, column = 1, sticky = E)
    Button(window, text = "Enter", font = 'Helvetica 10 bold', command = new_user_button).grid(row = 10, column = 1, sticky = E)
    Button(window, text = "Enter", font = 'Helvetica 10 bold', command = num_books_button).grid(row = 13, column = 1, sticky = E)
    Button(window, text = "Click Here to Get Book Recommendations!", font = 'Helvetica 12 bold', command = SecondWindow).grid(row = 16, column = 0, columnspan = 4)
    
    #this opens the window and keeps it open until someone closes the window
    window.mainloop()