from .errors import UnknownMethod
from .methods.factorial import FactorialAPIMethod


class Dispatcher:
    """Class responsible for dispatching API call to proper method class."""

    def __init__(self):
        self.method_mapping = {
            'factorial': FactorialAPIMethod,
        }

    async def dispatch(self, method_name, payload):
        method_cls = self.method_mapping.get(method_name)
        if not method_cls:
            raise UnknownMethod(method_name)
        return await method_cls().call(payload)
