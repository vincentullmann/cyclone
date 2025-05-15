import hou
import _hou  # type: ignore

# IMPORT LOCAL LIBRARIES
from .mixin import WrapMixin


class ObjNodeProxy(WrapMixin, hou.ObjNode):
    pass


class SopNodeProxy(WrapMixin, hou.SopNode):
    pass


# TODO:
# add a list of "class, func"-pairs:
# [
#  (hou.ObjNode, _hou.ObjNode_swigregister),
#  (hou.SopNode, _hou.SopNode_swigregister),
# ]


def apply() -> None:
    _hou.ObjNode_swigregister(ObjNodeProxy)
    _hou.SopNode_swigregister(SopNodeProxy)


def remove() -> None:
    # untested
    _hou.ObjNode_swigregister(hou.ObjNode)
    _hou.SopNode_swigregister(hou.SopNode)
