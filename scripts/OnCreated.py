"""
https://www.sidefx.com/docs/houdini/hom/locations.html#node_event_files
"""

# 🌀 IMPORT LOCAL LIBRARIES
from cyclone.core import events

kwargs: dict

events.emit("OnCreated", **kwargs)
