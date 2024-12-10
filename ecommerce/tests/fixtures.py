import pytest


@pytest.fixture
def create_admin_user(django_user_model):
    """
    Return admin user
    :param django_user_model:
    :return:
    """
    return django_user_model.objects.create_superuser("admin", "a@a.com", "password")
