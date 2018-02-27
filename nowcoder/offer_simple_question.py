# -*- coding:utf-8 -*-
class Solution:
    """
    请实现一个函数，将一个字符串中的空格替换成“%20”。例如，当字符串为We Are Happy.则经过替换之后的字符串为We%20Are%20Happy。
    """

    # s 源字符串
    def replaceSpace(self, s):
        # write code here
        result = s.replace(" ", "%20")
        return result


class NodeOfLinkedList:
    def __init__(self, val):
        self.value = val
        self.pre = None
        self.nex = None


class Solution1:
    """输入一个链表，从尾到头打印链表每个节点的值。"""

    def printListFromTailToHead(self, listNode):
        ll = [listNode.value]
        tmp = listNode.nex
        while tmp:
            ll.insert(0, tmp.value)
            tmp = tmp.nex
        return ll

    def gen_test(self):
        node5 = NodeOfLinkedList(5)
        node4 = NodeOfLinkedList(4)
        node3 = NodeOfLinkedList(3)
        node2 = NodeOfLinkedList(2)
        node1 = NodeOfLinkedList(1)
        node1.nex = node2
        node2.nex = node3
        node3.nex = node4
        node4.nex = node5
        node2.pre = node1
        node3.pre = node2
        node4.pre = node3
        node5.pre = node4
        return node1


class Solution2:
    """输入某二叉树的前序遍历和中序遍历的结果，请重建出该二叉树。假设输入的前序遍历和中序遍历的结果中都不含重复的数字。
        例如输入前序遍历序列{1,2,4,7,3,5,6,8}和中序遍历序列{4,7,2,1,5,3,8,6}，则重建二叉树并返回。
    """

def wrapper(fun):
    def inner():
        wrapper_inner = 0
        print "begin"
        fun()
        print "end"

    return inner

@wrapper
def test_wrapper():
    print "fun"


if __name__ == "__main__":
    test_wrapper()

    so = Solution()
    print so.replaceSpace("We Are Happy.")

    so1 = Solution1()
    print so1.printListFromTailToHead(so1.gen_test())
