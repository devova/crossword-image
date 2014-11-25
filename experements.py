import pandas as pd

grid = pd.io.json.read_json('data/1.json', orient='records')
print(grid)