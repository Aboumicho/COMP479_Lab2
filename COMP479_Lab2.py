import os
from os import path
import re
from bs4 import BeautifulSoup

#get number of files
directory = os.getcwd()
cpt = sum([len(files) for r, d, files in os.walk(str(directory)+"/reuters")])


#Get all reuters tags from all files
file_name = 'reut2-'

# for i in range(cpt):
#     file_name + f'{i:03}' + '.sgm'
#     reuters_file = open(file_name).read()
reuters_file = open('reut2-000.sgm').read()

soup = BeautifulSoup(reuters_file, 'html.parser')
reuters_tag = soup.find_all('reuters')

all_places = open('all-places-strings.lc.txt').read()
list_places = []

for reuter in reuters_tag:
    article_id = reuter.get('newid')
    row = "Article newid="+str(article_id) + ": " 
    #check for places in reuter article
    for place in all_places.split("\n"):
        if place in reuter.get_text():
            row += place + " | "
    #write to file
    row += "\n"
    file_table = open("reut2-001_table.txt", "a")
    file_table.write(row)

# for place in all_places.split("\n"):
#     for reuter in reuters_tag:
#         number_of_occurence = str(reuter).count(str(place))
