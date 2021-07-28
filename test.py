import os
import plotly.graph_objects as plygo
from plotly.subplots import make_subplots
import plotly.io as pio

fig = make_subplots(
    rows=2,
    cols=1,
    #subplot_titles=['trace1','trace2'],
    #specs=[[{}, None], [{'colspan':2}, None]]
    )

#fig.add_trace(plygo.Scatter(
#    x= '',
#    y= '',
#    connectgaps= ,
#    fill= 'tonexty | none',
#    line= '{linear | spline}',
#    marker= '{dtick, tick0, tickangle, tickmode, ticks(outside, inside)}',
#    mode= 'lines | markers | lines+markers',
#    name= 'tracename',
#    showlegend= ,
#    ))

#fig.add_trace(plygo.Scatter(x= [1,2,3,4], y=[2,3,4,5], fill='tonexty'), row=2, col=1)

fig.add_trace(plygo.Scatter(
    x= [1, 2 ,3 , 4],
    y= [2, 6 , None, 5],
    connectgaps= True,
    fill= 'tonexty',
    mode= 'lines+markers',
    line= {'shape':'linear'},
    name= 'one',
    ), row=1, col=1)

fig.add_trace(plygo.Scatter(
    x= [1, 2 ,3 , 4],
    y= [2, 6 , None, 5],
    connectgaps= False,
    fill= 'none',
    mode= 'lines+markers',
    line= {'shape':'linear'},
    name= 'two',
    ), row=2, col=1)

fig.update_xaxes({'tickmode':'auto', 'tick0':0, 'dtick':1, 'tickangle':0, 'ticks':'outside', 'showline': True, 'linecolor':'black', 'linewidth':1, 'showgrid':False}, row= 1, col= 1)
fig.update_yaxes({'tickmode':'auto', 'tick0':0, 'dtick':1, 'tickangle':0, 'ticks':'outside', 'showline': True, 'linecolor':'black', 'linewidth':1, 'showgrid':False}, row= 1, col= 1)

fig.update_layout(
    width= 1366,
    height= 768,
    template= pio.templates['simple_white'],
    title= 'Figure Test',
    #plot_bgcolor= '#ffffff',
    #paper_bgcolor= '#eeeeee',
    showlegend= True
    )

fig.write_image(os.getcwd() + '/plot1.jpeg', scale=3, engine='kaleido')