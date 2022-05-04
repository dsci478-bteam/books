# Final Project DSCI 487
Written by Mandey Brown, Sam Fortescue, Emma Hamilton

# Data

**Note:** the GUI does not depend on these files, so there is no need to download them unless your intention is to run data.ipynb.

First step of the process: use the Young Adult genre data that can be gathered from: https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

Unpack the .gz file and run the jsontocsv.sh script to convert the json files to csv files. Or use the links below.
The following files are too large to stored on Github so each are stored on Google Drive and can be accessed through the following links:
- Books: https://drive.google.com/file/d/15DvRQIdkXVg3qXVkyDm2GsgXVcTmgzYj/view?usp=sharing
- Interactions: https://drive.google.com/file/d/1fw03Bv9094adgGqZHvPcSE6O_HaKV5nf/view?usp=sharing

# Dependencies

This repo uses Git Large File Storage. In order to clone the repository completely one needs to install Git LFS ([found here](https://git-lfs.github.com/)) onto their local instance of git, and run `git lfs install`.

In addition the following Python packages are used in the GUI:
- [numpy](https://numpy.org/)
- [numpy_indexed](https://github.com/EelcoHoogendoorn/Numpy_arraysetops_EP)
- [pandas](https://pandas.pydata.org/)
- [scipy](https://scipy.org/)
- [sklearn](https://scikit-learn.org/stable/index.html)
- [tkinter](https://tkdocs.com/index.html) (for install see [here](https://realpython.com/python-gui-tkinter/))
- [pillow](https://python-pillow.org/) (if you get an error message running GUI.py that is related to 'ImageTK' see [here](https://stackoverflow.com/questions/48317606/importerror-cannot-import-name-imagetk))

# About

The data.ipynb is a jupyter notebook file that is used to load the above files for usage. The loaded files are then formated into a sparse matrix which allows for ease of computation for computing the Recommender System. This file also generates the red_books.csv (comprising of the books that have been read by any user) file and the user_sparse.csv file (consiting of the coordinate spare matrix encoding). You will likely not need to use this file.

GUI.py contains two functions that create a listing of a provided number of books to either a returning user or a new user. The returning users will get a list of books based on the Collaborative Filtering Recommender System that uses the results of the weighted adjusted cosinse similarity score. The users that have the closest similarity (that are not 1) to the entered user will be used to recommend books. If the cosine similarity is 1 there are no unread books between the users, as such there would be no books to recommend from this user. The most liked books from the similar user that have not been read by the entered user will be displayed. At this time, a cold start Recommender System has not been implemented due to time constraints. Currently when a new user is selected, a list of book will be generated randomly using the books who have an average rating above 4.5 out of 5. 

A GUI was created to interact with this process using the python library tkinter. GUI.py contains the functions needed to get the recommended books from the sparse matrix as well as the GUI itself. In the GUI a user will either enter a returning user ID or a new user ID and the number of books they want recommended to them. They then will click the button to get the list of recommendations and a new window will pop up with the list of recommendations. There are error checks in place to prevent users from entering a character as a user ID among other checks. If an error occurs a new window will open and display a message. 
