import sys
import string
from sklearn.feature_extraction import DictVectorizer
import pickle

START = '*START*'
NONE = '*NONE*'


def counter(lines):
    count = {}
    for line in lines:
        words = line.split(' ')
        for word in words:
            if word in count:
                count[word] += 1
            else:
                count[word] = 1
    return count

def main():
    input_file = open(sys.argv[1], 'r')
    # each line is a sentence
    train_data = input_file.read().splitlines()
    input_file.close()
    model = pickle.load(open(sys.argv[2], 'rb'))
    # output_file = open(sys.argv[2], 'w')

    lines = []
    dv = pickle.load(open(sys.argv[3], 'rb'))

    count = counter(train_data)
    rare = dict((k, v) for k, v in count.items() if v <= 5)
    # print(rare)

    for line in train_data:
        ptag = START
        pptag = START

        words = line.split(' ')
        for i, word in enumerate(words):

            # features = tag
            features = "t1=" + ptag
            features += " " + "t2t1=" + pptag + "_" + ptag
            # pptag = ptag
            # ptag = tag

            pword, ppword, aword, aaword = NONE, NONE, NONE, NONE
            if i == 0:
                pass
            elif i == 1:
                pword = words[0]
            else:
                pword = words[i-1]
                ppword = words[i-2]

            if i == len(words) - 2:
                aword = words[len(words) - 1]
            elif i == len(words) - 1:
                pass
            else:
                aword = words[i+1]
                aaword = words[i+2]

            if ppword != NONE:
                features += " " + "ppw=" + ppword
            if pword != NONE:
                features += " " + "pw=" + pword
            if aword != NONE:
                features += " " + "aw=" + aword
            if aaword != NONE:
                features += " " + "aaw=" + aaword


            # if not rare
            if word not in rare:
                # pass
                features += " " + "form=" + word
            # rare
            else:
                if any([str(i) in word for i in range(10)]):
                    features += " " + "contNumber=True"
                else:
                    features += " " + "contNumber=False"

                if '-' in word:
                    features += " " + "contHyphen=True"
                else:
                    features += " " + "contHyphen=False"

                if any([letter in word for letter in string.ascii_uppercase]):
                    features += " " + "contUpper=True"
                else:
                    features += " " + "contUpper=False"

                for i in range(1, min(4+1, len(word) + 1)):
                    end = len(word) - 1
                    features += " " + "suff" + str(i) + "=" + word[end-i + 1 : end + 1]
                    features += " " + "pre" + str(i) + "=" + word[0 : i]

            x_line_dict = {}
            x_line = features
            for key_and_value in x_line.split(' '):
                # print(key_and_value)
                key, value = key_and_value.split('=', 1)
                x_line_dict[key] = value
            print(x_line_dict)
            X = dv.transform(x_line_dict)
            print(X)

            print(model.predict(X))
            break





if __name__ == '__main__':
    main()
