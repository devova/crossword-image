from models import Crossword
import pandas as pd

grid = Crossword('data/1.json')
print(grid.p_index)
print(grid.p_columns)
print(grid)