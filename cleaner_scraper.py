from bs4 import BeautifulSoup
from requests import get
import re
import time
url = [
    'https://www.mint.ca/store/buy/new-releases_coins-cat410002',

    'https://www.boringcompany.com/'
]
list1 = []
list_start = []
list_end = []
final_list = []
final_list_boring = []
startup_final_list = []
list_difference = []
first_run = True


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


def assign_starting_list():
    global first_run
    global startup_final_list
    print("is first run true? ")
    print(first_run)
    if first_run:
        startup_final_list = final_list.copy()
        first_run = False
        #print("\n".join(startup_final_list))
        print("is first run true? ")
        print(first_run)


def run():
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
            #print("\n".join(final_list))
            assign_starting_list()


def clear_and_compare_lists():
    global first_run
    global list_difference
    starting_list_length = int(len(startup_final_list))
    final_list.append("dog coin")
    new_list_length = int(len(final_list))
    print(starting_list_length)
    print(new_list_length)
    #print("startup_final_list")
    #print(startup_final_list)
   # print("final_list")
    #print(final_list)
    if starting_list_length < new_list_length:
        list_difference.append(str([item for item in final_list if item not in startup_final_list]))
        #list_difference.append(str(list_difference))
        print(list_difference[:])
        print("startup < final")
    elif starting_list_length > new_list_length:
        list_difference.append(str([item for item in startup_final_list if item not in final_list]))
        #list_difference.append(list_difference)
        #list_difference.append(str(list_difference))

        print(list_difference[:])
        print("startup > final")
    else:
        list_difference.append(str([item for item in final_list if item not in startup_final_list]))

        #list_difference.append(str(list_difference))
        print(list_difference[:])
        print("startup == final")
    if len(list_difference) != 0:
        print("Will Email the List!")

    if not first_run:
        list1.clear()
        list_start.clear()
        list_end.clear()
        final_list.clear()
        list_difference.append(" ")
        list_difference.clear()


while True:
    run()
    print("in compare")
    if not first_run:
        startup_final_list.pop(0)
        clear_and_compare_lists()
    time.sleep(10)


