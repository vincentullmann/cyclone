import hou  # type: ignore[reportMissingModuleSource]


class Cam(hou.ObjNode):

    def __init__(self, node=None):
        print("MyCameraNode.__my_init__")
        self.i = 0

    def count(self):
        self.i += 1
        print("Counter: ", self.i)

    def test123(self):
        return "MyCameraNode.test123"

    def OnDeleted(self):
        print("deleting camera node")
