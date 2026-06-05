from pathlib import Path

import pytest


_TEST_DATA = Path(__file__).parent / "resources"


@pytest.fixture
def test_data():
    return _TEST_DATA
