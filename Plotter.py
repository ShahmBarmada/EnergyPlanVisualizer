import pandas as pd
import plotly.graph_objects as plygo
from plotly.subplots import make_subplots

def plotter (srcFig = dict, srcPlt = list) -> list:
    fig = srcFig['id']
    plt = []
    for i in range(0, len(srcPlt)):
        plt.append(srcPlt[i]['id'])

    fig = make_subplots(rows= srcFig['rows'], cols= srcFig['cols'])

    for i in range(0, len(srcPlt)):
        if srcPlt[i]['tracetype'] == 'Scatter':
            pass

        elif srcPlt[i]['tracetype'] == 'Bar':
            pass

        elif srcPlt[i]['tracetype'] == 'Pie':
            pass

    return [fig, plt]

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