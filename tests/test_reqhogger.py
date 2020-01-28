import os
from unittest import TestCase
from unittest.mock import patch

from tinydb.storages import JSONStorage, MemoryStorage

from hogger.reqhogger import RequestStorage


class RequestStorageTestCase(TestCase):
    def setUp(self):
        self.sample_data = {"name": "Neil Armstrong", "year": 1969}
        self.request_storage = RequestStorage()

    def tearDown(self):
        self.request_storage.clean()

    @patch.dict("os.environ", {"HOGGER_PERSIST": "1"})
    def test_instantiate_class_with_hogger_persist(self):
        self.assertEqual(os.environ["HOGGER_PERSIST"], "1")
        request_storage = RequestStorage()
        self.assertTrue(isinstance(request_storage.storage.storage, JSONStorage))
        request_storage.storage.close()

    def test_instantiate_class_without_hogger_persist(self):
        self.assertIsNone(os.environ.get("HOGGER_PERSIST"))
        request_storage = RequestStorage()
        self.assertTrue(isinstance(request_storage.storage.storage, MemoryStorage))

    def test_clean(self):
        self.request_storage.push(self.sample_data)
        self.assertEqual(len(self.request_storage.items), 1)
        self.request_storage.clean()
        self.assertEqual(len(self.request_storage.items), 0)

    def test_push(self):
        self.assertEqual(len(self.request_storage.items), 0)
        self.request_storage.push(self.sample_data)
        self.assertEqual(self.request_storage.items[0], self.sample_data)

    def test_delete(self):
        self.request_storage.push(self.sample_data)
        self.assertEqual(len(self.request_storage.items), 1)
        self.request_storage.delete(1)
        self.assertEqual(len(self.request_storage.items), 0)

    def test_items(self):
        self.request_storage.push(self.sample_data)
        self.assertEqual(self.request_storage.items, [self.sample_data])
