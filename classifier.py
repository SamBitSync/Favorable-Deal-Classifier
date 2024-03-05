import pandas as pd
import numpy as np
from graphviz import Digraph


class Node:
    def __init__(self, attribute=None, category=None, left=None, right=None, value=None):
        self.attribute = attribute  # Split attribute
        self.category = category  # Category for nominal attributes
        self.left = left  # Left child (subtree)
        self.right = right  # Right child (subtree)
        self.value = value  # Class label (for leaf nodes)


def entropy(y):
    classes, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)
    return -np.sum(probs * np.log2(probs))


def information_gain(X, y, attribute, category=None):
    if category is not None:
        left_mask = X[:, attribute] == category
        right_mask = ~left_mask
        left_entropy = entropy(y[left_mask])
        right_entropy = entropy(y[right_mask])
        left_weight = np.sum(left_mask) / len(y)
        right_weight = 1 - left_weight
        return entropy(y) - (left_weight * left_entropy + right_weight * right_entropy)
    else:
        attribute_values = np.unique(X[:, attribute])
        gain = entropy(y)
        for value in attribute_values:
            mask = X[:, attribute] == value
            gain -= np.sum(mask) / len(y) * entropy(y[mask])
        return gain


def gain_ratio(X, y, attribute, category=None):
    gain = information_gain(X, y, attribute, category)
    split_info = split_information(X, attribute, category)
    return gain / split_info if split_info != 0 else 0


def split_information(X, attribute, category=None):
    if category is not None:
        left_mask = X[:, attribute] == category
        right_mask = ~left_mask
        left_weight = np.sum(left_mask) / len(X)
        right_weight = 1 - left_weight
        return -(left_weight * np.log2(left_weight) + right_weight * np.log2(right_weight))
    else:
        attribute_values, counts = np.unique(X[:, attribute], return_counts=True)
        probs = counts / len(X)
        return -np.sum(probs * np.log2(probs))


def find_best_split(X, y, feature_names):
    best_attribute = None
    best_category = None
    best_gain = -np.inf
    for attribute in range(X.shape[1]):
        values = np.unique(X[:, attribute])
        if len(values) == 1:  # Skip if only one value
            continue
        for category in values:
            gain = gain_ratio(X, y, attribute, category)
            if gain > best_gain:
                best_attribute = attribute
                best_category = category
                best_gain = gain
    return best_attribute, best_category


def build_tree(X, y, feature_names):
    if len(np.unique(y)) == 1:
        return Node(value=y[0])
    best_attribute, best_category = find_best_split(X, y, feature_names)
    if best_attribute is None:
        return Node(value=np.argmax(np.bincount(y)))
    left_mask = X[:, best_attribute] == best_category
    right_mask = ~left_mask
    left_subtree = build_tree(X[left_mask], y[left_mask], feature_names)
    right_subtree = build_tree(X[right_mask], y[right_mask], feature_names)
    return Node(attribute=best_attribute, category=best_category, left=left_subtree, right=right_subtree)


def visualize_tree(node, feature_names, class_labels, dot=None):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='box')

    if node.value is not None:
        class_label = class_labels[node.value]
        dot.node(str(id(node)), label=class_label)
    else:
        if node.attribute is not None and node.category is not None:
            attribute_name = feature_names[node.attribute]
            category = node.category
            label = f"{attribute_name} = {category}"
        else:
            label = "Decision Criteria"
        dot.node(str(id(node)), label=label)
        if node.left is not None:
            dot.edge(str(id(node)), str(id(node.left)), label=f"{attribute_name} = {category}")
            visualize_tree(node.left, feature_names, class_labels, dot)
        if node.right is not None:
            dot.edge(str(id(node)), str(id(node.right)), label=f"{attribute_name} != {category}")
            visualize_tree(node.right, feature_names, class_labels, dot)
    return dot



# Loading the synthetic data
synthetic_data = pd.read_excel('data.xlsx')

# Convert nominal attributes into one-hot encoded format
X = pd.get_dummies(synthetic_data.drop(columns=['Favorable Deal']))

# Convert "Good Deal" and "Bad Deal" to binary labels
y = (synthetic_data['Favorable Deal'] == 'Good Deal').astype(int).values

feature_names = X.columns.tolist()

# Build the decision tree
root = build_tree(X.values, y, feature_names)

# Visualize the decision tree
class_labels = ['Bad Deal', 'Good Deal']
dot = visualize_tree(root, feature_names, class_labels)
dot.render('decision_tree', format='png', cleanup=True)
