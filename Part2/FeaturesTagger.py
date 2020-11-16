import sys
import string
from sklearn.feature_extraction import DictVectorizer
import pickle

START = '*START*'
END = '*END*'
NONE = '*NONE*'
SR_TVAH = 4

suffixes = ["eer", "er", "ion", "ity", "ment", "ness", "or", "sion", "ship", "th",
            "able", "ible", "al", "ary", "ful", "ic", "ious", "ous", "ive", "less", "y",
            "ed", "en", "ing", "ize", "ise",
            "ly", "ward", "wise",
            "less", "or", "ar", "ist", "al", "ion", "ence", "ment", "ness", "ish", "ify", "ize"]

prefixes = ["anti", "dis", "en", "il", "im", "in", "ir", "mis", "non", "ob", "op", "pre", "un", "re",
            "auto", "de", "down", "extra", "hyper", "inter", "mega", "mid", "over", "out", "post", "pro",
            "semi", "sub", "super", "tele", "trans", "ultra", "under", "up"]





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


    dv = pickle.load(open(sys.argv[3], 'rb'))


    count = counter(train_data)
    rare = dict((k, v) for k, v in count.items() if v <= 5)
    # print(rare)

    maxlen = 0
    # minlen = 1000
    lines = []
    # ptags = []
    # pptags = []
    for line in train_data:
        maxlen = max(maxlen, len(line.split(" ")))
        lines.append([[NONE, {}, START], [NONE, {}, START]]
                     + [[word, {}, ""] for word in line.split(" ")]
                     + [[NONE, {}, END], [NONE, {}, END]])
    # print(minlen)

    for column_index in range(2, maxlen + 2):
        dict_list = []
        for line_index, line in enumerate(lines):
            if column_index >= len(line) - 2:
                dict_list.append({})
                continue

            features ={}
            word = lines[line_index][column_index][0]
            pword = lines[line_index][column_index - 1][0]
            ppword = lines[line_index][column_index - 2][0]
            aword = lines[line_index][column_index + 1][0]
            aaword = lines[line_index][column_index + 2][0]
            t1 = lines[line_index][column_index - 1][2]
            t2t1 = lines[line_index][column_index - 2][2] + "_" + t1
            t2 = lines[line_index][column_index - 2][2]
            # features["index"] = str(column_index - 2)
            if pword != NONE:
                features["pw"] = pword
            if ppword != NONE:
                features["ppw"] = ppword
            if aword != NONE:
                features["aw"] = aword
            if aaword != NONE:
                features["aaw"] = aaword
            features["len"] = str(len(word))
            features["t1"] = t1
            # features["t2"] = t2
            features["t2t1"] = t2t1

            # if word in rare:
            #     features["israre"] = "True"
            # else:
            #     features["israre"] = "False"

            # if not rare
            # if word not in rare:
            if True:
                # pass
                features["form"] = word
            # rare
            # else:
            if True:
                if any([str(i) in word for i in range(10)]):
                    features["contNumber"] = "True"
                else:
                    features["contNumber"] = "False"

                if '-' in word:
                    features["contHyphen"] = "True"
                else:
                    features["contHyphen"] = "False"

                if any([letter in word for letter in string.ascii_uppercase]):
                    features["contUpper"] = "True"
                else:
                    features["contUpper"] = "False"

                mutual_suff = False
                mutual_pre = False
                for i in range(1, min(SR_TVAH + 1, len(word) + 1)):
                    end = len(word) - 1
                    if word[end - i + 1: end + 1].lower() in suffixes:
                        mutual_suff = True
                    features["suff" + str(i)] = word[end - i + 1: end + 1].lower()
                    if word[0: i].lower() in prefixes:
                        mutual_pre = True
                    features["pre" + str(i)] = word[0: i].lower()
                # features["mutual_suff"] = str(mutual_suff)
                # features["mutual_pre"] = str(mutual_pre)

            # lines[line_index][column_index][1] = features
            dict_list.append(features)

        # run the model on the column
        X = dv.transform(dict_list)
        tags = model.predict(X)
        for i, tag in enumerate(tags):
            if column_index >= len(lines[i]) - 2:
                continue
            lines[i][column_index][2] = tag

    with open(sys.argv[4], 'w') as output_file:
        for line in lines:
            output_file.write(" ".join([triplet[0]+"/"+triplet[2] for triplet in line[2:-2]]) + "\n")




if __name__ == '__main__':
    main()
