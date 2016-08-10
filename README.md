# tweets_bosnia
Collecting and analysing tweets from within Bosnia and from Bosnian users.

This projects allows to 

* scrape the 200 most common Bosnian, Croatian and Serbian words (00_most_common_words.py). Collected words are saved in .txt format.
* collect selected tweets from relevant political actors within Bosnia (01_twitter_parties.py). Collected tweets are saved in .json format.
* collect tweets via a stream from within Bosnia and from Bosnian users (02_bosnian_users.py). Collected tweets are saved in .json format.
* analyse the collected tweets using R (99_analysis_bosnian_all.R)
