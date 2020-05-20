import os

fileList = os.listdir("./txt")
print(fileList)
with open("pos.txt", 'w', encoding="utf-8") as pos, open(
        "neg.txt",
        'w', encoding="utf-8") as neg:
    neg_list = []
    pos_list = []
    for file in fileList:
        with open("./txt/" + file, "r", encoding="utf-8") as f:
            comment_list = f.readlines()
            if file.endswith("pos.txt"):
                pos_list = pos_list + comment_list
            else:
                neg_list = neg_list + comment_list
    pos.writelines(pos_list)
    neg.writelines(neg_list)
