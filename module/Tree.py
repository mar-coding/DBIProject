from __future__ import annotations

from math import floor
from random import randint


class Node:
    uidCounter = 0

    # order is holding branching factor
    def __init__(self, order):
        Node.uidCounter += 1
        self.order = order
        self.parent: Node = None
        self.keys = []
        self.values = []
        self.uid = self.uidCounter

    # Split a full Node to two new ones.
    def split(self) -> Node:
        left = Node(self.order)
        right = Node(self.order)
        mid = int(self.order // 2)
        left.parent = right.parent = self
        left.keys = self.keys[:mid]
        left.values = self.values[:mid + 1]
        right.keys = self.keys[mid + 1:]
        right.values = self.values[mid + 1:]

        # Setup the pointers to child nodes.
        self.values = [left, right]

        # Hold the first element from the right subtree.
        self.keys = [self.keys[mid]]

        # Setup correct parent for each child node.
        for child in left.values:
            if isinstance(child, Node):
                child.parent = left

        for child in right.values:
            if isinstance(child, Node):
                child.parent = right

        # Return the 'top node'
        return self

    def getSize(self) -> int:
        return len(self.keys)

    def isEmpty(self) -> bool:
        return len(self.keys) == 0

    def isFull(self) -> bool:
        return len(self.keys) == self.order - 1

    def isNearlyUnderflow(self) -> bool:
        return len(self.keys) <= floor(self.order / 2)

    def isUnderflow(self) -> bool:
        return len(self.keys) <= floor(self.order / 2) - 1

    def isRoot(self) -> bool:
        return self.parent is None


class LeafNode(Node):
    def __init__(self, order):
        super().__init__(order)

        self.prevLeaf: LeafNode = None
        self.nextLeaf: LeafNode = None

    def add(self, key, value):

        # Insert key if it doesn't exist
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return

        # Otherwise, search key and append value.
        for i, item in enumerate(self.keys):

            # Key found => Append Value
            if key == item:
                self.values[i].append(value)
                break

            # Key not found && key < item => Add key before item.
            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            # Key not found here. Append it after.
            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    # Split a full leaf node.
    def split(self) -> Node:
        top = Node(self.order)
        right = LeafNode(self.order)
        mid = int(self.order // 2)
        self.parent = right.parent = top
        right.keys = self.keys[mid:]
        right.values = self.values[mid:]
        right.prevLeaf = self
        right.nextLeaf = self.nextLeaf
        top.keys = [right.keys[0]]

        # Setup the pointers to child nodes.
        top.values = [self, right]
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]

        # Setup pointer to next leaf
        self.nextLeaf = right
        return top


class BPlusTree(object):
    def __init__(self, order):

        # First node must be leaf (to store data)
        self.root: Node = LeafNode(order)
        self.order: int = order

    @staticmethod
    # return right-most node/pointer.
    def _find(node: Node, key):
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i
            elif i + 1 == len(node.keys):
                return node.values[i + 1], i + 1

    @staticmethod
    def _mergeUp(parent: Node, child: Node, index):
        parent.values.pop(index)
        pivot = child.keys[0]
        for c in child.values:
            if isinstance(c, Node):
                c.parent = parent

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break
            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def checkAfterDelete(self):
        root = self.root
        if not root.isEmpty():
            qu = [root, 0]
            while len(qu) > 0:
                node = qu.pop(0)
                height = qu.pop(0)

                if not isinstance(node, LeafNode):
                    qu += self.intersperse(node.values, height + 1)
                    if not node.keys:
                        # get all child from parent node then use rightmost for key of parent node
                        child = node.values.pop()
                        node.values.append(child)
                        properKey = child.keys[0]
                        node.keys.append(properKey)
                        pass

    def insert(self, key, value):
        node = self.root

        # While we are in internal nodes... search for leafs.
        while not isinstance(node, LeafNode):
            node, index = self._find(node, key)

        # Node is now guaranteed a LeafNode!
        node.add(key, value)

        while len(node.keys) == node.order:
            if not node.isRoot():
                parent = node.parent
                node = node.split()
                jnk, index = self._find(parent, node.keys[0])
                self._mergeUp(parent, node, index)
                node = parent
            else:
                node = node.split()
                self.root = node

    def retrieve(self, key):
        node = self.root
        while not isinstance(node, LeafNode):
            node, index = self._find(node, key)

        for i, item in enumerate(node.keys):
            if key == item:
                return node.values[i]

        return None

    def delete(self, key):
        node = self.root

        while not isinstance(node, LeafNode):
            node, parentIndex = self._find(node, key)

        if key not in node.keys:
            return False

        index = node.keys.index(key)

        # Remove the last inserted data.
        node.values[index].pop()

        if len(node.values[index]) == 0:
            # Remove the list element.
            node.values.pop(index)
            node.keys.pop(index)

            while node.isUnderflow() and not node.isRoot():
                prevSibling = BPlusTree.getPrevSibling(node)
                nextSibling = BPlusTree.getNextSibling(node)
                jnk, parentIndex = self._find(node.parent, key)

                if prevSibling and not prevSibling.isNearlyUnderflow():
                    self._borrowLeft(node, prevSibling, parentIndex)
                elif nextSibling and not nextSibling.isNearlyUnderflow():
                    self._borrowRight(node, nextSibling, parentIndex)
                elif prevSibling and prevSibling.isNearlyUnderflow():
                    self._mergeOnDelete(prevSibling, node)
                elif nextSibling and nextSibling.isNearlyUnderflow():
                    self._mergeOnDelete(node, nextSibling)

                node = node.parent

            if node.isRoot() and not isinstance(node, LeafNode) and len(node.values) == 1:
                self.root = node.values[0]
                self.root.parent = None
        self.checkAfterDelete()

    @staticmethod
    def _borrowLeft(node: Node, sibling: Node, parentIndex):
        if isinstance(node, LeafNode):
            key = sibling.keys.pop(-1)
            data = sibling.values.pop(-1)
            node.keys.insert(0, key)
            node.values.insert(0, data)
            node.parent.keys[parentIndex - 1] = key
        else:
            parent_key = node.parent.keys.pop(-1)
            sibling_key = sibling.keys.pop(-1)
            data: Node = sibling.values.pop(-1)
            data.parent = node
            node.parent.keys.insert(0, sibling_key)
            node.keys.insert(0, parent_key)
            node.values.insert(0, data)

    @staticmethod
    def _borrowRight(node: LeafNode, sibling: LeafNode, parentIndex):
        if isinstance(node, LeafNode):
            key = sibling.keys.pop(0)
            data = sibling.values.pop(0)
            node.keys.append(key)
            node.values.append(data)
            node.parent.keys[parentIndex] = sibling.keys[0]
        else:
            parent_key = node.parent.keys.pop(0)
            sibling_key = sibling.keys.pop(0)
            data: Node = sibling.values.pop(0)
            data.parent = node
            node.parent.keys.append(sibling_key)
            node.keys.append(parent_key)
            node.values.append(data)

    @staticmethod
    def _mergeOnDelete(l_node: Node, r_node: Node):
        parent = l_node.parent
        jnk, index = BPlusTree._find(parent, l_node.keys[0])
        parent_key = parent.keys.pop(index)
        parent.values.pop(index)
        parent.values[index] = l_node

        if isinstance(l_node, LeafNode) and isinstance(r_node, LeafNode):
            l_node.nextLeaf = r_node.nextLeaf
        else:
            l_node.keys.append(parent_key)
            for r_node_child in r_node.values:
                r_node_child.parent = l_node

        l_node.keys += r_node.keys
        l_node.values += r_node.values

    @staticmethod
    def getPrevSibling(node: Node) -> Node:
        if node.isRoot() or not node.keys:
            return None
        jnk, index = BPlusTree._find(node.parent, node.keys[0])
        return node.parent.values[index - 1] if index - 1 >= 0 else None

    @staticmethod
    def getNextSibling(node: Node) -> Node:
        if node.isRoot() or not node.keys:
            return None
        jnk, index = BPlusTree._find(node.parent, node.keys[0])

        return node.parent.values[index + 1] if index + 1 < len(node.parent.values) else None

    def printTree(self):
        if self.root.isEmpty():
            print('The b++ Tree is empty!')
            return
        queue = [self.root, 0]

        while len(queue) > 0:
            node = queue.pop(0)
            height = queue.pop(0)

            if not isinstance(node, LeafNode):
                queue += self.intersperse(node.values, height + 1)
            print('lvl ' + str(height), '|'.join(map(str, node.keys)), ' -->\t current -> ', node.uid,
                  '\t parent -> ',
                  node.parent.uid if node.parent else None)

    def getLeftmostLeaf(self):
        if not self.root:
            return None

        node = self.root
        while not isinstance(node, LeafNode):
            node = node.values[0]

        return node

    def getRightmostLeaf(self):
        if not self.root:
            return None

        node = self.root
        while not isinstance(node, LeafNode):
            node = node.values[-1]

    def showAllData(self):
        node = self.getLeftmostLeaf()
        if not node:
            return None

        while node:
            for node_data in node.values:
                print('[{}]'.format(', '.join(map(str, node_data))), end=' -> ')

            node = node.nextLeaf
        print('Last node')

    def showAllDataReverse(self):
        node = self.getRightmostLeaf()
        if not node:
            return None

        while node:
            for node_data in reversed(node.values):
                print('[{}]'.format(', '.join(map(str, node_data))), end=' <- ')
            node = node.prevLeaf
        print()

    @staticmethod
    def intersperse(lst, item):
        result = [item] * (len(lst) * 2)
        result[0::2] = lst
        return result
