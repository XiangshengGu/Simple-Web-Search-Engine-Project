import pickle

with open("document_id.txt", "r") as file:
    new_list = {}
    for f in file:
        line_list = f.strip().split(": ")

        new_list[int(line_list[0])] = line_list[1]
        print(line_list)
    with open("document_id.pkl", "ab") as pickle_file:
        pickle.dump(new_list, pickle_file)
