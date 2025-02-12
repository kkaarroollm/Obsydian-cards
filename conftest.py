import typing

import pytest
from faker import Faker


@pytest.fixture(scope="session", autouse=True)
def fake() -> typing.Generator[Faker, None, None]:
    fake = Faker()
    Faker.seed(42)
    yield fake


@pytest.fixture
def tags(fake: Faker) -> set[str]:
    return {fake.unique.word() for _ in range(3)}
