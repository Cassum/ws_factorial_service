from math import factorial

from .base import BaseAPIMethod


class FactorialAPIMethod(BaseAPIMethod):
    """API method for calculating factorial of given number."""

    async def call(self, payload):
        value = payload['value']
        return factorial(value)
