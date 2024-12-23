import pytest
from django.db import IntegrityError
from django.db.models.expressions import result

from ecommerce.inventory import models


@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, product_attribute, attribute_value",
    [
        (1, 1, "10"),
    ],
)
def test_inventory_db_product_attribute_value_dataset(
    db, db_fixture_setup, id, product_attribute, attribute_value
):
    result = models.ProductAttributeValue.objects.get(id=id)
    assert result.product_attribute.id == product_attribute
    assert result.attribute_value == attribute_value


def test_inventory_db_product_attribute_value_data(db, product_attribute_value_factory):
    new_attribute_value = product_attribute_value_factory.create(
        attribute_value="new_value", product_attribute__name="new_attribute"
    )
    assert new_attribute_value.attribute_value == "new_value"
    assert new_attribute_value.product_attribute.name == "new_attribute"


def test_inventory_db_insert_inventory_product_values(
    db, product_with_attribute_values_factory
):
    new_inv_attribute = product_with_attribute_values_factory(sku="12345678")
    result = models.ProductInventory.objects.get(sku="12345678")
    count = result.attribute_values.all().count()
    assert count == 2
