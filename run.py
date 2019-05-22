import numpy as np
import matplotlib.pyplot as plt
import string
import random


class Node:
    max_depth = -1

    def __init__(self):
        self.left = None
        self.right = None
        self.depth = None
        self.width = None

    def create_location(self, start=0.1, end=0.9, depth=0):
        mid = start + (end - start) / 2
        Node.max_depth = max(Node.max_depth, depth)
        self.depth = depth
        self.width = mid

        if self.left:
            self.left.create_location(start, mid, depth + 1)
        if self.right:
            self.right.create_location(mid, end, depth + 1)

    def node_plot(self, parent=None, color='b'):
        if parent:
            px, py = parent.width, 1 - parent.depth / (Node.max_depth + 1)
            sx, sy = self.width, 1 - self.depth / (Node.max_depth + 1)
            X = (px, sx)
            Y = (py, sy)
            plt.scatter(X, Y)
            print(X, Y)
            if self.__getattribute__('color') is not None:
                is_red = self.__getattribute__('color')
                if is_red:
                    color = "red"
                else:
                    color = "black"

            plt.plot(X, Y, color=color)
        if self.left:
            self.left.node_plot(parent=self)
        if self.right:
            self.right.node_plot(parent=self)

    def plot(self):
        self.create_location()
        self.node_plot()
        plt.pause(.1)
        plt.clf()


class TreeNode(Node):
    def __init__(self, key, val, color):
        super(TreeNode, self).__init__()
        self.key = key
        self.val = val
        self.color = color
        self.left = None
        self.right = None


class LLRBT():
    RED = True
    BLACK = False

    def __init__(self):
        self.root = None

    def get(self, key):
        x = self.root
        while x is not None:
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x.val

        return None

    def isRed(self, x):
        if x is None:
            return False

        return x.color is LLRBT.RED

    def rotateLeft(self, h):

        assert self.isRed(h.right)

        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = self.RED
        return x

    def rotateRight(self, h):
        assert self.isRed(h.left)
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = self.RED
        return x

    def flipColor(self, h):
        assert self.isRed(h) is False
        assert self.isRed(h.left) is True
        assert self.isRed(h.right) is True

        h.color = LLRBT.RED
        h.left.color = LLRBT.BLACK
        h.right.color = LLRBT.BLACK

    def _put(self, h, key, val):
        if h is None:
            return TreeNode(key, val, LLRBT.RED)

        if key < h.key:
            h.left = self._put(h.left, key, val)
        elif key > h.key:
            h.right = self._put(h.right, key, val)
        else:
            h.val = val

        if (self.isRed(h.right)) and (not self.isRed(h.left)):
            h = self.rotateLeft(h)
        if self.isRed(h.left) and self.isRed(h.left.left):
            h = self.rotateRight(h)
        if self.isRed(h.left) and self.isRed(h.right):
            self.flipColor(h)

        return h

    def put(self, key, val):
        self.root = self._put(self.root, key, val)
        self.root.color = LLRBT.BLACK


if __name__ == '__main__':
    rb_tree = LLRBT()

    data = list(range(pow(2, 6) - 1))
    # random.shuffle(data)
    for i in data:
        rb_tree.put(i, 0)
        rb_tree.root.plot()
    plt.show()
