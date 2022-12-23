import pytest

from testing_containers.db.db import Repo


@pytest.fixture(scope="class", name="repo")
def repo(request):
    """Instantiates a database object"""
    db = Repo()
    try:
        request.cls.repo = db
        yield db
    finally:
        db.close()
