# IMPORTS
import sys
import math
from collections import deque
import time

START = '*START*'
END = '*END*'
q_counts = dict()
e_counts = dict()
possible_tags = set()
num_words = 0
num_START_words = 0
suffix_1 = set()
suffix_2 = set()
suffix_3 = set()
suffix_4 = set()

def initialize_suffixes():
    global suffix_1
    global suffix_2
    global suffix_3
    global suffix_4

    suffix_1.update(
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')', '"', '.', '!', '#', ',', ';', ':', '-', '?', '\'',
         '`'])
    suffix_2.update(["er", "or", "th", "al", "ic", "ed", "ly", "en", "fy", "ee", "ry", "``", "''", "--"])
    suffix_3.update(["ion", "ity", "ful", "ous", "ive", "ing", "dom", "acy", "ism", "ist", "ate", "ish", "ive", "..."])
    suffix_4.update(["ment", "ness", "ship", "able", "less", "hood", "wise", "ward"])


def find_word_signature( str ):
    end = len(str)
    last_1 = str[end - 1:]
    last_2 = str[end - 2:]
    last_3 = str[end - 3:]
    last_4 = str[end - 4:]

    if last_4 in suffix_4:
        return "^"+last_4

    if last_3 in suffix_3:
        return "^"+last_3

    if last_2 in suffix_2:
        return "^"+last_2

    if last_1 in suffix_1:
        return "^"+last_1

    return "^NONE"


def all_q_counts(q_file_name):
    global q_counts
    global num_START_words

    q_file = open(q_file_name, 'r')
    lines = q_file.read().splitlines()
    q_file.close()
    for line in lines:
        tags_count = line.split("\t")
        q_counts[tags_count[0]] = int(tags_count[1])

    for key in q_counts:
        tags = key.split(" ")
        if(tags[0] == START and len(tags) == 2):
            num_START_words += q_counts[key]


def all_e_counts(e_file_name):
    global e_counts
    global possible_tags
    global num_words

    e_file = open(e_file_name, 'r')
    lines = e_file.read().splitlines()
    e_file.close()
    for line in lines:
        word_tag__count = line.split("\t")
        e_counts[word_tag__count[0]] = int(word_tag__count[1])
        tag = ((word_tag__count[0]).split(" "))[1]
        possible_tags.update([tag])

    # print()
    # print()
    # print()
    # print(possible_tags)
    # print()
    # print()
    # print()

    for key in e_counts:
        if key[0]!='^':
            num_words += e_counts[key]


def getQ(t1, t2, t3):
    x = 0.8
    y = 0.15
    z = 0.05

    if t3 == END:
        p1 = 1
    else:
        p1 = q_counts[t3] / num_words
    if(t2 == START):
        try:
            p2 = q_counts[t2 + " " + t3]/num_START_words
        except:
            p2=0
        try:
            p3 = q_counts[t1 + " " + t2 + " " + t3] / num_START_words
        except:
            p3=0
    else:
        try:
            p2 = q_counts[t2 + " " + t3] / q_counts[t2]
        except:
            p2=0
        try:
            p3 = q_counts[t1 + " " + t2 + " " + t3] / q_counts[t1 + " " + t2]
        except:
            p3=0

    q = x*p3 + y*p2 + z*p1
    return q

def getE(w1, t1):
    c2 = q_counts[t1]
    if w1 + " " + t1 in e_counts:
        c1 = e_counts[w1 + " " + t1]
        if c1 > 1:
            p = c1/c2
            return p
    return 0



def tags(i):
    start = set()
    start.update([START])
    if i == -1 or i == 0:
        return start
    else:
        return possible_tags

active_tags = dict()

f=0
def Viterbi(sentence):
    global active_tags
    words = sentence.split(" ")
    n = len(words)

    v_p = dict()
    v_p[(0,START,START)] = 0.0
    v_tags = dict()


    for i in range(1,n+1):
        known = 0

        max1=0
        tag1 = None
        max2=0
        tag2 = None
        for t in tags(i):
            e = getE(words[i-1],t)
            if e != 0:
                known = 1
                e = math.log(e)
            else:
                #e = -sys.maxsize - 1
                continue
            #max3 is for finding the best t1 for each t (and then will find best two t)
            max3 = 0
            for t_i_1 in tags(i-1):
                p_max = -sys.maxsize - 1
                best_tag = None
                for t_i_2 in tags(i-2):
                    try:
                        p = v_p[(i-1,t_i_2,t_i_1)] + math.log(getQ(t_i_2, t_i_1, t)) + e
                    except:
                        p = -sys.maxsize - 1
                    if p > p_max:
                        p_max = p
                        best_tag = t_i_2
                v_p[(i,t_i_1,t)] = p_max
                v_tags[(i,t_i_1,t)] = best_tag

                if p_max > max3:
                    max3 = p_max

            if max3 >= max2 and max3 >= max1:
                max2 = max1
                tag2 = tag1
                max1 = max3
                tag1 = t
            elif max3 >= max2:
                max2 = max3
                tag2 = t
            active_tags[i] = (tag1, tag2)




        if not known:
            word_signature = find_word_signature(words[i-1])
            for t in tags(i):
                e = getE(word_signature, t)
                if e == 0:
                    #e = -sys.maxsize - 1
                    continue
                else:
                    e = math.log(e)
                for t_i_1 in tags(i - 1):
                    p_max = -sys.maxsize - 1
                    best_tag = None
                    for t_i_2 in tags(i - 2):
                        try:
                            p = v_p[(i - 1, t_i_2, t_i_1)] + math.log(getQ(t_i_2, t_i_1, t)) + e
                        except:
                            p = -sys.maxsize - 1
                        if p > p_max:
                            p_max = p
                            best_tag = t_i_2
                    v_p[(i, t_i_1, t)] = p_max
                    v_tags[(i, t_i_1, t)] = best_tag

    best_tags = deque()

    best_last = None
    best_last_1 = None
    p_max = -sys.maxsize - 1
    for t in tags(n):
        for t_1 in tags(n-1):
            try:
                p = v_p[(n,t_1,t)] + math.log(getQ(t_1,t,END))
            except:
             p = -sys.maxsize - 1
            if p > p_max:
                p_max = v_p[(n,t_1,t)]
                best_last = t
                best_last_1 = t_1

    if best_last == None or best_last == "*START*":
        best_last = "O"
    best_tags.append(best_last)
    if best_last_1 == None or best_last_1 == "*START*":
        best_last_1 = "O"
    best_tags.append(best_last_1)

    # for i in range(n-2,0,-1):
    #     j = n-i+2
    #     best_tags.append(v_tags[(i+2),best_tags[i+1],best_tags[i]])

    for i, k in enumerate(range(n - 2, 0, -1)):
        try:
            if v_tags[(k + 2, best_tags[i + 1], best_tags[i])] ==  None or v_tags[(k + 2, best_tags[i + 1], best_tags[i])] == "*START*":
                best_tags.append("O")
            else:
                best_tags.append(v_tags[(k + 2, best_tags[i + 1], best_tags[i])])
        except:
            best_tags.append("O")
            print(sentence)
            print()
            print()
    best_tags.reverse()
    global f
    print(f)
    f+=1
    #
    # tags_list = list()
    # for i in range(0,n):
    #     tags_list.append(best_tags[i])
    #print(sentence)
    return best_tags




def main():
    start = time.time()

    initialize_suffixes()
    all_q_counts(sys.argv[2])
    all_e_counts(sys.argv[3])

    input_file = open(sys.argv[1], 'r')
    # each line is a sentence
    input_data = input_file.read().splitlines()
    input_file.close()

    output_file = open(sys.argv[4], 'w')

    for sentence in input_data:
        tags = Viterbi(sentence)
        words = sentence.split(" ")
        n = len(words)
        words_tags = ""
        for i in range(0, n-1):
            words_tags = words_tags + words[i] + "/" + tags[i] + " "
        words_tags = words_tags + words[n-1] + "/" + tags[n-1]
        output_file.write(words_tags + "\n")

    output_file.close()

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()