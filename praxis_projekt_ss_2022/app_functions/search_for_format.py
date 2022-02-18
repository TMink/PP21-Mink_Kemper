import os


# searches for files with specific format
def search_for_format(path: str, format: [str]):
    obj_list = []
    content_list = os.listdir(path)
    for elem in content_list:
        if any(word in elem for word in format):
            obj_list.append(elem)
    return obj_list
