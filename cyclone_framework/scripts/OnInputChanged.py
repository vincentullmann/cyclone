"""
https://www.sidefx.com/docs/houdini/hom/locations.html#node_event_files
"""

# 🌀 IMPORT LOCAL LIBRARIES
from cyclone import events

kwargs: dict

events.emit("OnInputChanged", **kwargs)
