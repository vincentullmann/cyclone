# IMPORT THIRD PARTY LIBRARIES
from typing import Any
import hou


class BaseNode:
    """Generic Base Node Class providing common functions"""

    defaults: dict[str, Any] = {}
    """Dict of default values for node parameters."""

    def __init__(self, node: hou.OpNode) -> None:
        self.node = node

    ############################################################################
    # Utility Functions

    def parm(self, name: str) -> hou.Parm:
        """Return the parameter at the given path.

        Opposed to the factory `hou.Node.parm` this function will raise an Error
        if the parm is not found.
        This allows for simpler code in a controlled environment where parameters
        can be assumed to exist.

        Args:
            name (str): name of the parameter

        Raises:
            AttributeError: if the parameter doesn't exist.

        Returns:
            hou.Parm: the parameter

        """
        parm = self.node.parm(name)
        if parm:
            return parm
        else:
            raise AttributeError("Invalid parm: %s", name)

    def set_parm(self, name: str, value: Any) -> None:
        self.parm(name).set(value)

    ############################################################################
    # Features

    def OnCreated(self, node: hou.OpNode, type: hou.nodeType) -> None:

        # set default values
        for name, value in self.defaults.items():
            self.set_parm(name, value)
