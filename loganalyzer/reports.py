from enum import Enum


class ReportType(Enum):
    """Report Type Enum-class."""

    AVERAGE_TIME = 0  # handler, total, average response time
    TOTAL = 1  # handler, total


class ReportManager:
    """A Report Manager class."""

    def __init__(
        self, report_type: ReportType, data: list[dict[str, any]], **filters
    ) -> None:
        """
        Initialize a report manager.

        Args:
            report_type (ReportType): report method.
            data (list[dict[str, any]]): data dictionary
            filters (dict): simple filters for data.

        """
        self.report_type = report_type
        self.filters: dict[str, any] = filters
        self._data = data

    @property
    def data(self):
        """Property for get data."""
        return self._data

    def set_data(self, new_data: dict):
        """Set new data dict."""
        self._data = new_data

    def _filter_data(self) -> dict[str, any]:
        """
        Filter data.

        Returns:
            dict[str, any]: filtered data

        """
        if not self.filters:
            return self._data

        filtered_data = []

        for item in self._data:
            for filter_name, filter_value in self.filters.items():
                if item.get(filter_name) == filter_value:
                    filtered_data.append(item)

        return filtered_data
