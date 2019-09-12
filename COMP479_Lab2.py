import os
from os import path
import re
from bs4 import BeautifulSoup

#get number of files
directory = os.getcwd()
cpt = sum([len(files) for r, d, files in os.walk(str(directory)+"/reuters")])


#Get all reuters tags from all files

for i in range(cpt):
    file_name = 'reut2-' + str(f'{i:03}') + '.sgm'
    reuters_file = open(directory + "/reuters/" + file_name).read()
    file_table = file_name.split(".")[0] + "_table.txt"

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
        table = open(file_table, "a")
        table.write(row)

# for place in all_places.split("\n"):
#     for reuter in reuters_tag:
#         number_of_occurence = str(reuter).count(str(place))
