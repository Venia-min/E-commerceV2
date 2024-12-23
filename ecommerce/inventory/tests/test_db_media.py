import pytest

from ecommerce.inventory import models


@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, product_inventory, image, alt_text, is_feature, created_at, updated_at",
    [
        (
            1,
            1,
            "images/default.png",
            "a default image solid color",
            1,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
        ),
        (
            8616,
            8616,
            "images/default.png",
            "a default image solid color",
            1,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
        ),
    ],
)
def test_inventory_db_media_dataset(
    db,
    db_fixture_setup,
    id,
    product_inventory,
    image,
    alt_text,
    is_feature,
    created_at,
    updated_at,
):
    result = models.Media.objects.get(id=id)
    result_created_at = result.created_at.strftime("%Y-%m-%d %H:%M:%S")
    result_updated_at = result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    assert result.product_inventory.id == product_inventory
    assert result.image == image
    assert result.alt_text == alt_text
    assert result.is_feature == is_feature
    assert result_created_at == created_at
    assert result_updated_at == updated_at


def test_inventory_db_media_insert_data(db, media_factory):
    new_media = media_factory.create(product_inventory__sku="12345678")
    assert new_media.product_inventory.sku == "12345678"
    assert new_media.image == "images/default.png"
    assert new_media.alt_text == "a default image solid color"
    assert new_media.is_feature == 1
