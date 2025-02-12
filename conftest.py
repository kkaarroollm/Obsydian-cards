import typing
from pathlib import Path

import pytest
from faker import Faker

from app.models import Tag


@pytest.fixture(scope="session")
def get_fixture_md() -> typing.Callable[[str], str]:
    def wrapper(name: str) -> str:
        path = Path(__file__).parent.resolve() / "tests" / "fixtures"
        with open(path / name, "r") as file_:
            return file_.read()

    return wrapper


@pytest.fixture(scope="function")
def get_empty_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("notes")


@pytest.fixture(scope="function")
def get_files_dir(get_empty_dir: Path, get_fixture_md: typing.Callable[[str], str]) -> typing.Callable[..., Path]:
    def wrapper(*filenames: str) -> Path:
        for filename in filenames:
            content = get_fixture_md(filename)
            (get_empty_dir / filename).write_text(content, encoding="utf-8")
        return get_empty_dir

    return wrapper


@pytest.fixture(scope="session", autouse=True)
def fake() -> typing.Generator[Faker, None, None]:
    fake = Faker()
    Faker.seed(42)
    yield fake


@pytest.fixture
def tags(fake: Faker) -> set[Tag]:
    return {Tag(tag=fake.pystr()) for _ in range(3)}
