from models import Crossword
import pandas as pd

grid = Crossword('data/1.json')
irow = grid[2]
irow[:5] = 1
irow[15:] = 1
irow._find_unknown_zones()
print(irow.name.idx)
print(irow.name.data)
print(irow.zsones)
print(grid)
