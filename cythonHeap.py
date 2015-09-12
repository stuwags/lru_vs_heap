import heap
import sys
import heapq
from random import randint
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    k = 70000
    onlyfiles = [ f for f in listdir("./text") if isfile(join("./text",f)) ]
    print onlyfiles

    # dict = {}
    lru = heap.Lru();
    for f in onlyfiles:
        with open ("./text/" + f, 'r') as f:
            for line in f:
                for word in line.split():
                    # if word in dict:
                    #     dict[word] += 1
                    # else:
                    #     dict[word] = 1
                    lru.add_word(word)
    lru.get_k_words(k)

    # heap = []
    # for word, count in dict.iteritems():
    #     heap.append((count, word))
    #     n = node(word, count)


    # heapq.heapify(heap)
    # heapq.nlargest(k, heap)
    # k = randint(0, 50000)

