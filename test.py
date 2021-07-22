import os
import plotly.graph_objects as plygo
from plotly.subplots import make_subplots


# make go.figure
# update figure layout (width, height, title, legend, barmode)
# TEST: add data to figure without subplot

# add subplots to go.figure
# define (rows, columns, shared_xaxes, shared_yaxes, titles)

# add traces (go.Scatter, go.Bar, go.pie, )
# go.Scatter (x, y, fill, mode, name, line_shape, dx, dy, title)
# go.Bar (x, y, name, layout.barmode, texttemplate, textposition, textfont_color, title)
# go.Pie (values, title, textposition, pull, )

fig1 = plygo.Figure(
    data=(
        {'type':'scatter','x':[1,2,3,4],'y':[1,2,3,4],'fill':'tonexty'},
        {'type':'scatter','x':[1,2,3,4],'y':[2,3,4,5],'fill':'tonexty'}),
    layout={
        'width': 1366,
        'height': 768,
        'title': 'Fig1'
    })

fig2 = make_subplots(rows=2, cols=2, subplot_titles=['trace1','trace2'], specs=[[{}, None], [{'colspan':2}, None]])
fig2.add_trace(plygo.Scatter(x= [1,2,3,4], y=[1,2,3,4], fill='tonexty'), row=1, col=1)
fig2.add_trace(plygo.Scatter(x= [1,2,3,4], y=[2,3,4,5], fill='tonexty'), row=2, col=1)
fig2.update_layout(
    width= 1366,
    height= 768,
    title= 'Fig2')

fig1.write_image(os.getcwd() + '/plot1.jpeg', scale=3, engine='kaleido')
fig2.write_image(os.getcwd() + '/plot2.jpeg', scale=3, engine='kaleido')