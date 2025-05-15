from typing import Callable

import hou
import _hou  # type: ignore

# IMPORT LOCAL LIBRARIES
from .mixin import WrapMixin


# to avoid unnecessary patching only the types of nodes that we currently use
# is added here.
NODE_HOOKS: list[tuple[type[hou.Node], Callable[[type[hou.Node]], None]]] = [
    (hou.ObjNode, _hou.ObjNode_swigregister),
    (hou.SopNode, _hou.SopNode_swigregister),
    (hou.RopNode, _hou.RopNode_swigregister),
    (hou.LopNode, _hou.LopNode_swigregister),
]


def apply() -> None:
    """Install our hooks in the Houdini API."""
    for node_class, swigregister_func in NODE_HOOKS:

        ProxyClass = type(node_class.__name__ + "Proxy", (WrapMixin, node_class), {})
        swigregister_func(ProxyClass)


def remove() -> None:
    # untested
    for node_class, swigregister_func in NODE_HOOKS:
        swigregister_func(node_class)
