import pytest
from src.domain.item import Item
from src.domain.value_objects import Name
from src.domain.value_objects import Description


def test_domain_item_entity_validation_success():
    item = Item(id=1, name="valid", description="desc")
    assert item.id == 1
    assert item.name.value == "valid"
    assert item.description.value == "desc"

def test_domain_item_entity_empty_name():
    with pytest.raises(ValueError):
        Item(name="", description="desc")

def test_domain_item_entity_long_description():
    long_desc = "a" * 256
    with pytest.raises(ValueError):
        Item(name="valid", description=long_desc)

def test_domain_name_value_object_forbidden_word():
    for forbidden in ["禁止", "NG", "不適切"]:
        with pytest.raises(ValueError):
            Name(f"test{forbidden}")

def test_domain_description_value_object_length():
    long_desc = "a" * 256
    with pytest.raises(ValueError):
        Description(long_desc)
