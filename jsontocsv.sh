#!/bin/bash

# Have all uncompressed .json files in same directory as script, or modify script to look at another location :)
# Parts in the brackets e.g. [.book_id, .title, ...] are the variables being pulled from the .json files. 
# That is what we would change if we needed to add other variables, but as of now I don't think we need to.

jq -r '. | [.book_id, .title, .average_rating, .description] | @csv' goodreads_books_young_adult.json > books.csv
jq -r '. | [.user_id, .book_id, .is_read, .rating] | @csv' goodreads_interactions_young_adult.json > interactions.csv
jq -r '. | [.user_id, .book_id, .review_text, .rating] | @csv' goodreads_reviews_young_adult.json > reviews.csv
