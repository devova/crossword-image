import pandas as pd
import numpy as np
from pandas.core.series import Series
from pandas.core.index import Index
from pandas.compat import StringIO

FILLED = 2
EMPTY = 1
UNKNOWN = 0
FILLED_STR = 'x'
EMPTY_STR = '.'
UNKNOWN_STR = ' '
STRING_REPRESENTATION = {UNKNOWN: UNKNOWN_STR, EMPTY: EMPTY_STR, FILLED: FILLED_STR}


class LineDescription(str):
    def __new__(cls, value):
        idx, data = value
        obj = super(LineDescription, cls).__new__(cls, idx)
        obj.data = data
        obj.idx = idx
        return obj

    def to_string(self):
        s = ' '.join(map(str, self.data))
        return ' %15s' % s


class BaseLine(Series):
    def _get_repr(self, name=False, print_header=False, length=True, dtype=True, na_rep='NaN', float_format=None):
        out = ''.join([self.name.to_string(), '|'] + [STRING_REPRESENTATION[i] for _, i in self.iteritems()])
        return out


class BaseCrossword(pd.DataFrame):
    _constructor_sliced = BaseLine
    p_index = None
    p_columns = None

    def _getitem_column(self, key):
        """ return the actual column """

        # get column
        key = str(key)
        if self.columns.is_unique:
            return self._get_item_cache(key)

        # duplicate columns & possible reduce dimensionaility
        result = self._constructor(self._data.get(key))
        if result.columns.is_unique:
            result = result[key]

        return result

    def _ixs(self, i, axis=0):
        #irow
        if axis == 0:

            """
            Notes
            -----
            If slice passed, the resulting data will be a view
            """

            if isinstance(i, slice):
                return self[i]
            else:
                label = self.index[i]
                if isinstance(label, Index):
                    # a location index by definition
                    result = self.take(i, axis=axis)
                    copy = True
                else:
                    new_values = self._data.fast_xs(i)

                    # if we are a copy, mark as such
                    copy = isinstance(new_values, np.ndarray) and new_values.base is None
                    result = self._constructor_sliced(new_values, index=self.columns,
                                    name=self.index[i], dtype=new_values.dtype)
                result._set_is_copy(self, copy=copy)
                return result

        # icol
        else:

            """
            Notes
            -----
            If slice passed, the resulting data will be a view
            """

            label = self.columns[i]
            if isinstance(i, slice):
                # need to return view
                lab_slice = slice(label[0], label[-1])
                return self.ix[:, lab_slice]
            else:
                label = self.columns[i]
                if isinstance(label, Index):
                    return self.take(i, axis=1, convert=True)

                # if the values returned are not the same length
                # as the index (iow a not found value), iget returns
                # a 0-len ndarray. This is effectively catching
                # a numpy error (as numpy should really raise)
                values = self._data.iget(i)
                if not len(values):
                    values = np.array([np.nan] * len(self.index), dtype=object)
                result = self._constructor_sliced.from_array(
                    values, index=self.index,
                    name=label, fastpath=True)

                # this is a cached value, mark it so
                result._set_as_cached(label, self)
                return result

    def iterrows(self):
        """
        Iterate over rows of DataFrame as (index, Series) pairs.

        Notes
        -----

        * ``iterrows`` does **not** preserve dtypes across the rows (dtypes
          are preserved across columns for DataFrames). For example,

            >>> df = DataFrame([[1, 1.0]], columns=['x', 'y'])
            >>> row = next(df.iterrows())[1]
            >>> print(row['x'].dtype)
            float64
            >>> print(df['x'].dtype)
            int64

        Returns
        -------
        it : generator
            A generator that iterates over the rows of the frame.
        """
        columns = self.columns
        for k, v in zip(self.index, self.values):
            s = self._constructor_sliced(v, index=columns, name=k)
            yield k, s

    def to_string(self, buf=None, columns=None, col_space=None, colSpace=None,
                  header=True, index=True, na_rep='NaN', formatters=None,
                  float_format=None, sparsify=None, index_names=True,
                  justify=None, line_width=None, max_rows=None, max_cols=None,
                  show_dimensions=False):
        _buf = buf if buf is not None else StringIO()
        _buf.write('                 ______________________________________________________________________\n')
        for _, row in self.iterrows():
            _buf.write('%s\n' % row.to_string())
        if buf is None:
            return _buf.getvalue()