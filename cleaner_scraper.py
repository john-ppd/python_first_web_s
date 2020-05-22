from bs4 import BeautifulSoup
from requests import get
import re
url = [
    'https://www.mint.ca/store/buy/new-releases_coins-cat410002',

    'https://www.boringcompany.com/'
]
list1 = []
list_start = []
list_end = []
final_list = []
final_list_boring = []

def find_all_index_start(list_index,find_word):
    #print("list1")
    #print(list1[:])
    sentence = str(list1[list_index])
    word = str(find_word)
    for match in re.finditer(word, sentence):
        list_start.append(int(match.end()))#gets end coordinate of find_word

def find_all_index_end(list_index,find_word):
    sentence = str(list1[list_index])
    word = str(find_word)
    for match in re.finditer(word, sentence):
        list_end.append(int(match.end()))

def scan_through_ranges(list_index):
    for i in range(int(len(list_start))):
        search_string = str(list1[list_index])
        if list_index == 0:
            #print(search_string[list_start[i]+1:list_end[i]-7:1])#to offset the pointer to get cleaner text without =width ect
            final_list.append(search_string[list_start[i]+1:list_end[i]-7:1])

        elif list_index == 1:
            final_list_boring.append(search_string[list_start[i]:list_end[i]-4:1])
            final_list.append(search_string[list_start[i]:list_end[i]-4:1])

    #print(final_list[:])

for i in range(len(url)):
    page = get(url[i])
    soup = BeautifulSoup(page.text, 'lxml')
    if i == 0:
        list1.append(soup.findAll( class_= "imgResult"))
        find_all_index_start(i, 'title')
        find_all_index_end(i, ' width=')
        scan_through_ranges(i)

    elif i == 1:
        #list1.clear()
        list_start.clear()
        list_end.clear()
        list1.append(soup.findAll("a"))
        find_all_index_start(i, '<a href=\"/')
        find_all_index_end(i, '</a>')
        for j in range(int(len(list_start))):
            if list_start[j] > list_end[j]:
                list_end.pop(j)
        scan_through_ranges(i)
        #print(final_list_boring[:])
        #print(list1)
        print("\n".join(final_list))
