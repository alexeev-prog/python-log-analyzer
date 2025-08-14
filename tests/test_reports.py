import pytest

from loganalyzer.reports import (
    AverageTimeReport,
    ReportManager,
    ReportStrategy,
    UserAgentReport,
)


@pytest.fixture
def sample_data():
    return [
        {"url": "/api/test1", "response_time": 0.1, "http_user_agent": "Agent1"},
        {"url": "/api/test1", "response_time": 0.2, "http_user_agent": "Agent1"},
        {"url": "/api/test2", "response_time": 0.3, "http_user_agent": "Agent2"},
        {"url": "/api/test2", "response_time": 0.4, "http_user_agent": "Agent2"},
        {"url": "/api/test2", "response_time": 0.5, "http_user_agent": "Agent2"},
    ]


def test_report_strategy_abstract():
    with pytest.raises(TypeError):
        ReportStrategy().generate_report([])


def test_average_time_report(sample_data):
    report = AverageTimeReport()
    result = report.generate_report(sample_data)

    assert len(result) == 2
    assert result[0]["handler"] == "/api/test2"
    assert result[0]["total"] == 3
    assert result[0]["avg_response_time"] == 0.4

    assert result[1]["handler"] == "/api/test1"
    assert result[1]["total"] == 2
    assert result[1]["avg_response_time"] == 0.15


def test_user_agent_report(sample_data):
    report = UserAgentReport()
    result = report.generate_report(sample_data)

    assert len(result) == 2
    assert result[0]["user_agent"] == "Agent2"
    assert result[0]["total"] == 3
    assert result[1]["user_agent"] == "Agent1"
    assert result[1]["total"] == 2


def test_report_manager_no_filters(sample_data):
    strategy = AverageTimeReport
    manager = ReportManager(strategy, sample_data)
    result = manager.generate()
    assert len(result) == 2


def test_report_manager_with_filter(sample_data):
    def test_filter(item):
        return item["url"] == "/api/test1"

    strategy = AverageTimeReport
    manager = ReportManager(strategy, sample_data, filters=[test_filter])
    result = manager.generate()
    assert len(result) == 1
    assert result[0]["handler"] == "/api/test1"


def test_report_manager_property(sample_data):
    strategy = AverageTimeReport()
    manager = ReportManager(strategy, sample_data)
    assert manager.data == sample_data

    new_data = [{"url": "/new", "response_time": 1.0}]
    manager.set_data(new_data)
    assert manager.data == new_data
