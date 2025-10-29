import sys
from unittest.mock import MagicMock

def pytest_sessionstart(session):
    # item_repositoryのBase.metadata.create_allをimport前にMock化
    sys.modules["employee.infrastructure.item_repository"] = MagicMock()
