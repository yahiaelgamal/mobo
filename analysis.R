library(jsonlite)
library(ggplot2)
library(ggvis)

goodreads_df = fromJSON(readLines('goodreads_ratings.json'))

goodreads_df = within(goodreads_df, published[published == -1] <- NA)

agrep('the secret life of bees',
      goodreads_df$book_name,
      ignore.case = T, fixed=T)


