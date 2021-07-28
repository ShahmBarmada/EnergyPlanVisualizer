import pandas as pd
import plotly.graph_objects as plygo
from plotly.subplots import make_subplots

def plotter (srcFig = dict, srcPlt = list):

    figure = make_subplots(rows= srcFig['rows'], cols= srcFig['cols'])

    for i in range(0, len(srcPlt)):
        if srcPlt[i]['tracetype'] == 'Scatter':

            plot = srcPlt[i]

            # get data
            srcStd = plot['datasrc']
            stdDF = pd.read_csv(srcStd['path'], delimiter=',', low_memory=False, index_col='Index')

            # set x data (datatype[monthly, hourly], xstart, xend, xtype[time, data], xdata{haeder key})


            # set y data (ydata{haeder key})
            yData = []
            for i, headers in enumerate(list(stdDF.columns.values)):
                if str(plot['ydata'])[:2] == '00' and plot['ydata'] == headers[:4]:
                    yData.append(headers)
                    break
                elif str(plot['ydata'])[:2] == headers[:2]:
                    yData.append(headers)
                    next

            # set name

            # set fill
            if plot['tracefill']:
                styleFill = 'tonexty'
            else:
                styleFill = 'none'

            # set mode & shape
            if plot['tracestyle'] == 'Smooth Linear':
                styleLine = {'shape': 'spline'}
            else:
                styleMode = str(plot['tracestyle']).replace('Only','').replace(' ', '').strip().lower()
                styleLine = {'shape': 'linear'}

            # set ticks (xtick, xstep, ytick, ystep)
            for i in range(0, len(yData)):

                figure.add_trace(plygo.Scatter(
                    x= ['January','February','March','April','May','June','July','August','September','October','November','December'],
                    y= stdDF.loc[['January','February','March','April','May','June','July','August','September','October','November','December'],yData[i]].tolist(),
                    connectgaps= False,
                    fill= styleFill,
                    mode= styleMode,
                    line= styleLine,
                    ), row= plot['row'], col= plot['col'])

            #figure.update_xaxes({'tickmode':'auto', 'tick0':0, 'dtick':1, 'tickangle':0, 'ticks':'outside', 'showline': True, 'linecolor':'black', 'linewidth':1, 'showgrid':False}, row= plot['row'],     col= plot['col'])
            #figure.update_yaxes({'tickmode':'auto', 'tick0':0, 'dtick':1, 'tickangle':0, 'ticks':'outside', 'showline': True, 'linecolor':'black', 'linewidth':1, 'showgrid':False}, row= plot['row'],     col= plot['col'])

            # update layout (colspan, rowspan)


        elif srcPlt[i]['tracetype'] == 'Bar':
            pass

        elif srcPlt[i]['tracetype'] == 'Pie':
            pass

    figure.update_layout(width= srcFig['width'], height= srcFig['height'], title= srcFig['name'])

    return figure

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