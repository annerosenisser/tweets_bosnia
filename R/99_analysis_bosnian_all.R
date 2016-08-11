# Analysis of the distribution of all
# Bosnian tweets. 

# (c) Annerose Nisser, 2016-07-09


# Empty workspace
rm(list = ls())
setwd("~/Documents/15-16/Code/twitter")
# --------------------------- #
# Load required packages ----
require(jsonlite)
# --------------------------- #
# Important: don't have the package rjson loaded!! 
# rjson also has the command fromJSON, which could mask
# the command from jsonlite. 
# fromJSON only works with jsonlite, not rjson! 
detach("package:rjson", unload=TRUE)

tweets <- fromJSON("~/Documents/15-16/Data/bosnian_politicians_tweets.txt",
                     simplifyDataFrame = T, flatten=TRUE)

# tweets <- readLines(bosnian_all_tweets, warn = "F")


tweets <- fromJSON("~/Documents/15-16/Data/bs_all_tweets.txt",
                   simplifyDataFrame = T)

names(tweets)

table(tweets$time_zone)

table(tweets$user_lang)

table(tweets$tweet_lang)
