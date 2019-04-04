class APIConnectionError(Exception):

    def __init__(self, original_exception):
        msg = "Unable to connect"
        super().__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
