import math

def get_file(filename):
    with open(filename, "r") as file:
        count = 0
        for f in file:
            new_token_dict = {}
            token_list = f.strip().replace("'", "").split(": ")
            token = token_list[0]
            token_dic = eval(token_list[1])
            document_f = len(token_dic)
            for i in token_dic:
                term_f = token_dic[i]
                new_token_dict[str(i)] = "{:.3f}".format(calculate_score(term_f, document_f, 55393))
            new_sorted_dic = {}
            for i, j in sorted(new_token_dict.items()):
                new_sorted_dic[i] = j
            new_sorted_str = "{}= {}\n".format(token, str(new_sorted_dic).replace("'", ""))
            with open("tfidf.txt", "a") as tf_file:
                tf_file.write(new_sorted_str)
            print("processing {} tokens".format(count))
            count += 1


def calculate_score(term_frequency, document_frequency, num_of_documents):
    weighted_term_frequency = 1 + math.log(term_frequency, 10)
    weighted_document_frequency = math.log(num_of_documents / document_frequency, 10)
    score = weighted_term_frequency * weighted_document_frequency
    return score



if __name__ == "__main__":
    file_name = "whole.txt"
    get_file(file_name)
