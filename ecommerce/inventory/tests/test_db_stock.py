import pytest

from ecommerce.inventory import models


@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, product_inventory, last_checked, units, units_sold",
    [
        (1, 1, "2021-09-04 22:14:18", 135, 0),
        (8616, 8616, "2021-09-04 22:14:18", 100, 0),
    ],
)
def test_inventory_db_stock_dataset(
    db,
    db_fixture_setup,
    id,
    product_inventory,
    last_checked,
    units,
    units_sold,
):
    result = models.Stock.objects.get(id=id)
    result_last_checked = result.last_checked.strftime("%Y-%m-%d %H:%M:%S")
    assert result.product_inventory.id == product_inventory
    assert result_last_checked == last_checked
    assert result.units == units
    assert result.units_sold == units_sold


def test_inventory_db_stock_insert_data(db, stock_factory):
    new_stock = stock_factory.create(product_inventory__sku="12345678")
    assert new_stock.product_inventory.sku == "12345678"
    assert new_stock.units == 2
    assert new_stock.units_sold == 100
