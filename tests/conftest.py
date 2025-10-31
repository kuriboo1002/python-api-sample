import sys
from unittest.mock import MagicMock

from employee.infrastructure.item_repository_adapter import ItemRepositoryAdapterInterface

class MockItemRepositoryAdapter(ItemRepositoryAdapterInterface):
    def get_by_id(self, item_id: int):
        return None
    def get_all(self):
        return []
    def update(self, item_id: int, req):
        return None
    def delete(self, item_id: int):
        return False
    def create(self, req):
        return None

def pytest_sessionstart(session):
    # item_repositoryのBase.metadata.create_allをimport前にMock化
    sys.modules["employee.infrastructure.item_repository"] = MagicMock()
