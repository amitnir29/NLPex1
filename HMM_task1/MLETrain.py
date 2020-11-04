# IMPORTS
import sys


UNK = '*UNK*'
START = '*START*'


#TODO: 1. IN CASE NOT 2 WORDS, 2. ^ WHAT? 3. UNKs

def main():
    input_file = open(sys.argv[1], 'r')
    # each line is a sentence
    train_data = input_file.read().splitlines()
    input_file.close()
    q_dict = {}
    e_dict = {}

    # TODO make UNKs

    for line in train_data:
        words_with_tags = line.split(' ')
        # for the q we will need to remember last two tags
        tag_before_2 = START
        tag_before_1 = START
        for word_and_tag in words_with_tags:
            # TODO:
            try:
                word, tag = word_and_tag.split('/')
            except:
                print(word_and_tag)

            # for e
            key = word + ' ' + tag
            if key in e_dict:
                e_dict[key] += 1
            else:
                e_dict[key] = 1

            # for q
            for key in [tag, tag + ' ' + tag_before_1, tag + ' ' + tag_before_1 + ' ' + tag_before_2]:
                if key in q_dict:
                    q_dict[key] += 1
                else:
                    q_dict[key] = 1


            # for q next round
            tag_before_2 = tag_before_1
            tag_before_1 = tag

    # write to outputs
    q_output = open(sys.argv[2], 'w')
    for key, value in q_dict.items():
        q_output.write(key + "\t" + str(value) + "\n")
    e_output = open(sys.argv[3], 'w')
    for key, value in e_dict.items():
        e_output.write(key + "\t" + str(value) + "\n")
    q_output.close()
    e_output.close()


if __name__ == '__main__':
    main()

#YUVAL is trying


