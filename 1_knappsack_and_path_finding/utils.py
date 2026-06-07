
formatted_string = lambda path: "\n".join([f"  Not selected: ID {n['id']}"
                                   if n['benefit'] == 0 and n['weight'] == 0
                                       else f"  ID: {n['id']} | B: {n['benefit']} | W: {n['weight']}"
                                       for n in path])

formatted_string_accumulative_left = lambda path: "\n".join([f"  Not selected: ID {path[i]['id']}"
                                           if i != len(path) - 1
                                              and path[i]['benefit'] == path[i+1]['benefit']
                                              and path[i]['weight'] == path[i+1]['weight']
                                           else f"  ID: {path[i]['id']} | B: {path[i]['benefit']} | W: {path[i]['weight']}"
                                           for i in range(len(path))])

weight_accumulated = lambda node_path: sum([element["weight"] for element in node_path])

filter_by_size = lambda my_list, size: list(filter(lambda x: len(x) == size, my_list))

# def get_smallest_2d_list(d2_list, index):
#     return d2_list
#     pass

def readData(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.readlines()

    except FileNotFoundError:
        exit(f"Error: The file '{path}' was not found.")

