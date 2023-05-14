import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    # print vec1, vec2
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    return Counter(WORD.findall(text))

def get_similarity(a, b):
    a = text_to_vector(a.strip().lower())
    b = text_to_vector(b.strip().lower())

    return get_cosine(a, b)

def initialize_name_1(name):
    name = name.split(", ")
    if len(name) > 1:
        first_name = name[-1]
    else:
        return name[0]
    initialized_firstname = first_name[0] + "."
    return name[0] + initialized_firstname

def initialize_name_2(name):
    name = name.split(", ")
    if len(name) > 1:
        first_name = name[0]
    else:
        return name[0]
    initialized_firstname = first_name[0]
    return name[1] + initialized_firstname

def comparing(name1,name2):
    name11 = initialize_name_1(name1)
    name12 = initialize_name_2(name1)
    name21 = initialize_name_1(name2)
    name22 = initialize_name_2(name2)

    k = 0
    if get_similarity(name11,name21) > 0.8 or get_similarity(name11,name22) > 0.8:
        k = k + 1
    if get_similarity(name12, name21) > 0.8 or get_similarity(name12, name22) > 0.8:
        k = k + 1
    if k > 0:
        return 1
    else:
        return 0



