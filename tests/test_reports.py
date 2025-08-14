from loganalyzer.reports import ReportManager, ReportType

EXAMPLE_DATA = [
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": 0.024, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": 0.02, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": 0.024, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.032, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.064, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.1, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.076, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.076, "http_user_agent": "..."}
]

def test_report_manager_init():
    report_man = ReportManager(ReportType.AVERAGE_TIME, EXAMPLE_DATA, status=200)

    assert report_man.data == EXAMPLE_DATA
    report_man.set_data([])
    assert report_man.data == []
    report_man.set_data(EXAMPLE_DATA)
    assert report_man.data == EXAMPLE_DATA
