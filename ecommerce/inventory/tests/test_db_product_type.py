import pytest
from django.db import IntegrityError


def test_inventory_db_producttype_insert_data(db, product_type_factory):
    new_type = product_type_factory.create(name="new_type")
    assert new_type.name == "new_type"


def test_inventory_db_producttype_uniqueness_integrity(db, product_type_factory):
    product_type_factory.create(name="not_unique")
    with pytest.raises(IntegrityError):
        product_type_factory.create(name="not_unique")
