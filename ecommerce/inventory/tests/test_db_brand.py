import pytest
from django.db import IntegrityError


def test_inventory_db_brand_insert_data(db, brand_factory):
    new_brand = brand_factory.create(name="new_brand")
    assert new_brand.name == "new_brand"


def test_inventory_db_brand_uniqueness_integrity(db, brand_factory):
    brand_factory.create(name="not_unique")
    with pytest.raises(IntegrityError):
        brand_factory.create(name="not_unique")
