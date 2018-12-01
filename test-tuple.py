
def tuple2str(tp):
    return " ".join([str(item) for item in tp])


def str2tuple(s):
    lst = s.split(" ")
    return lst

tp = (3,4,6)

print(tuple2str(tp))