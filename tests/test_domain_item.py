import pytest

def test_domain_item_entity_validation_success():
    from employee.domain.item import Item
    item = Item(name="valid", description="desc")
    assert item.name.value == "valid"
    assert item.description.value == "desc"

def test_domain_item_entity_empty_name():
    from employee.domain.item import Item
    with pytest.raises(ValueError):
        Item(name="", description="desc")

def test_domain_item_entity_long_description():
    from employee.domain.item import Item
    long_desc = "a" * 256
    with pytest.raises(ValueError):
        Item(name="valid", description=long_desc)

def test_domain_name_value_object_forbidden_word():
    from employee.domain.value_objects import Name
    for forbidden in ["禁止", "NG", "不適切"]:
        with pytest.raises(ValueError):
            Name(f"test{forbidden}")

def test_domain_description_value_object_length():
    from employee.domain.value_objects import Description
    long_desc = "a" * 256
    with pytest.raises(ValueError):
        Description(long_desc)
