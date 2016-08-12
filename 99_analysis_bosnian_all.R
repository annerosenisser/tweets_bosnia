# Analysis of the distribution of all
# Bosnian tweets. 

# (c) Annerose Nisser, 2016-07-09


# Empty workspace
rm(list = ls())
setwd("~/Documents/15-16/Code/tweets_bosnia")

# Inspiring links: 
# http://juliasilge.com/blog/Ten-Thousand-Tweets/

# --------------------------- #
# Load required packages ----
require(jsonlite)
require(lubridate) # for easily cleaning time stamps
# --------------------------- #
# Important: don't have the package rjson loaded!! 
# rjson also has the command fromJSON, which could mask
# the command from jsonlite. 
# fromJSON only works with jsonlite, not rjson! 
detach("package:rjson", unload=TRUE)

tweets <- fromJSON("data/tweets/bosnian_politicians_tweets.txt",
                     simplifyDataFrame = T, flatten=TRUE)

# tweets <- readLines(bosnian_all_tweets, warn = "F")


tweets <- fromJSON("~/Documents/15-16/Data/bs_all_tweets.txt",
                   simplifyDataFrame = T)

names(tweets)

table(tweets$created_at)

table(tweets$user.lang)

table(tweets$lang)
table(tweets$place.country_code)
# ------------------------------ # 
# Plot the temporal distribution of the tweets: 

class(tweets$created_at)

time <- tweets$created_at
time[200:500]

# Extract the relevant time variable: 
time <- paste0(substring(time, 5, 10), ",", substring(time, 26, 30))
time <- as.Date(time, format = "%b%d, %Y") # see http://www.statmethods.net/input/dates.html

hist(time, breaks = 200)
# The temporal distribution looks quite ok. 



# ------------------------------ # 



