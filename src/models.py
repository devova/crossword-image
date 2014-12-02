import pandas as pd
import numpy as np
from base import BaseCrossword, BaseLine, LineDescription, UNKNOWN, EMPTY, FILLED


class Line(BaseLine):
    zones = []

    def _find_unknown_zones(self):
        self.zones = []
        s, e = None, None
        in_zone = False
        for i, v in enumerate(self.values):
            if v == UNKNOWN:
                e = i
                if not in_zone:
                    s = i
                    in_zone = True
            else:
                if in_zone:
                    in_zone = False
                    self.zones.append((s, e))
        if in_zone:
            self.zones.append((s, e))
        self.zones = pd.DataFrame(self.zones, columns=['start', 'end'])
        self.zones['len'] = self.zones['end'] - self.zones['start'] + 1


class Crossword(BaseCrossword):
    _constructor_sliced = Line

    def __init__(self, f=None, data=None, index=None, columns=None, dtype=None,copy=False):
        _data = data
        if f:
            axes = pd.io.json.read_json(f, orient='records')
            p_index = pd.Series(list(map(LineDescription, enumerate(axes.y.values[0]))), dtype=tuple)
            p_columns = pd.Series(list(map(LineDescription, enumerate(axes.x.values[0]))), dtype=tuple)
            shape = (p_index.shape[0], p_columns.shape[0])
            _data = np.empty(shape, dtype=int)
            _data.fill(UNKNOWN)
        super().__init__(data=_data, index=p_index, columns=p_columns, dtype=dtype, copy=copy)