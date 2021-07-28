import pandas as pd
import plotly.graph_objects as plygo
from plotly.subplots import make_subplots

def plotter (srcFig = dict, srcPlt = list):

    figure = make_subplots(rows= srcFig['rows'], cols= srcFig['cols'], width= srcFig['width'], height= srcFig['height'], title= srcFig['name'])

    for i in range(0, len(srcPlt)):
        if srcPlt[i]['tracetype'] == 'Scatter':

            plot = srcPlt[i]

            # get x data plot['datasrc'] plot['datatype']
            # get y data

            figure.add_trace(plygo.Scatter(
                x= [1, 2 ,3 , 4],
                y= [2, 6 , None, 5],
                connectgaps= True,
                fill= 'tonexty',
                mode= 'lines+markers',
                line= {'shape':'linear'},
                name= plot['name']
                ), row= plot['row'], col= plot['col'])
            
            figure.update_xaxes({'tickmode':'auto', 'tick0':0, 'dtick':1, 'tickangle':0, 'ticks':'outside', 'showline': True, 'linecolor':'black', 'linewidth':1, 'showgrid':False}, row= plot['row'], col= plot['col'])
            figure.update_yaxes({'tickmode':'auto', 'tick0':0, 'dtick':1, 'tickangle':0, 'ticks':'outside', 'showline': True, 'linecolor':'black', 'linewidth':1, 'showgrid':False}, row= plot['row'], col= plot['col'])
            
            pass

        elif srcPlt[i]['tracetype'] == 'Bar':
            pass

        elif srcPlt[i]['tracetype'] == 'Pie':
            pass

# make subplot (rows, cols, print_grid, subplot_titles, specs, insets, column_titles, row_titles, x_title, y_title)

# update layout (title, height, width, legend, plot_bgcolor)

# add_trace
# scatter (x, y, mode{markers, lines+markers, lines}, connectgaps, line_shape{spline, linear}, fill{tonexty, none}, name)
# scatter layout (title, xaxis{tickmode, tick0, dtick}, yaxis{tickmode, tick0, dtick}, xaxis_tickformat, yaxis_tickformat )
#
# Bar (x, y, barmode{gourp, stack, relative}, opacity, textposition{auto, outside}, bargap, bargroupgap)
# Bar layout ()
#
# Pie (labels, values, hole, pull, )
# Pie layout ()