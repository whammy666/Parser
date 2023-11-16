import pytest

from pars_html import parse_item_id

@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        ("/catalog/earring_146538.html", "earring_146538"),
        ("rfkrfkr/frjfnrjfnjr/catalog/earring_1463243847538.html", "earring_1463243847538")
    ]
)
def test_parse_item_id(test_input: str, expected_output: str) -> None:

    output = parse_item_id(test_input)
    assert output == expected_output

