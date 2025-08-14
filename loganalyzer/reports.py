from abc import ABC, abstractmethod
from collections.abc import Callable


class ReportStrategy(ABC):
    """Report strategy class."""

    @abstractmethod
    def generate_report(self, data: list[dict[str, any]]) -> list[dict[str, any]]:
        """
        Generate data with used strategy.

        Args:
            data (list[dict[str, any]]): data.

        Returns:
            list[dict[str, any]]

        """
        raise NotImplementedError


class AverageTimeReport(ReportStrategy):
    """Report strategy 'average time'."""

    def generate_report(self, data: list[dict[str, any]]) -> list[dict[str, any]]:
        """Generate data report by average time strategy."""
        url_stats = {}
        for item in data:
            url = item["url"]
            response_time = item["response_time"]

            if url not in url_stats:
                url_stats[url] = []

            url_stats[url].append(response_time)

        report_data = [
            {
                "handler": handler,
                "total": len(url_stats[handler]),
                "avg_response_time": round(
                    sum(url_stats[handler]) / len(url_stats[handler]), 3
                ),
            }
            for handler in url_stats
        ]
        return sorted(report_data, key=lambda x: x["total"], reverse=True)


class UserAgentReport(ReportStrategy):
    """Report strategy 'user agent'."""

    def generate_report(self, data: list[dict[str, any]]) -> list[dict[str, any]]:
        """Generate data report by user agent."""
        stats = {}
        for item in data:
            user_agent = item["http_user_agent"]

            stats[user_agent] = stats.get(user_agent, 0) + 1

        report_data = [
            {"user_agent": user_agent, "total": stats[user_agent]}
            for user_agent in stats
        ]

        return sorted(report_data, key=lambda x: x["total"], reverse=True)


class ReportManager:
    """A Report Manager class."""

    def __init__(
        self,
        report_strategy: ReportStrategy,
        data: list[dict[str, any]],
        filters: list[Callable[[dict], bool]] | None = None,
    ) -> None:
        """
        Initialize a report manager.

        Args:
            report_strategy (ReportStrategy): report strategy class.
            data (list[dict[str, any]]): data dictionary
            filters (list[Callable[[dict], bool]] | None): simple filters for data.

        """
        if filters is None:
            filters = []

        self.report_strategy = report_strategy
        self.filters = filters
        self._data = data

    @property
    def data(self):
        """Property for get data."""
        return self._data

    def set_data(self, new_data: dict):
        """Set new data dict."""
        self._data = new_data

    def _filter_data(self) -> list[dict[str, any]]:
        """
        Filter data.

        Returns:
            dict[str, any]: filtered data

        """
        if not self.filters:
            return self._data

        filtered_data = []

        for item in self._data:
            if self.filters:
                if all(filter_fn(item) for filter_fn in self.filters):
                    filtered_data.append(item)
            else:
                filtered_data.append(item)

        return filtered_data

    def generate(self):
        """Generate report."""
        return self.report_strategy().generate_report(self._filter_data())
