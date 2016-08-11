# tweets_bosnia
Collecting and analysing tweets from within Bosnia and from Bosnian users.

This projects allows to 

* scrape the 200 most common Bosnian, Croatian and Serbian words using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (**python/00_most_common_words.py**). The words are scraped from subpages of [http://www.ezglot.com/most-frequently-used-words.php](http://www.ezglot.com/most-frequently-used-words.php), and saved in .txt format (data/txt). The scraper can be easily extended to scrape more than just the 200 most common words (ezglot.com provides 3000 words per language); and to scrape the most common words of other languages than Bosnian, Croatian or Serbian. List of most common words are helpful for collecting tweets that use a certain language (especially if you don't always want to trust Twitter's language classification). 

* collect selected tweets from relevant political actors within Bosnia (**python/01_twitter_parties.py**). Selected parts of the collected tweets are saved in .json format (data/json). I hand-selected the political actors I want to follow. Each time the file is run, it looks up the 200 latest tweets from those relevant actors and adds them to the json file in case the tweet is not yet there (no duplication of tweets). This signifies that no Twitter stream is necessary, but that you are very likely to get all relevant tweets if you run the script often enough (I have a [cronjob](http://www.everydaylinuxuser.com/2014/10/an-everyday-linux-user-guide-to.html) that runs it once a day). 

* collect tweets via a stream from within Bosnia and from Bosnian users (**python/02_bosnian_users.py**). Collected tweets are saved in .json format (data/json). The format (store all tweets always inside an array) makes sure that I easily can read all tweets into R using the [jsonlite](https://cran.r-project.org/web/packages/jsonlite/vignettes/json-aaquickstart.html)
package. The format remains correct even if you interrupt the stream with CTRL-C.

* analyse the collected tweets using R (**R/99_analysis_bosnian_all.R**).
