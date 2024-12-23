import pytest
from django.db import IntegrityError

from ecommerce.inventory import models


@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, name, description",
    [
        (1, "men-shoe-size", "men shoe size"),
    ],
)
def test_inventory_db_product_attribute_dataset(
    db, db_fixture_setup, id, name, description
):
    result = models.ProductAttribute.objects.get(id=id)
    assert result.name == name
    assert result.description == description


def test_inventory_db_product_attribute_insert_data(db, product_attribute_factory):
    new_attribute = product_attribute_factory.create()
    assert new_attribute.name == "attribute_name_0"
    assert new_attribute.description == "description_0"


def test_inventory_db_product_attribute_uniqueness_integrity(
    db, product_attribute_factory
):
    product_attribute_factory.create(name="not_unique")
    with pytest.raises(IntegrityError):
        product_attribute_factory.create(name="not_unique")
