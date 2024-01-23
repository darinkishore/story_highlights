import pytest
from transformations.dat.colors import (color_mappings, get_color_mapping,
                                        get_reverse_color_mapping)


@pytest.mark.parametrize("key, expected_color", [
    ("Main Male Character", "#1155cc"),
    ("Male Character 4", "#a4c2f4"),
    ("Antagonist", "#ff0000"),
    ("Nonexistent Character", None),
])
def test_get_color_mapping(key, expected_color):
    if expected_color is not None:
        assert get_color_mapping(key) == expected_color
    else:
        with pytest.raises(KeyError):
            get_color_mapping(key)

@pytest.mark.parametrize("value, expected_key", [
    ("#1155cc", "Main Male Character"),
    ("#abcdef", None),
])
def test_get_reverse_color_mapping(value, expected_key):
    if expected_key is not None:
        assert get_reverse_color_mapping(value) == expected_key
    else:
        with pytest.raises(KeyError):
            get_reverse_color_mapping(value)
