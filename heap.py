import sys
import heapq
from random import randint
from os import listdir
from os.path import isfile, join

class Node:
    def __init__(self, word, count):
        self.words = set()
        self.words.add(word)
        self.count = count
        self.nxt = None
        self.prev = None
    
    def add_word(self, word):
        self.words.add(word)

    def remove_word(self, word):
       self.words.remove(word)

class Lru:
    def __init__(self):
        self.node_ptrs = {}
        self.head = None
        self.tail = None

    def add_word(self, word):
        if word in self.node_ptrs:
            n = self.node_ptrs[word]
            if n.prev != None: #there is a word in front of it
                if n.prev.count == n.count + 1: #this means prior node is one higher and we move word up a node
                    n.remove_word(word)
                    n.prev.add_word(word)
                    self.node_ptrs[word] = n.prev
                else: #prior node is not one higher
                    if len(n.words) == 1: #optimization that allows you to change count if there is only one word in node
                        n.count += 1
                    else: #we need to make a middle node
                        self.add_middle_node(n, word)
            else: #there isn't a node in front of n
                if len(n.words) == 1: #optimization that allows you to change count if there is only one word in node
                    n.count += 1
                else:
                    self.move_node_to_front(n, word)
            if len(n.words) == 0: #kill n node if it is empty
                n.prev.nxt = n.nxt
                n.nxt.prev = n.prev
        else: #word doesn't exist
            if self.tail == None: #no nodes exist in list
                n = Node(word, 1)
                self.tail = n
                self.head = n
                self.node_ptrs[word] = n
            elif self.tail.count > 1: #back of the list count exceeds one
                self.add_node_to_back(word)
            else:
                self.tail.add_word(word)
                self.node_ptrs[word] = self.tail

    def add_node_to_back(self, word):
        n = Node(word, 1)
        self.node_ptrs[word] = n
        self.tail.nxt = n
        n.prev = self.tail
        self.tail = n

    def add_middle_node(self, n, word):
        n.remove_word(word)
        middle = Node(word, n.count + 1)
        middle.nxt = n
        middle.prev = n.prev
        middle.prev.nxt = middle
        middle.nxt.prev = middle
        self.node_ptrs[word] = middle

    def move_node_to_front(self, n, word):
        n.remove_word(word)
        first = Node(word, n.count + 1)
        n.prev = first
        first.nxt = n
        self.node_ptrs[word] = first
        self.head = first

    def get_k_words(self, k):
        n = self.head
        words = k
        rv = []
        while(words > 0):
            for word in n.words:
                rv.append((n.count, word))
            words -= len(n.words)
            n = n.nxt
        return rv

if __name__ == "__main__":
    k = sys.argv[1]
    k = int(k)
    onlyfiles = [ f for f in listdir("./text") if isfile(join("./text",f)) ]
    print onlyfiles
    count = 0
    if (sys.argv[2] == "lru"):
        lru = Lru();
        for f in onlyfiles:
            with open ("./text/" + f, 'r') as f:
                for line in f:
                    for word in line.split():
                        count += 1
                        lru.add_word(word)
        print lru.get_k_words(k)
        print "Number of words", count

    else:
        dict = {}
        for f in onlyfiles:
            with open ("./text/" + f, 'r') as f:
                for line in f:
                    for word in line.split():
                        if word in dict:
                            dict[word] += 1
                        else:
                            dict[word] = 1
        heap = []
        len(dict)
        for word, count in dict.iteritems():
            heap.append((count, word))

        heapq.heapify(heap)
        heapq.nlargest(k, heap)

