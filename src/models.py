import pandas as pd
import numpy as np
from base import BaseCrossword


class Crossword(BaseCrossword):

    def __init__(self, f=None, data=None, index=None, columns=None, dtype=None,copy=False):
        _data = data
        if f:
            axes = pd.io.json.read_json(f, orient='records')
            p_index = pd.Series(axes.y.values[0], dtype=tuple)
            p_columns = pd.Series(axes.x.values[0], dtype=tuple)
            shape = (p_index.shape[0], p_columns.shape[0])
            _data = np.empty(shape, dtype=int)
            _data.fill(1)
        super().__init__(data=_data, index=index, columns=columns, dtype=dtype, copy=copy)
        if f:
            self.p_index = p_index
            self.p_columns = p_columns