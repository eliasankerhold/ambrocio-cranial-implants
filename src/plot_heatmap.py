import plotly as pl
import os
import pandas as pd

path = os.path.join('..', 'exports', 'hits.csv')


print(path)


df = pd.read_csv(path)

mesh = pl.graph_objs.Mesh3d(x=df.x,
                            y=df.y,
                            z=df.z,
                            i=df.i,
                            j=df.j,
                            k=df.k,
                            intensity=df.hits,
                            intensitymode="cell")

fig = pl.graph_objs.Figure(data=[mesh])
fig.write_html("heatmap_database_28.html")
fig.show()
