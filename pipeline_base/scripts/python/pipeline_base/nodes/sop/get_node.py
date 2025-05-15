# IMPORT THIRD PARTY LIBRARIES
from typing import Any
import hou

# IMPORT LOCAL LIBRARIES
from cyclone.logger import logger
from cyclone.nodes.base import BaseNode


class GetNode(BaseNode):
    """
    Get a node from the Houdini scene.
    """

    defaults = {
        "source": "initial source",
    }

    def __init__(self, node: hou.SopNode) -> None:
        """Initialize the GetNode class."""
        super().__init__(node)

        self.x = 0
        self._source_node: hou.OpNode | None = None
        # self.node.addParmCallback(self._source_changed, ("source",))

        # init
        self.source_changed()

    ############################################################################

    def button_pick_clicked(self) -> None:

        path = hou.ui.selectNode(
            # relative_to_node=self.node,
            # initial_node=self.node,
            title="Select a node",
            # node_type_filter=hou.nodeTypeFilter.Parms,
            multiple_select=False,
            custom_node_filter_callback=self.node_filter,
        )
        if isinstance(path, str):
            self.set_parm("source", path)

    def button_jump_clicked(self) -> None:

        if not self._source_node:
            return

        # TODO: there must be an easier way
        for pane in [
            hou.ui.paneTabUnderCursor(),
            *hou.ui.currentPaneTabs(),
        ]:
            if pane and isinstance(pane, hou.NetworkEditor):  #  pane.type() == hou.paneTabType.NetworkEditor:
                pane.setCurrentNode(self._source_node)
                pane.homeToSelection()  # type: ignore[attr-defined]  # not sure where this comes from.
                return

    def source_menu(self) -> list[str]:
        nodes = hou.node("/").allSubChildren(recurse_in_locked_nodes=True)  # type: ignore[union-attr]
        nodes = [node for node in nodes if self.node_filter(node)]
        paths = [self.node.relativePathTo(node) for node in nodes]
        paths = [path for path in paths for _ in range(2)]
        return paths

    def node_filter(self, node: hou.Node) -> bool:
        node_type = node.type().name()

        allowed_types = {"output"}
        if node_type in allowed_types:
            return True

        name = node.name()
        if name.isupper():
            return True

        # failed all tests
        return False

    ################################################################################

    def source_changed(self, **kwargs: Any) -> None:
        # node: hou.OpNode = None, parm_tuple: hou.ParmTuple = None,

        # remove old callbacks
        if self._source_node:
            try:
                self._source_node.removeEventCallback((hou.nodeEventType.AppearanceChanged,), self._source_appearance_changed)
                self._source_node.removeEventCallback((hou.nodeEventType.NameChanged,), self._source_name_changed)
            except hou.OperationFailed:
                # callback was not added
                pass

        parm = self.parm("source")
        self._source_node = parm.evalAsNode()
        if self._source_node:
            self._source_node.addEventCallback((hou.nodeEventType.AppearanceChanged,), self._source_appearance_changed)
            self._source_node.addEventCallback((hou.nodeEventType.NameChanged,), self._source_name_changed)

    def _source_appearance_changed(self, node: hou.OpNode, change_type: hou.appearanceChangeType, **kwargs: Any) -> None:

        print("[_source_appearance_changed]", kwargs)
        if self._source_node is None:
            return

        if change_type == hou.appearanceChangeType.Color:
            self.node.setColor(node.color())

    def _source_name_changed(self, node: hou.OpNode, **kwargs: Any) -> None:
        print("[_source_name_changed]", kwargs)

        parm = self.parm("source")

        path = parm.evalAsString()
        is_absolute = path.startswith("/")

        if is_absolute:
            parm.set(node.path())
        else:
            parm.set(self.node.relativePathTo(node))
