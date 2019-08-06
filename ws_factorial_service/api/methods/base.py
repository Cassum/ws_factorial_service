from abc import ABC, abstractmethod


class BaseAPIMethod(ABC):
    """Base class for all API methods."""

    def __init__(self):
        pass

    @abstractmethod
    def call(self, payload):
        """Actual API method logic."""
        pass
