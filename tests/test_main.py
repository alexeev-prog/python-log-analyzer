from unittest.mock import patch

import pytest

from loganalyzer import main


@pytest.fixture
def mock_data():
    return [
        {
            "@timestamp": "2023-01-01T00:00:00+00:00",
            "url": "/test",
            "response_time": 0.1,
            "http_user_agent": "TestAgent",
        },
        {
            "@timestamp": "2023-01-02T00:00:00+00:00",
            "url": "/test",
            "response_time": 0.2,
            "http_user_agent": "TestAgent",
        },
    ]


@patch("argparse.ArgumentParser.parse_args")
@patch("loganalyzer.load_log_data")
def test_main_average_report(mock_load, mock_parse, mock_data, capsys):
    mock_parse.return_value = type(
        "",
        (),
        {
            "file": ["test.log"],
            "report": "average",
            "date": None,
            "user_agent": None,
            "fileformat": "log",
        },
    )()

    mock_load.return_value = mock_data
    main()

    captured = capsys.readouterr()
    assert "handler" in captured.out
    assert "total" in captured.out
    assert "avg_response_time" in captured.out


@patch("argparse.ArgumentParser.parse_args")
@patch("loganalyzer.load_json_data")
def test_main_user_agent_report(mock_load, mock_parse, mock_data, capsys):
    mock_parse.return_value = type(
        "",
        (),
        {
            "file": ["test.json"],
            "report": "user_agent",
            "date": None,
            "user_agent": None,
            "fileformat": "json",
        },
    )()

    mock_load.return_value = mock_data
    main()

    captured = capsys.readouterr()
    assert "user_agent" in captured.out
    assert "total" in captured.out


@patch("argparse.ArgumentParser.parse_args")
def test_main_invalid_report(mock_parse, capsys):
    mock_parse.return_value = type(
        "",
        (),
        {
            "file": ["test.log"],
            "report": "invalid",
            "date": None,
            "user_agent": None,
            "fileformat": "log",
        },
    )()

    main()
    captured = capsys.readouterr()
    assert "Fatal error" in captured.out


@patch("argparse.ArgumentParser.parse_args")
@patch("loganalyzer.load_log_data", side_effect=FileNotFoundError("File not found"))
def test_main_file_not_found(mock_load, mock_parse, capsys):
    mock_parse.return_value = type(
        "",
        (),
        {
            "file": ["missing.log"],
            "report": "average",
            "date": None,
            "user_agent": None,
            "fileformat": "log",
        },
    )()

    main()
    captured = capsys.readouterr()
    assert "Fatal error" in captured.out


@patch("argparse.ArgumentParser.parse_args")
def test_main_invalid_date(mock_parse, capsys):
    mock_parse.return_value = type(
        "",
        (),
        {
            "file": ["test.log"],
            "report": "average",
            "date": "2023-13-01",
            "user_agent": None,
            "fileformat": "log",
        },
    )()

    main()
    captured = capsys.readouterr()
    assert (
        "Fatal error when opening test.log: [Errno 2] No such file or directory: 'test.log'\n"
        in captured.out
    )
