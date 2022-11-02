from os import listdir
import pickle

txt_file_path = r"D:\Tool\PycharmProject\INFAssignment3\27files"
pickle_file_path = r"D:\Tool\PycharmProject\INFAssignment3\27pickle"

count = 0
for txt_file_name in listdir(txt_file_path):
    pickle_file_name = ""
    current_first_name = ""
    with open(r"{}\{}".format(txt_file_path, txt_file_name), "r") as txt_file:
        for line in txt_file:
            line_list = line.rstrip().split("= ")
            token_name = line_list[0]
            token_dic = eval(line_list[1].replace("{", "((").replace(", ", "), (").replace(":", ",").replace("}", "))"))
            if token_name.isalpha():
                if len(token_name) == 1:
                    current_first_name = token_name * 2
                else:
                    current_first_name = token_name[:2]
                with open(r"{}\{}.pkl".format(pickle_file_path, current_first_name), "ab") as pickle_file:
                    pickle.dump((token_name, token_dic), pickle_file)
            else:
                with open(r"{}\special.pkl".format(pickle_file_path), "ab") as pickle_file:
                    pickle.dump((token_name, token_dic), pickle_file)

            print("name = {}, num = {}".format(token_name, count))
            count += 1
