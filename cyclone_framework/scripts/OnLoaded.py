"""
https://www.sidefx.com/docs/houdini/hom/locations.html#node_event_files
"""

# IMPORT STANDARD LIBRARIES
import typing

# 🌀 IMPORT LOCAL LIBRARIES
from cyclone import events

kwargs: dict[str, typing.Any]

events.emit("OnLoaded", **kwargs)
