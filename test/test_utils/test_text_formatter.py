# IMPORT THIRD PARTY LIBRARIES
import pytest

# IMPORT LOCAL LIBRARIES
from cyclone.utils.text import CustomFormatter


@pytest.fixture
def formatter():
    return CustomFormatter()


def test_upper(formatter):
    assert formatter.format("Hello {name:upper}", name="foo") == "Hello FOO"


def test_capitalize(formatter):
    assert formatter.format("Hello {name:capitalize}", name="foo") == "Hello Foo"


def test_camelcase(formatter):
    assert formatter.format("Hello {name:camelcase}", name="some_name") == "Hello SomeName"


def test_no_format_spec(formatter):
    assert formatter.format("Hello {name}", name="foo") == "Hello foo"
