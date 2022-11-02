import pickle
from nltk.stem import PorterStemmer
import time
import re

def stemming_input(user_input):
    user_token_list = user_input.strip().split(" ")
    normalized_token_list = []
    porter_stem = PorterStemmer()
    for i in user_token_list:
        normalized_token_list.append(porter_stem.stem(i))
    return normalized_token_list


def get_inverted_index(token, pickle_folder):
    try:
        if token.isalpha():
            if len(token) == 1:
                pickle_file_name = "{}/{}.pkl".format(pickle_folder, token * 2)
            else:
                pickle_file_name = "{}/{}.pkl".format(pickle_folder, token[:2])
            with open(pickle_file_name, "rb") as pickle_file:
                load_tuple = pickle.load(pickle_file)
                while load_tuple[0] != token:
                    load_tuple = pickle.load(pickle_file)
                token_dic = load_tuple[1]

        else:
            pickle_file_name = "{}/special.pkl".format(pickle_folder)
            with open(pickle_file_name, "rb") as pickle_file:
                load_tuple = pickle.load(pickle_file)
                while load_tuple[0] != token:
                    load_tuple = pickle.load(pickle_file)
                token_dic = load_tuple[1]

    except EOFError as e:
        return tuple()
    return token_dic


def merge_list(lst):
    final_tuple = lst[0]
    for i in range(1, len(lst)):
        same_token = []
        key_sequence1 = final_tuple
        key_sequence2 = lst[i]
        index1 = 0
        index2 = 0
        while index1 < len(key_sequence1) and index2 < len(key_sequence2):
            word1 = key_sequence1[index1][0]
            word2 = key_sequence2[index2][0]
            if word1 < word2:
                index1 += 1
            elif word1 > word2:
                index2 += 1
            else:
                same_token.append((word1, key_sequence1[index1][1] + key_sequence2[index2][1]))
                index1 += 1
                index2 += 1
        final_tuple = tuple(same_token)
    return list(final_tuple)


def find_max_id(lst):
    lst = [i for i in sorted(lst, key=lambda x: x[1])]
    result = []
    if len(lst) > 5:
        new_five_tuple = lst[len(lst) - 5:]
        for i in new_five_tuple:
            result.append(i[0])
    else:
        for j in lst:
            result.append(j[0])
    return result


def top_links(top_ids, doc_id_dic):
    for i in top_ids:
        print(doc_id_dic[i])


if __name__ == "__main__":

    folderpath = r'D:\Tool\PycharmProject\INFAssignment3\27pickle'
    with open("document_id.pkl", "rb") as file:
        document_id_dic = pickle.load(file)
    print('***** Search Engine Starts! *****')
    command = ''
    while command != 'N':
        str_input = str(input('Search[Type anything]: ')).lower()
        words = re.sub(r'[^0-9a-zA-Z]+', ' ', str_input.lower()).strip()
        start = time.time()
        print("Program Start")
        stemmed_token_list = stemming_input(words)
        token_list = []
        for token in stemmed_token_list:
            unsorted_tuple = get_inverted_index(token, folderpath)
            sorted_tuple = tuple([i for i in sorted(list(unsorted_tuple), key=lambda x: x[0])])
            token_list.append(sorted_tuple)
        if len(token_list) > 1:
            token_list = merge_list(token_list)
            max_doc_id_list = find_max_id(token_list)
        elif len(token_list) == 1:
            max_doc_id_list = find_max_id(list(token_list[0]))
        else:
            max_doc_id_list = []

        print('\nHere are the top results:\n')
        top_links(max_doc_id_list, document_id_dic)

        end = time.time()
        print("Total execution time: " + str(end - start) + " seconds.")
        command = str(input('\nContinue?(Y\\N)'))
