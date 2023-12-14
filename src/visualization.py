import plotly as plt
import os
import pandas as pd

results_path = os.path.join('..', 'exports', 'hits.csv')
result = pd.read_csv(results_path)

mesh = plt.graph_objs.Mesh3d(x=result.x, y=result.y, z=result.z,
                             i=result.i, j=result.j, k=result.k,
                             intensitymode='cell', intensity=result.hits)

fig = plt.graph_objs.Figure(data=[mesh])
fig.show()
