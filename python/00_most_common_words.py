# This is a small scraper allowing to extract the most common
# Bosnian, Croatian and Serbian words from the following websites:

from bs4 import BeautifulSoup # import beautifulsoup

import urllib
import re

# THIS SCRIPT SHOULD RUN ON PYTHON 2!
# ****************************** #
# Bosnian:
# http://www.ezglot.com/most-frequently-used-words.php?l=bos&submit=Select&lang=eng

# Croatian:
# http://www.ezglot.com/most-frequently-used-words.php?l=hrv&submit=Select

# Serbian:
# http://www.ezglot.com/most-frequently-used-words.php?l=hbs&submit=Select

languages =  ['bs', 'hr', 'sr']

websites = dict(zip(languages, ['http://www.ezglot.com/most-frequently-used-words.php?l=bos&submit=Select&lang=eng',
            'http://www.ezglot.com/most-frequently-used-words.php?l=hrv&submit=Select',
            'http://www.ezglot.com/most-frequently-used-words.php?l=hbs&submit=Select']))

words = dict.fromkeys(languages)
# ********************************** #
# https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#Quick%20Start
# http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html

# Loop see "Learning Python", pg. 397
for (key, value) in websites.items():

    r = urllib.urlopen(value).read()
    soup = BeautifulSoup(r)
    # print(type(soup))

    # print some of the html:
    # print soup.prettify()[0:20]

    # extract html:
    soup = soup.find_all("span", lang=key)

    words[key] = str(soup).split(',') # split into a list
    words[key] = words[key][0:100]


    # clean html:

    words[key] = [re.findall('\>.+\<', word) for word in words[key]]
    words[key] = [word[0] for word in words[key]] # unlist
    words[key] = [word[1:-1] for word in words[key]]

    # ensure right encoding:
    # words[key] = [word.encode('latin1') for word in words[key]]

    # Save extracted list to text file:
    name = ''.join(['../data/txt/100mostcommon_', key, '.txt'])
    file = open(name, 'w')
    for word in words[key]:
        print(key)
        print(word)
        file.write("%s\n" % word)

    file.close()


