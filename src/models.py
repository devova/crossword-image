import pandas as pd
import numpy as np
from pandas.core.series import Series
# from pandas.util.testing import Series

FILLED = 'x'
EMPTY = '.'
UNDEFINED = ' '
STRING_REPRESENTATION = (UNDEFINED, EMPTY, FILLED)


class Line(Series):
    def __str__(self):
        return 'Hello'


class Crossword(pd.DataFrame):

    _constructor_sliced = Line

    def __init__(self, f=None, data=None, index=None, columns=None, dtype=None,copy=False):
        _data = data
        if f:
            axes = pd.io.json.read_json(f, orient='records')
            p_index = pd.DataFrame(axes.y.values[0])
            p_columns = pd.DataFrame(axes.x.values[0])
            shape = (p_index.shape[0], p_columns.shape[0])
            _data = np.empty(shape, dtype=int)
            _data.fill(0)
        super().__init__(data=_data, index=index, columns=columns, dtype=dtype, copy=copy)
        if f:
            self.p_index = p_index
            self.p_columns = p_columns

    # def __str__(self):
    #     output = ''
    #     output +=
    #     return output