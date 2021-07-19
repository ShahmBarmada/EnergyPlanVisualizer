import os
import plotly.graph_objects as plygo

plotData = dict({"data": [{"type": "scatter", "x": [1,2,3], "y": [2,1,2]}]})
fig1 = plygo.Figure(data = plotData)
fig1 = plygo.Bar(fig1)

fig1.update_layout(width=1366, height=768)
fig1.write_image(os.getcwd() + '/plot_.jpeg', scale=3, engine='kaleido')
