import sys
import string

START = '*START*'
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
        words_with_tags = line.split(' ')
        for word_and_tag in words_with_tags:
            word, tag = word_and_tag.rsplit('/', 1)
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
    output_file = open(sys.argv[2], 'w')

    count = counter(train_data)
    rare = dict((k, v) for k, v in count.items() if v <= 5)
    print(rare)

    for line in train_data:
        ptag = START
        pptag = START

        words_with_tags = line.split(' ')
        for i, word_and_tag in enumerate(words_with_tags):
            word, tag = word_and_tag.rsplit('/',1)
            features = tag
            features += " " + "len=" + str(len(word))
            # features += " " + "index=" + str(i)
            features += " " + "t1=" + ptag
            # features += " " + "t2=" + pptag
            features += " " + "t2t1=" + pptag + "_" + ptag
            pptag = ptag
            ptag = tag

            pword, ppword, aword, aaword = NONE, NONE, NONE, NONE
            if i == 0:
                pass
            elif i == 1:
                pword = words_with_tags[0].rsplit('/',1)[0]
            else:
                pword = words_with_tags[i-1].rsplit('/', 1)[0]
                ppword = words_with_tags[i-2].rsplit('/', 1)[0]

            if i == len(words_with_tags) - 2:
                aword = words_with_tags[len(words_with_tags) - 1].rsplit('/',1)[0]
            elif i == len(words_with_tags) - 1:
                pass
            else:
                aword = words_with_tags[i+1].rsplit('/', 1)[0]
                aaword = words_with_tags[i+2].rsplit('/', 1)[0]

            if ppword != NONE:
                features += " " + "ppw=" + ppword
            if pword != NONE:
                features += " " + "pw=" + pword
            if aword != NONE:
                features += " " + "aw=" + aword
            if aaword != NONE:
                features += " " + "aaw=" + aaword


            # if word not in rare:
            if True:
                features += " " + "form=" + word
            # rare
            # else:
            if True:
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

                mutual_suff = False
                mutual_pre = False
                for i in range(1, min(SR_TVAH + 1, len(word) + 1)):
                    end = len(word) - 1
                    if word[end-i + 1 : end + 1].lower() in suffixes:
                        mutual_suff = True
                    features += " " + "suff" + str(i) + "=" + word[end-i + 1 : end + 1].lower()
                    if word[0 : i].lower() in prefixes:
                        mutual_pre = True
                    features += " " + "pre" + str(i) + "=" + word[0 : i].lower()

                # features += " " + "mutual_suff=" + str(mutual_suff)
                # features += " " + "mutual_pre=" + str(mutual_pre)



            output_file.write(features + "\n")


    output_file.close()


if __name__ == '__main__':
    main()
