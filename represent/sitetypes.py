class SiteType:

    def __init__(self, str, dims, coherent_parameters):
        self._str = str
        self.dims = dims
        self.coherent_parameters = coherent_parameters

    # TODO stricter equality condition may be more useful later
    def __eq__(self, other):
        return (self._str == other._str)
