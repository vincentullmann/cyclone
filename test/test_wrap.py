#!/usr/bin/env hython.exe


"""
Run on Windows:
>>> export PATH="/mnt/c/Program Files/Side Effects Software/Houdini 20.5.550/bin":${PATH}
>>> hython.exe test/test_wrap.py
"""

import unittest
import hou


# print("=== 1")
#
# obj = hou.node("/obj")
# cam = obj.createNode("cam", "my_cam")
# print(repr(cam))

# geo = obj.createNode("geo")
# obj.createNode("null")
#
# get_node = geo.createNode("me::get_node::1.0")
# # print(get_node)
# print("1 > ", get_node.x)
# print("1 > ", get_node.x)
# print("1 > ", get_node.x)
# print("1 > ", get_node.x)
# print("------------------")
#
#
# get_node2 = hou.node("/obj/geo1/get_node1")
# print("2 >", get_node2.x)


#
#  foobar()


class TestStringMethods(unittest.TestCase):

    def setUp(self):

        self.node_obj = hou.node("/obj")
        self.node_geo = self.node_obj.createNode("geo")

    def test_has_instance_attributes(self):

        # todo: replace with a mock class?
        test = self.node_geo.createNode("me::get_node::1.0")
        self.assertIsInstance(test.x, int)
        self.assertEqual(test.x, 0)

    def test_share_instance_state(self):
        # print(">>>>>> [test_share_instance_state] start")

        # todo: replace with a mock class?
        inst_a = self.node_geo.createNode("me::get_node::1.0")
        inst_b = hou.node(inst_a.path())

        self.assertEqual(inst_a.x, inst_b.x)

        inst_a.x = 5
        self.assertEqual(inst_a.x, inst_b.x)

        inst_b.x = 8
        self.assertEqual(inst_a.x, inst_b.x)
        # print(">>>>>> [test_share_instance_state] done")

    def test_raise(self):

        with self.assertRaises(AttributeError):
            self.node_geo.foobar

    def test_delete(self):

        # todo: replace with a mock class?
        node = self.node_obj.createNode("null")

        from cyclone.wrapping import mixin

        mixin.wrap_node(node)

        key = mixin.get_key(node)

        assert key in mixin._WRAPPED_NODE_CACHE

        node.destroy()

        assert key not in mixin._WRAPPED_NODE_CACHE


if __name__ == "__main__":
    unittest.main()

#
# node_obj = hou.node("/obj")
# node_geo = node_obj.createNode("geo")
# node_geo.destroy()


# print(obj.children())

# print(123, cam.test123())
# print(123, cam.test345())


# print(cam.__repr__())

# print("=== 2 type(cam)", type(cam))
# print("=== 3", cam.path())
# print("=== 3 type(cam)", type(cam))
# print("=== 4", cam.path())
# print("=== 4 type(cam)", type(cam))
# print("=== 5", cam.test123())
# print("=== 5 type(cam)", type(cam))


# print(2, cam.path())

# print("@@@ cam", cam)
# print("@@@ type(cam)", type(cam))
# print("@@@ cam.path()", cam.path())
