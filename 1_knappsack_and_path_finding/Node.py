class Node:
    def __init__(self, id_node, benefit, weight, parent=None, left=None, right=None):
        self.id = id_node
        self.benefit = benefit
        self.weight = weight
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        return f"[ID:{self.id} B:{self.benefit} W:{self.weight}]"
