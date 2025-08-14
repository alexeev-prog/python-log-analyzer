from datetime import date, datetime


def validate_date(date_string):
    """Validate date string."""
    try:
        date.fromisoformat(date_string)
    except ValueError:
        raise ValueError("Incorrect data format, should be %Y-%m-%d")  # noqa: B904


def create_user_agent_filter(target_user_agent: str) -> callable:
    """Create date filter for reports manager."""

    def filter_func(entry):
        user_agent = entry["http_user_agent"]
        return user_agent == target_user_agent

    return filter_func


def create_date_filter(target_date_str: str) -> callable:
    """Create date filter for reports manager."""

    def filter_func(entry):
        entry_date = datetime.strptime(
            entry["@timestamp"], "%Y-%m-%dT%H:%M:%S%z"
        ).date()
        target_date = datetime.strptime(  # noqa: DTZ007
            target_date_str,
            "%Y-%m-%d",
        ).date()
        return entry_date == target_date

    return filter_func
