# IMPORT STANDARD LIBRARIES
import string


class CustomFormatter(string.Formatter):
    """Custom Formatter adding support for different string transformations.

    Example:
    >>> formatter = CustomFormatter()
    >>> formatter.format("Hello {name:upper}", name="foo")
    'Hello FOO'

    >>> formatter.format("Hello {name:camelcase}", name="some_name")
    'Hello SomeName'

    """

    def format_field(self, value: str, format_spec: str) -> str:

        if format_spec.lower() == "upper":
            return value.upper()
        if format_spec.lower() == "capitalize":
            return value.capitalize()
        if format_spec.lower() == "camelcase":
            return "".join(word.capitalize() for word in str(value).split("_"))

        return super().format_field(value, format_spec)  # type: ignore  # format_field has no type hint
