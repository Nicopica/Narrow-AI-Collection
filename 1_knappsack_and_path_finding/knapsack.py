from Node import *

EMPTY_VALUE = (0, 0) # Weight and Benefit. The id will be the same on each level
MAX_CAPACITY = 420
DATA_PATH_KNAPSACK = "data/knapsack.txt"

def build_binary_tree(tree, data):
    if not data:
        return tree

    if tree.left is None and tree.right is None:
        id_node, benefit, weight = data[0]

        tree.left = Node(id_node, EMPTY_VALUE[0], EMPTY_VALUE[1], parent=tree)
        tree.right = Node(id_node, benefit, weight, parent=tree)

        build_binary_tree(tree.left, data[1:])
        build_binary_tree(tree.right, data[1:])

    return tree


def get_path_to_root(node):
    if node.parent is None:
        return []

    current_element = {"id": node.id,
                       "weight": node.weight,
                       "benefit": node.benefit}

    return [current_element] + get_path_to_root(node.parent)


def build_binary_tree_only_possible_solutions(tree, data):
    if not data:
        return tree

    id_node, item_benefit, item_weight = data[0]

    new_total_weight = tree.weight + item_weight
    new_total_benefit = tree.benefit + item_benefit

    tree.left = Node(id_node, tree.benefit, tree.weight, parent=tree)

    build_binary_tree_only_possible_solutions(tree.left, data[1:])

    if new_total_weight <= MAX_CAPACITY:
        tree.right = Node(id_node, new_total_benefit, new_total_weight, parent=tree)
        build_binary_tree_only_possible_solutions(tree.right, data[1:])

    return tree


def get_all_leaves(tree):
    if tree is None:
        return []

    if tree.left is None and tree.right is None:
        return [tree]

    solutions = []

    if tree.left:
        solutions.extend(get_all_leaves(tree.left))

    if tree.right:
        solutions.extend(get_all_leaves(tree.right))

    return solutions



def dfs(root, max_capacity):
    best_benefit = 0
    best_node = root

    stack = [(root, 0, 0)]

    while stack:
        node, acc_w, acc_b = stack.pop()

        current_weight = acc_w + node.weight
        current_benefit = acc_b + node.benefit

        if current_weight > max_capacity:
            continue

        if current_benefit > best_benefit:
            best_benefit = current_benefit
            best_node = node

        if node.left:
            stack.append((node.left, current_weight, current_benefit))
        if node.right:
            stack.append((node.right, current_weight, current_benefit))

    return best_benefit, best_node



def bfs(root, max_capacity):
    best_benefit = 0
    best_node = root

    queue = [(root, 0, 0)]

    while queue:
        node, acc_w, acc_b = queue.pop(0)

        current_weight = acc_w + node.weight
        current_b = acc_b + node.benefit

        if current_weight > max_capacity:
            continue

        if current_b > best_benefit:
            best_benefit = current_b
            best_node = node

        if node.left:
            queue.append((node.left, current_weight, current_b))
        if node.right:
            queue.append((node.right, current_weight, current_b))

    return best_benefit, best_node

