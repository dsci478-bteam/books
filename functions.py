# Package Imports
import math
import numpy as np
import numpy_indexed as npi 
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import time

# Prints out num_rec book recommendations for user_id
def getRec(user_id, num_rec):

    # Read books data
    books = pd.read_csv('red_books.csv')

    # Read sparse matrix encoding into df
    sparse_df = pd.read_csv('users_sparse.csv')

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

    # Print titles
    for i in range(rec_books.size):
        print(i+1,": ",books[books['book_id']==rec_books[rec_books.size - (i + 1)]].title.to_string(index=False))

# Main Function
def main():
  getRec(500002,10)  

start_time = time.time()

if __name__=="__main__":
    main()

print("--- %s seconds ---" % (time.time() - start_time))
