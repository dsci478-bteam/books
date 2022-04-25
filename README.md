# Final Project DSCI 487
Written by Mandey Brown, Sam Fortescue, Emma Hamilton

First step of the process: use the Young Adult genre data that can be gathered from: https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

Unpack the .gz file and run the jsontocsv.sh script to convert the json files to csv files. 
The csv files are too large to store on an individual machine so each are stored on Google Drive and can be accessed through the following links:
- Books: https://drive.google.com/file/d/15DvRQIdkXVg3qXVkyDm2GsgXVcTmgzYj/view?usp=sharing
- Interactions: https://drive.google.com/file/d/1fw03Bv9094adgGqZHvPcSE6O_HaKV5nf/view?usp=sharing
- Reviews: https://drive.google.com/file/d/1YsCPIsibCmrMCd1jZzPNZozdI1ezg8qb/view?usp=sharing

The data.ipynb is a jupyter notebook file that is used to load the above files for usage. The loaded files are then formated into a sparse matrix which allows for ease of computation for computing the recommender system. This file also generates the red_books.csv (comprising of the books that have been read by any user) file and the user_sparse.csv file (consiting of the coordinate spare matrix encoding)

GUI.py contains two functions that create a listing of a provided number of books to either a returning user or a new user. The returning users will get a list of books based on the collaborativee recommender system that uses the results of the adjusted cosinse similarity score. The user that has the closest similarity to the entered user will be used to recommend books. The most liked books from the similar user that have not been read by the entered user will be displayed. At this time, a cold start recommender system has not been implemented due to time constraints. Currently when a new user is selected, a list of book will be generated randomly using the books who have an average rating above 4.5 out of 5. 

A GUI was created to interact with this process using the python library tkinter. GUI.py contains the functions needed to get the recommended books from the sparse matrix as well as the GUI itself. In the GUI a user will either enter a returning user ID or a new user ID and the number of books they want recommended to them. They then will click the button to get the list of recommendations and a new window will pop up with the list of recommendations. 
