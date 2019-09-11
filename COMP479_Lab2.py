import os
import re
from bs4 import BeautifulSoup

#Get all reuters tags
reuters_file = open('reut2-000.sgm').read()
soup = BeautifulSoup(reuters_file, 'html.parser')
reuters_tag = soup.find_all('reuters')

all_places = open('all-places-strings.lc.txt').read()
for place in all_places.split("\n"):
    for reuter in reuters_tag:
        