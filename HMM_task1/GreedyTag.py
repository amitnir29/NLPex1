# IMPORTS
import sys
import math

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

    print()
    print()
    print()
    print(possible_tags)
    print()
    print()
    print()

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


def geerdyHMM(sentence):
    words = sentence.split(" ")
    n = len(words)
    tags = [""]*n

    for i in range(0,n):
        known = 0
        p_ti_wi = -sys.maxsize - 1

        for tag in possible_tags:
            g_t_wi=0
            e = getE(words[i], tag)
            if e != 0:
                known = 1
                e = math.log(e)
            else:
                continue

            if i==0:
                g_t_wi = e + math.log(getQ(START, START, tag))
            elif i==1:
                g_t_wi = e + math.log(getQ(START, tags[i-1], tag))
            else:
                g_t_wi = e + math.log(getQ(tags[i-2],tags[i-1],tag))

            if g_t_wi > p_ti_wi:
                tags[i] = tag
                p_ti_wi = g_t_wi

        if not known:
            word_signature = find_word_signature(words[i])
            for tag in possible_tags:
                g_t_wi = 0
                e = getE(word_signature, tag)
                if e == 0:
                    continue
                e = math.log(e)

                if i == 0:
                    g_t_wi = e + math.log(getQ(START, START, tag))
                elif i == 1:
                    g_t_wi = e + math.log(getQ(START, tags[i - 1], tag))
                else:
                    g_t_wi = e + math.log(getQ(tags[i - 2], tags[i - 1], tag))

                if g_t_wi > p_ti_wi:
                    tags[i] = tag
                    p_ti_wi = g_t_wi


    #print (tags)
    return tags




def main():
    initialize_suffixes()
    all_q_counts(sys.argv[2])
    all_e_counts(sys.argv[3])

    input_file = open(sys.argv[1], 'r')
    # each line is a sentence
    input_data = input_file.read().splitlines()
    input_file.close()

    output_file = open(sys.argv[4], 'w')

    for sentence in input_data:
        tags = geerdyHMM(sentence)
        words = sentence.split(" ")
        n = len(words)
        words_tags = ""
        for i in range(0,n-1):
            words_tags = words_tags + words[i] + "/" + tags[i] + " "
        words_tags = words_tags + words[n - 1] + "/" + tags[n - 1]
        output_file.write(words_tags+"\n")

    output_file.close()

if __name__ == '__main__':
    main()