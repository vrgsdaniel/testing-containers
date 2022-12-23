import pytest
from psycopg2.errors import UniqueViolation

from testing_containers.db.db import Repo
from testing_containers.model.users import User


@pytest.mark.usefixtures("repo")
class TestRepo:
    def test_insert_users(self):
        repo: Repo = self.repo
        alice = User(name="alice", email="alice@example.com")
        bob = User(name="bob", email="bob@example.com")
        robert = User(name="robert", email="bob@example.com")
        users = [alice, bob]
        # check that the users are not there
        result = repo.get_user("alice")
        assert result is None

        # check that the users are there
        repo.insert_users(users)
        result = repo.get_user("alice")
        assert result == alice
        result = repo.get_user("bob")
        assert result == bob

        # check that pk fails
        with pytest.raises(UniqueViolation):
            repo.insert_users([robert])
