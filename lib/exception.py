class DataNotFoundError(Exception):
    pass


class ScrapingDataNotFoundError(Exception):
    pass


class FoursquareAPIError(Exception):
    pass


class FoursquareAPIRateLimitExceeded(Exception):
    pass
