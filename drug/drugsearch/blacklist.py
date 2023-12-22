import sys
import re

def black_list(keyword=""):
    black = []
    li = []
    
    with open(r"/root/IRSE/Project/drug/drugsearch/black.txt", 'r') as f:
        for line in f:
            black.append(line.strip('\n'))
    for i in black:
        if keyword == i:
            #keyword = keyword.replace(i, 'sensitive')
            li.append(keyword)
            print('Invalid Search')        

    return li


if __name__ == '__main__':
    print(black_list("hard drug"))

