from models import Crossword
import pandas as pd

grid = Crossword('data/1.json')
irow = grid.irow(34)
g = grid.reset_index()
irow[:5] = 0
irow[15:] = 0
irow._find_unknown_zones()
print(irow.name)
print(irow.zones)
