import pytest
from employee.application.item_schemas import ItemUpdateRequest, ItemCreateRequest

def test_schema_item_update_request_validation_success():
    req = ItemUpdateRequest(name="valid", description="desc")
    assert req.name == "valid"
    assert req.description == "desc"

def test_schema_item_update_request_validation_empty_name():
    with pytest.raises(ValueError):
        ItemUpdateRequest(name="", description="desc")

def test_schema_item_update_request_validation_long_description():
    long_desc = "a" * 256
    with pytest.raises(ValueError):
        ItemUpdateRequest(name="valid", description=long_desc)

def test_schema_item_create_request_success():
    req = ItemCreateRequest(name="newitem", description="desc")
    assert req.name == "newitem"
    assert req.description == "desc"

def test_schema_item_create_request_empty_name():
    with pytest.raises(ValueError):
        ItemCreateRequest(name="", description="desc")

def test_schema_item_create_request_long_description():
    long_desc = "a" * 256
    with pytest.raises(ValueError):
        ItemCreateRequest(name="valid", description=long_desc)
