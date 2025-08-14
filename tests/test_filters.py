import pytest

from loganalyzer.filters import (
    create_date_filter,
    create_user_agent_filter,
    validate_date,
)


def test_validate_date_valid():
    validate_date("2023-01-01")


def test_validate_date_invalid():
    with pytest.raises(ValueError):
        validate_date("2023-13-01")


def test_user_agent_filter():
    filter_func = create_user_agent_filter("TestAgent")
    entry = {"http_user_agent": "TestAgent"}
    assert filter_func(entry) is True

    entry = {"http_user_agent": "WrongAgent"}
    assert filter_func(entry) is False


def test_date_filter():
    filter_func = create_date_filter("2023-01-01")
    entry = {"@timestamp": "2023-01-01T12:00:00+00:00"}
    assert filter_func(entry) is True

    entry = {"@timestamp": "2023-01-02T12:00:00+00:00"}
    assert filter_func(entry) is False
