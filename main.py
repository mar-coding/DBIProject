from module.Tree import BPlusTree


def main():
    bpt = BPlusTree(order=4)
    bpt.insert(10, 20)
    bpt.insert(22, 20)
    bpt.insert(45, 20)
    bpt.insert(26, 20)
    bpt.insert(12, 20)
    bpt.insert(8, 20)
    bpt.insert(7, 20)
    bpt.insert(6, 20)
    bpt.insert(9, 20)
    bpt.insert(4, 20)
    bpt.insert(5, 20)
    # bpt.delete(26)
    # bpt.delete(6)

    # print(bpt)
    bpt.printTree()
    # bpt.showAllData()


if __name__ == "__main__":
    main()
