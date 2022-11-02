from bs4 import BeautifulSoup
from posting import Posting
from nltk.stem import PorterStemmer
import json
import os
import time
import re


start = time.time()
print("Program Start")

# Key: number, Value: url
url_dict = {}
url_id = 0

# inverted index. Key: token, Value: [postings]
word_dict = {}

# Key: token, Value: field
word_field_dict = {}

# directory for getting json file
directory = r"D:\UCIrvine\INF 141\Assignment3\DEV"

# directory for mapping document id with document url
url_id_directory = r"D:\Tool\PycharmProject\INFAssignment3\document_id.txt"

# directory for mapping token with postings
token_directory = r"D:\Tool\PycharmProject\INFAssignment3\token"

# collect the number of unique token
token_count = set()

# the format for tokenization
token_format = r"[0-9a-z\s]+"

tag_score = {"p": 1, "b": 10, "strong": 15, "h6": 20, "h5": 25, "h4": 30, "h3": 35, "h2": 40, "h1": 45, "title": 50}


def read_files_from_dir(path_to_DEV):
    # an empty list to store all file and sub-directory paths
    list_of_all_file_paths = []
    # get a list of sub-directory names from the given path
    subdir_list = os.listdir(path_to_DEV)
    # iterate through the list of file and sub-directory names
    for file in subdir_list:
        # get the path of that file
        file_path = os.path.join(path_to_DEV, file)
        # get a list of json file names from the given path
        json_directory = os.listdir(file_path)
        for json_file in json_directory:
            json_path = r"{}".format(os.path.join(file_path, json_file))
            # add each file path to the list
            list_of_all_file_paths.append(json_path)
    # count how many files in the list
    count_files = len(list_of_all_file_paths)
    # [0] is the list of all file paths,
    # [1] is the total number of files.
    return [list_of_all_file_paths, count_files]


# Get the content inside the file
def get_file(filename):
    with open(filename, "r") as file:
        json_parse = json.load(file)
    return json_parse


# Get the url name
def get_url(content_dict):
    return content_dict["url"]


# Tokenize the content based on token_format criteria
def tokenization(text):
    result_token_list = []
    porter_stem = PorterStemmer()
    pattern = re.compile(token_format)
    token_list = re.findall(pattern, text)
    medium_token_list = "".join(token_list).split()
    for i in medium_token_list:
        normalized_word = porter_stem.stem(i)
        result_token_list.append(normalized_word)
    return result_token_list


# Get the actual content of the file
def get_content(content_dict):
    html_content = content_dict["content"]
    for field in tag_score:
        field_content_list = BeautifulSoup(html_content, "lxml").find_all(field)
        for field_content_html in field_content_list:
            field_content = field_content_html.text.lower()
            parsed_field_content_list = tokenization(field_content)
            if field not in word_field_dict:
                word_field_dict[field] = parsed_field_content_list
            else:
                word_field_dict[field] += parsed_field_content_list
    return word_field_dict


def create_posting(token, doc_id, field_name):
    if token not in word_dict:
        new_posting = Posting(doc_id, tag_score[field_name])
        word_dict[token] = [new_posting]
    else:
        posting_list = word_dict[token]
        count = 0
        for i in range(len(posting_list)):
            if posting_list[i].get_id() == doc_id:
                new_occurrence = posting_list[i].get_tfidf() + tag_score[field_name]
                new_posting = posting_list[i]
                new_posting.set_tfidf(new_occurrence)
                posting_list[i] = new_posting
                break
            else:
                count += 1
        if count == len(posting_list):
            word_dict[token].append(Posting(doc_id, tag_score[field_name]))


def create_url_dictionary(url):
    if url not in url_dict:
        url_dict[url_id] = url


# Write url dictionary to file
def url_write_to_txt(dictionary, txt_name):
    with open(txt_name, 'a+', encoding='utf-8', errors='ignore') as file:
        for document_id, document_url in dictionary.items():
            file.write("{}: {}\n".format(str(document_id), document_url))


# Write word dictionary to file
def token_write_to_txt(token_dictionary):
    a = ""
    word_file = r"{}".format(os.path.join(token_directory, r"{}.txt".format(url_id)))
    with open(word_file, 'a+', encoding='utf-8', errors='ignore') as file:
        for i in token_dictionary:
            token_count.add(i)
            a += i + " = {"
            for j in token_dictionary[i]:
                a += j.result_posting() + "}\n"
        file.write(a)


# Read file from DEV
result_list = read_files_from_dir(directory)
json_list = result_list[0]
doc_num = result_list[1]

# count report
total_token_count = 0


for j in json_list:
    # Get the file from document into file
    json_content_dict = get_file(j)

    # Append the url into url_dict
    file_url = get_url(json_content_dict)
    create_url_dictionary(file_url)

    # Get parsed content
    parsed_content_dict = get_content(json_content_dict)

    # Create word posting
    for f in parsed_content_dict:
        word_list = parsed_content_dict[f]
        for word in word_list:
            create_posting(word, url_id, f)

    # print out report
    print("running url_id:", url_id)
    total_token_count += len(word_dict)
    print("totally", total_token_count, "tokens with duplication")

    # Write url id dictionary into file
    url_write_to_txt(url_dict, url_id_directory)
    token_write_to_txt(word_dict)

    # Plus the document id with 1
    url_id += 1

    # clear url_dict and word_dict
    url_dict = {}
    word_dict = {}

print("There are", len(token_count), "unique tokens.")
end = time.time()
print("Total execution time: " + str(end - start) + " seconds.")
