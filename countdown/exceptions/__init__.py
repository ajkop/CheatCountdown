class ApplicationError(Exception):
    """ Base level error in the application """


class APIError(ApplicationError):
    """ Generic error with the API calls."""


class APIAuthenticationError(APIError):
    """ Bad authentication while communicating with API"""
