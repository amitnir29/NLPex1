# IMPORTS
import sys

START = '*START*'
END = '*END*'
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
    suffix_2.update(["er", "or", "th", "al", "ic", "ed", "ly", "en", "fy", "ee", "ry", "``", "''", "--", "\'\'"])
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
                word, tag = word_and_tag.rsplit('/',1)
            except:
                print(word_and_tag)

            # for e
            key = word + ' ' + tag
            if key in e_dict:
                e_dict[key] += 1
            else:
                e_dict[key] = 1

            initialize_suffixes()
            signature = find_word_signature(word)
            key = signature + ' ' + tag
            if key in e_dict:
                e_dict[key] += 1
            else:
                e_dict[key] = 1


            # for q
            for key in [tag, tag_before_1 + ' ' + tag, tag_before_2 + ' ' + tag_before_1 + ' ' + tag]:
                if key in q_dict:
                    q_dict[key] += 1
                else:
                    q_dict[key] = 1


            # for q next round
            tag_before_2 = tag_before_1
            tag_before_1 = tag

        for key in [tag_before_1 + ' ' + END, tag_before_2 + ' ' + tag_before_1 + ' ' + END]:
            if key in q_dict:
                q_dict[key] += 1
            else:
                q_dict[key] = 1

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


