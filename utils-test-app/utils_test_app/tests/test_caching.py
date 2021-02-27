from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase

from app_utils.caching import ObjectCacheMixin


CURRENT_PATH = "utils_test_app.tests.test_caching"
fake_objects = dict()


class FakeManager(ObjectCacheMixin):
    def create(self, name):
        pk = len(fake_objects) + 1
        fake_objects[pk] = self.model(pk, name)
        return fake_objects[pk]

    def get(self, pk):
        return fake_objects[pk]

    def select_related(self, query):
        return self

    @property
    def model(self):
        return FakeModel


class _FakeMeta:
    def __init__(self, app_label, model_name) -> None:
        self.app_label = app_label
        self.model_name = model_name


class FakeModel:
    def __init__(self, pk, name) -> None:
        self.pk = pk
        self.name = name

    _meta = _FakeMeta("dummy", "fakemodel")
    objects = FakeManager()


@patch(
    CURRENT_PATH + ".FakeManager._fetch_object_for_cache",
    wraps=FakeModel.objects._fetch_object_for_cache,
)
class TestObjectCacheMixin(TestCase):
    def setUp(self) -> None:
        self.obj = FakeModel.objects.create(name="My Fake Model")
        cache.clear()

    def test_get_cached_1(self, mock_fetch_object_for_cache):
        """when cache is empty, load from DB"""
        obj = FakeModel.objects.get_cached(pk=self.obj.pk)

        self.assertEqual(obj.name, "My Fake Model")
        self.assertEqual(mock_fetch_object_for_cache.call_count, 1)

    def test_get_cached_2(self, mock_fetch_object_for_cache):
        """when cache is not empty, load from cache"""
        obj = FakeModel.objects.get_cached(pk=self.obj.pk)

        obj = FakeModel.objects.get_cached(pk=self.obj.pk)

        self.assertEqual(obj.name, "My Fake Model")
        self.assertEqual(mock_fetch_object_for_cache.call_count, 1)

    def test_get_cached_3(self, mock_fetch_object_for_cache):
        """when cache is empty, load from DB"""
        obj = FakeModel.objects.get_cached(pk=self.obj.pk, select_related="dummy")

        self.assertEqual(obj.name, "My Fake Model")
        self.assertEqual(mock_fetch_object_for_cache.call_count, 1)
