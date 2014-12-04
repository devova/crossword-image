RULES = []


class Rule(object):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args)
        RULES.append(obj)
        return obj

    def __init__(self, df=None):
        self.df = df

    def apply(self):
        raise NotImplementedError
