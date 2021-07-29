import re
import pandas as pd
import plotly.graph_objects as plygo
import plotly.io as pio
from plotly.subplots import make_subplots

def plotter (srcFig = dict, srcPlt = list):
    figTitles = []

    figure = make_subplots(rows= srcFig['rows'], cols= srcFig['cols'], subplot_titles= figTitles)

    for i in range(0, len(srcPlt)):
        if srcPlt[i]['tracetype'] == 'Scatter':

            plot = srcPlt[i]

            # get data
            srcStd = plot['datasrc']
            stdDF = pd.read_csv(srcStd['path'], delimiter=',', low_memory=False, index_col='Index')

            # set x data (datatype[monthly, hourly], xstart, xend, xtype[time, data], xdata{haeder key})
            if plot['datatype'] == 'monthly':
                xStart = plot['xstart']
                xEnd = plot['xend']
            
            elif plot['datatype'] == 'hourly':
                # set xStart
                if re.fullmatch(r'\d{1,4}', plot['xstart']):
                    xStart = 'h' + plot['xstart']

                elif re.fullmatch(r'h\d{1,4}', plot['xstart']):
                    xStart = plot['xstart']

                elif re.fullmatch(r'd\d{1,3}', plot['xstart']):
                    xStart = int(plot['xstart'][1:])
                    xStart = (xStart * 24) - 24 + 1
                    xStart = 'h' + str(xStart)

                elif re.fullmatch(r'w\d{1,2}', plot['xstart']):
                    xStart = int(plot['xstart'][1:])
                    xStart = ((xStart -1) * 24 * 7) + 1
                    xStart = 'h' + str(xStart)

                else:
                    xStart = 'h1'

                # set xEnd
                if re.fullmatch(r'\d{1,4}', plot['xend']):
                    xEnd = 'h' + plot['xend']

                elif re.fullmatch(r'h\d{1,4}', plot['xend']):
                    xEnd = plot['xend']

                elif re.fullmatch(r'd\d{1,3}', plot['xend']):
                    xEnd = int(plot['xend'][1:])
                    xEnd = xEnd * 24
                    xEnd = 'h' + str(xEnd)

                elif re.fullmatch(r'w\d{1,2}', plot['xend']):
                    xEnd = int(plot['xend'][1:])
                    xEnd = xEnd * 24 * 7
                    xEnd = 'h' + str(xEnd)

                else:
                    xEnd = 'h8784'

                if plot['xtype'] == 'time':
                    xData = stdDF.loc[xStart:xEnd].index.values.tolist()
                
                elif plot['xtype'] == 'data':
                    xDataOffset = ''

                    for i, headers in enumerate(list(stdDF.columns.values)):

                        if plot['xdata'][:2] == '00':

                            if plot['xdata'] == headers[:4]:

                                xDataOffset = headers
                                xData = stdDF.loc[xStart:xEnd, xDataOffset].tolist()
                                break

                        else:
                            xData = stdDF.loc[xStart:xEnd].index.values.tolist()

            # set y data (ydata{haeder key})
            yData = []
            for i, headers in enumerate(list(stdDF.columns.values)):

                if str(plot['ydata'])[:2] == '00':

                    if plot['ydata'] == headers[:4]:
                        yData.append(headers)
                        break

                elif str(plot['ydata'])[:2] == headers[:2]:
                    yData.append(headers)
                    next

            # set name
            pltName = plot['title']
            figTitles.append(pltName)

            # set fill
            if plot['tracefill']:
                styleFill = 'tonexty'
            else:
                styleFill = 'none'

            # set mode & shape
            styleMode = str(plot['tracestyle']).replace('Only','').replace(' ', '').strip().lower()

            if plot['tracestyle'] == 'Smooth Linear':
                styleLine = {'shape': 'spline'}
            else:
                styleLine = {'shape': 'linear'}

            # set ticks (xtick, xstep, ytick, ystep)

            if plot['xtick'] == 'auto':
                xTickMode = 'auto'
            else:
                xTickMode = 'linear'

            xTickStep = plot['xstep']

            if plot['ytick'] == 'auto':
                yTickMode = 'auto'
            else:
                yTickMode = 'linear'

            yTickStep = plot['ystep']


            for i in range(0, len(yData)):

                figure.add_trace(plygo.Scatter(
                    x= xData,
                    y= stdDF.loc[xStart:xEnd, yData[i]].tolist(),
                    connectgaps= False,
                    fill= styleFill,
                    mode= styleMode,
                    line= styleLine,
                    name= str(yData[i])[5:]
                    ), row= plot['row'], col= plot['col'])

            #figure.update_xaxes({'tickmode':'auto', 'tick0':0, 'dtick':1, 'tickangle':0, 'ticks':'outside', 'showline': True, 'linecolor':'black', 'linewidth':1, 'showgrid':False}, row= plot['row'], col= plot['col'])
            figure.update_xaxes({'tickmode': xTickMode, 'tick0': 0, 'dtick': xTickStep, 'tickangle': -45}, row= plot['row'], col= plot['col'])
            figure.update_yaxes({'tickmode': yTickMode, 'tick0': 0, 'dtick': yTickStep, 'tickangle': -45}, row= plot['row'], col= plot['col'])

            # update layout (colspan, rowspan)


        elif srcPlt[i]['tracetype'] == 'Bar':
            pass

        elif srcPlt[i]['tracetype'] == 'Pie':
            pass

    figure.update_layout(width= srcFig['width'], height= srcFig['height'], title= srcFig['name'], showlegend= True, template= pio.templates['simple_white'])
    
    print(figTitles)

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