import sys

def main():
    # file1 = open(sys.argv[1], 'r')
    file1 = open("hmm-viterbi-predictions.txt", 'r')
    lines_1 = file1.read().splitlines()
    file1.close()
    # file2 = open(sys.argv[2], 'r')
    file2 = open("ass1-tagger-dev", 'r')
    lines_2 = file2.read().splitlines()
    file2.close()

    n = len(lines_1)
    if n != len(lines_2):
        print("different numbers of lines")
        exit(-1)

    true_predictions = 0
    all_predictions = 0
    for i in range(0,n):
        words_tags_1 = lines_1[i].split(" ")
        words_tags_2 = lines_2[i].split(" ")
        j = len(words_tags_1)
        if j != len(words_tags_2):
            print("different numbers of tags in line ", i)
            exit(-1)

        for k in range(0,j):
            all_predictions += 1
            word1, tag1 = words_tags_1[k].rsplit('/',1)
            word2, tag2 = words_tags_2[k].rsplit('/',1)

            if word1 != word2:
               print("different words")
               exit(-1)

            if tag1 == tag2:
                true_predictions += 1
            else:
                print(words_tags_1)
                print()
                print(words_tags_2)
                print(word1 + "    " + tag1 + "    true:" + tag2)
                print()
                print()
                print()

    accuracy = true_predictions/all_predictions
    accuracy *= 100
    print(accuracy)
if __name__ == '__main__':
    main()


