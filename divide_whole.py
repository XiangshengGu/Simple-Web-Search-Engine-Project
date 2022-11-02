

first_name = ""
count = 0
with open("tfidf.txt", "r") as tfidf_file:
    for f in tfidf_file:
        name = f.split("= ")[0]
        if name.isalpha():
            first_name = name[0]
        else:
            first_name = "special"
        with open(r"D:\Tool\PycharmProject\INFAssignment3\27pickle\{}.txt".format(first_name), "a") as token_file:
            token_file.write(f)
        print("working with {} and the number of token is {}".format(name, count))
        count += 1
