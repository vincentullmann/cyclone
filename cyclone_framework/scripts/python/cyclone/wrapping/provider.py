"""Each Provider Class/Instance offers a different way to manage node classes"""

# IMPORT STANDARD LIBRARIES
import functools
import importlib
import inspect

# IMPORT THIRD PARTY LIBRARIES
import hou

# IMPORT LOCAL LIBRARIES
from cyclone.utils.text import CustomFormatter


class NodeClassProvider:
    """Base Provider Class"""

    def get(self, node_type: hou.NodeType) -> type[hou.Node] | None:
        raise NotImplementedError

    def reload(self, node_type: hou.NodeType) -> None:
        """reload the custom class registered for the given node type."""
        cls = self.get(node_type)
        if not cls:
            return

        module = inspect.getmodule(cls)
        if module:
            importlib.reload(module)


class RegistryProvider(NodeClassProvider):
    """Provider managing a registry to node classes."""

    def __init__(self) -> None:
        self._registry: dict[hou.NodeType, type] = {}

    def register(self, node_type: hou.NodeType, cls: type[hou.Node]) -> None:
        """Register a custom class for a specific Houdini node type."""
        self._registry[node_type] = cls

    def unregister(self, node_type: hou.NodeType) -> None:
        """Unregister a class for a given node type."""
        self._registry.pop(node_type, None)

    def get(self, node_type: hou.NodeType) -> type[hou.Node] | None:
        return self._registry.get(node_type)


class DynamicImportProvider(NodeClassProvider):
    def __init__(
        self,
        import_template: str = "nodes.{base}.{category}.{type}.Node",
    ) -> None:
        self.import_template = import_template
        self.formatter = CustomFormatter()

    def format_template(self, node_type: hou.NodeType) -> str:

        category = node_type.category().typeName().lower()
        # components used in the HDA-Manager
        scope, namespace, name, version = hou.hda.componentsFromFullNodeTypeName(node_type.name())

        context = {
            "category": category,
            "scope": scope,
            "namespace": namespace,
            "name": name,
            "version": version,
        }
        return self.formatter.format(self.import_template, **context)

    def get(self, node_type: hou.NodeType) -> type[hou.Node] | None:

        import_template = self.format_template(node_type)
        mod_path, class_name = import_template.rsplit(".", 1)

        try:
            mod = importlib.import_module(mod_path)
            return getattr(mod, class_name, None)
        except ImportError:
            return None


class CompositeProvider(NodeClassProvider):
    """Provider combining multiple child providers"""

    def __init__(self) -> None:

        registry = RegistryProvider()
        # forward the key methods
        self.register = registry.unregister
        self.unregister = registry.unregister

        self.providers: list[NodeClassProvider] = [
            registry,
        ]
        """list of registered providers, checked in order."""

    ##################
    # Overrides

    @functools.lru_cache(maxsize=None)
    def get(self, node_type: hou.NodeType) -> type[hou.Node] | None:
        for provider in self.providers:
            cls = provider.get(node_type)
            if cls:
                return cls

        return None

    def reload(self, node_type: hou.NodeType) -> None:

        # functools does not offer an easy method to clear specific keys
        # from the cache. Apparently there is some undocumented ".cache" dict
        # but lets stay with the official methods for now.
        # This is likely only used during development/debugging and not relevant
        # for production
        self.get.cache_clear()

        for provider in self.providers:
            provider.reload(node_type)

    ##################
    # new

    def add_import_path(self, path: str) -> None:
        """Add a new import path to the provider.

        args:
            path: the template path to add.

        """
        provider = DynamicImportProvider(path)
        self.providers.append(provider)


WrapClassProvider = CompositeProvider()
