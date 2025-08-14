import json

import pytest

from loganalyzer.reader import load_json_data, load_log_data


@pytest.fixture
def log_file(tmp_path):
    file = tmp_path / "test.log"
    content = [
        '{"key": "value1"}',
        '{"key": "value2"}',
        "invalid json",
        '{"key": "value3"}',
    ]
    file.write_text("\n".join(content))
    return file


@pytest.fixture
def json_file(tmp_path):
    file = tmp_path / "test.json"
    content = [{"key": "value1"}, {"key": "value2"}, {"key": "value3"}]
    file.write_text(json.dumps(content))
    return file


def test_load_log_data(log_file, capsys):
    result = load_log_data(str(log_file))
    assert len(result) == 3
    assert result[0]["key"] == "value1"
    assert result[1]["key"] == "value2"
    assert result[2]["key"] == "value3"

    captured = capsys.readouterr()
    assert "invalid json" in captured.out


def test_load_json_data(json_file):
    result = load_json_data(str(json_file))
    assert len(result) == 3
    assert result[0]["key"] == "value1"
    assert result[1]["key"] == "value2"
    assert result[2]["key"] == "value3"
