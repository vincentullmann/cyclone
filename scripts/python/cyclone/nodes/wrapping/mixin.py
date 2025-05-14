# IMPORT STANDARD LIBRARIES

# IMPORT THIRD PARTY LIBRARIES
import hou  # type: ignore[reportMissingModuleSource]

# IMPORT LOCAL LIBRARIES
from cyclone.core import events
from cyclone.nodes.wrapping.provider import WrapClassProvider


cache_key = tuple[str, int]


_WRAPPED_NODE_CACHE: dict[cache_key, hou.Node | None] = {}
"""Map to store wrapped Nodes.

tbd: using a `WeakValueDictionary` might be a good Idea here but might also lead
to counter-intuitive behavior if NodeClasses store/init values in their `__init__`
methods. (said that..  they probl. shouldn't do that.)
"""


def get_key(node: hou.Node) -> cache_key:
    """Given a hou.Node object, determine the key we should track
    the node type with in the internal _objectmap of SuperNode
    """
    return (node.type().nameWithCategory(), node.sessionId())


def clear_node_cache(event: events.Event, node: hou.Node, **kwargs) -> None:
    """Remove a node from the wrap cache"""
    key = get_key(node)
    _WRAPPED_NODE_CACHE.pop(key, None)


def wrap_node(node: hou.Node) -> hou.Node | None:
    key = get_key(node)

    # reuse
    if key in _WRAPPED_NODE_CACHE:
        return _WRAPPED_NODE_CACHE[key]

    # wrap
    cls = WrapClassProvider.get(node.type())
    if cls:
        wrapped = cls(node)
    else:
        wrapped = None

    # store and return
    _WRAPPED_NODE_CACHE[key] = wrapped
    return _WRAPPED_NODE_CACHE[key]


class WrapMixin(hou.Node):
    """Mixin to proxy attribute access to a custom-wrapped class if defined."""

    def _wrapped_node(self) -> hou.Node | None:
        return wrap_node(self)

    def reload(self):
        WrapClassProvider.reload(self.type())
        clear_node_cache(None, self)
        self._wrapped_node()

    def __getattr__(self, name: str):
        wrapped = self._wrapped_node()

        if name in wrapped.__dir__():
            return getattr(wrapped, name)
        else:
            raise AttributeError("NodeType %r has no attribute %r" % (self.type().nameWithCategory(), name))

    def __setattr__(self, name, value):
        if name == "this":  # Needed by Houdini's SWIG init
            return super().__setattr__(name, value)

        wrapped_node = self._wrapped_node()
        if hasattr(wrapped_node, name):
            return setattr(wrapped_node, name, value)
        return super().__setattr__(name, value)

    def __dir__(self):
        wrapped = self._wrapped_node()
        if not wrapped:
            return super().__dir__()

        # combine the __dir__ of both
        return set(super().__dir__()) | set(dir(wrapped))

    @property
    def __doc__(self):
        wrapped = self._wrapped_node()
        if not wrapped:
            return super().__doc__
        return wrapped.__doc__

    def __repr__(self):
        wrapped = self._wrapped_node()
        if not wrapped:
            return super().__repr__()

        cls = type(wrapped)
        return f"<{cls.__module__}.{cls.__name__}(type={self.type().name()} path={self.path()})>"


################################################################################
# Forward various events


@events.on("OnCreated")
@events.on("OnLoaded")
@events.on("OnNameChanged")
@events.on("OnInputChanged")
def on_cleared(event: events.Event, node: hou.Node, **kwargs):
    wrapped = wrap_node(node)

    # run `wrapped.OnCreated()` for any event type
    func = getattr(wrapped, event.name, None)
    if callable(func):
        func(**kwargs)


@events.on("OnDeleted")
def on_deleted(node: hou.Node, **kwargs):

    key = get_key(node)
    wrapped = _WRAPPED_NODE_CACHE.pop(key, None)

    if wrapped and hasattr(wrapped, "OnDeleted"):
        wrapped.OnDeleted()
