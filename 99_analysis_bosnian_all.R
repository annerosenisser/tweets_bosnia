# Analysis of the distribution of all
# Bosnian tweets. 

# (c) Annerose Nisser, 2016-07-09


# Empty workspace
rm(list = ls())
setwd("~/Documents/15-16/Code/tweets_bosnia")

# Displaying Bosnian characters correctly: 
Sys.setlocale("LC_CTYPE", "UTF-8")

# Inspiring links: 
# http://juliasilge.com/blog/Ten-Thousand-Tweets/

# --------------------------- #
# Load required packages ----
require(jsonlite)
# require(lubridate) # for easily cleaning time stamps
# --------------------------- #
# Important: don't have the package rjson loaded!! 
# rjson also has the command fromJSON, which could mask
# the command from jsonlite. 
# fromJSON only works with jsonlite, not rjson! 
detach("package:rjson", unload=TRUE)


tweets_path <- "data/tweets/bosnian_politicians_tweets.txt"
# tweets_path <- "~/Documents/15-16/Data/bosnian_politicians_tweets.txt"

tweets <- fromJSON(tweets_path,
                     simplifyDataFrame = T, flatten=TRUE)


# tweets <- readLines(bosnian_all_tweets, warn = "F")


# tweets <- fromJSON("~/Documents/15-16/Data/bs_all_tweets.txt",
#                    simplifyDataFrame = T)
# ------------------------------ # 
names(tweets)

# Check whether there are any duplicate tweets (= 
# check that the procedure of NOT adding duplicate 
# tweets to the file effectively works):
length(tweets$id_str)

length(unique(tweets$id_str)) 
# yes, the procedure works efficiently. There is only one 
# duplicate (probably at the beginning of the file?)
tweets[duplicated(tweets$id_str, fromLast = TRUE), ]
tweets[duplicated(tweets$id_str), ]

# Exclude those duplicates: 
tweets <- tweets[!duplicated(tweets$id_str), ]

# ------------------------------ # 
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
time <- time[time>=as.Date("2016-01-01")] # subset time just to 2016

# hist(time, breaks = 200)
# The temporal distribution looks quite ok. 

plot(as.Date(names(table(time))), table(time), type = "l", 
     yaxt = "n", xlab = "day", "ylab" = "# daily tweets")
axis(2, at = pretty(table(time)), labels = pretty(table(time)))
abline(v = as.Date("2016-10-02"), col = "red", cex = 2, lty = 2)
text(as.Date("2016-10-02") - 4, mean(table(time)), "election day",
     srt = 90, col = "red")

# ------------------------------ # 
# Examine those who tweeted 
# How many tweets came from the news portal klix.ba? 
names(tweets)
t <- table(tweets$user.name)
t <- sort(t, decreasing = T)

par(mar = c(7.1, 4.1, 4.1, 4.1)) # bottom, left, top and right
barplot(t, xaxt = "n", yaxt = "n", ylab = "# tweets")
text(seq_along(t)*1.2, par("usr")[3] - 300, 
     labels = names(t), srt = 45, pos = 2, xpd = NA, cex = 0.7)
axis(2, at = pretty(t), labels = F, xpd = NA)
text(par("usr")[1] - 0.2, pretty(t), 
     labels = pretty(t), srt = 45, pos = 2, xpd = NA, cex = 0.7)
