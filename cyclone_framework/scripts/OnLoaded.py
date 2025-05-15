"""
https://www.sidefx.com/docs/houdini/hom/locations.html#node_event_files
"""

# 🌀 IMPORT LOCAL LIBRARIES
from cyclone import events

kwargs: dict

events.emit("OnLoaded", **kwargs)

node = kwargs.get("node")
if node and hasattr(node, "OnLoaded"):
    node.OnLoaded()
