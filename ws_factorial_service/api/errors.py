class UnknownMethod(Exception):
    """Raised when unknown `method` field is specified in the API call."""

    def __init__(self, method_name, *args):
        self.method_name = method_name
        super().__init__(*args)
