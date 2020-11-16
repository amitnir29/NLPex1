import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
import sys

MAPPINGFILE = "feature_map_file"

def main():
    input_file = open(sys.argv[1], 'r')
    # each line is a sentence
    train_data = input_file.read().splitlines()
    input_file.close()

    dv = DictVectorizer(sparse=True)
    # print(dv)
    x_all_dicts = []
    y_labels = []
    for line in train_data:
        new_line = "labal=" + line
        x_line_dict = {}
        y_line, x_line = new_line.split(' ', 1)
        for key_and_value in x_line.split(' '):
            #print(key_and_value)
            key, value = key_and_value.split('=', 1)
            x_line_dict[key] = value
        x_all_dicts.append(x_line_dict)

        # y_line_dict = {}
        for key_and_value in y_line.split(' '):
            # print(key_and_value)
            key, value = key_and_value.split('=', 1)
            y_labels.append(value)
            # y_line_dict[key] = value
        # y_all_dicts.append(x_line_dict)

    # print(x_all_dicts)
    X = dv.fit_transform(x_all_dicts)
    # print(X.shape[0])
    # print(len(y_labels))
    # Y = dv.fit_transform(y_all_dicts)
    # print(X)
    # print(Y)

    model = LogisticRegression(multi_class="multinomial", max_iter=350)
    # model = SGDClassifier(loss='log')

    model = model.fit(X, y_labels)
    #
    pickle.dump(model, open(sys.argv[2], 'wb'))
    pickle.dump(dv, open(MAPPINGFILE, 'wb'))




    '''
    X = []
    Y = []

    for line in train_data:
        y,x = line.split(' ', 1)
        dv = DictVectorizer(x)
        X.append(x)
        Y.append(y)

    print(X, Y)
    '''

    #
    # output_file = open(sys.argv[2], 'w')
    # output_file.close()


if __name__ == '__main__':
    main()
    #v = DictVectorizer()
    #D = [{'foo': 'a', 'bar': 'b'}, {'foo': 'c', 'baz': 'b'}]
    #X = v.fit_transform(D)
    #print(X)
    #print(v.vocabulary_)
