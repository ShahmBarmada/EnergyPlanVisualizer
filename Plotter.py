import re
import pandas as pd
import plotly.graph_objects as plygo
import plotly.io as pio
from plotly.subplots import make_subplots

def plotter (srcFig = dict, srcPlt = list):

    figure = make_subplots(rows= srcFig['rows'], cols= srcFig['cols'])

    for plt_i in range(len(srcPlt)):

        plotsTitles = []
        plot = srcPlt[plt_i]

        # get data
        srcStd = plot['datasrc']
        stdDF = pd.read_csv(srcStd['path'], delimiter=',', low_memory=False, index_col='Index')

        # set x data (datatype[monthly, hourly], xstart, xend, xtype[time, data], xdata{haeder key})
        if plot['datatype'] == 'monthly':
            xStart = plot['xstart']
            xEnd = plot['xend']
            xData = stdDF.loc[xStart:xEnd].index.values.tolist()
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

                for xData_i, headers in enumerate(list(stdDF.columns.values)):

                    if plot['xdata'][:2] == '00':
                        if plot['xdata'] == headers[:4]:
                            xDataOffset = headers
                            xData = stdDF.loc[xStart:xEnd, xDataOffset].tolist()
                            break
                    else:
                        xData = stdDF.loc[xStart:xEnd].index.values.tolist()

        # set y data (ydata{haeder key})
        yData = []
        for yData_i, headers in enumerate(list(stdDF.columns.values)):

            if str(plot['ydata'])[:2] == '00':
                if plot['ydata'] == headers[:4]:
                    yData.append(headers)
                    break
            elif str(plot['ydata'])[:2] == headers[:2]:
                yData.append(headers)
                next

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

        if srcPlt[plt_i]['tracetype'] == 'Scatter':

            # set fill
            if plot['tracefill']:
                styleFill = 'tonexty'
            else:
                styleFill = 'none'

            # set mode & shape
            if plot['tracestyle'] == 'Smooth Linear':
                styleMode = 'lines'
                styleLine = {'shape': 'spline'}
            else:
                styleMode = str(plot['tracestyle']).replace('Only','').replace(' ', '').strip().lower()
                styleLine = {'shape': 'linear'}

            # build plot
            for i in range(len(yData)):

                figure.add_trace(plygo.Scatter(
                    x= xData,
                    y= stdDF.loc[xStart:xEnd, yData[i]].tolist(),
                    connectgaps= False,
                    fill= styleFill,
                    mode= styleMode,
                    line= styleLine,
                    name= str(yData[i])[5:]
                    ), row= plot['row'], col= plot['col'])

            # update layout & axes
            figure.update_xaxes({'title_text':'Test X', 'tickmode': xTickMode, 'tick0': 0, 'dtick': xTickStep, 'tickangle': -45}, row= plot['row'], col= plot['col'])
            figure.update_yaxes({'title_text':'Test Y', 'tickmode': yTickMode, 'tick0': 0, 'dtick': yTickStep, 'tickangle': 0}, row= plot['row'], col= plot['col'])

        elif srcPlt[plt_i]['tracetype'] == 'Bar':

            # set mode & shape
            styleMode = str(plot['tracestyle'])[:-2].replace(' ', '').strip().lower()

            # build plot
            for i in range(len(yData)):

                figure.add_trace(plygo.Bar(
                    x= xData,
                    y= stdDF.loc[xStart:xEnd, yData[i]].tolist(),
                    text= stdDF.loc[xStart:xEnd, yData[i]],
                    textfont_color= '#000000',
                    textposition= 'inside',
                    name= str(yData[i])[5:]
                    ), row= plot['row'], col= plot['col'])

            # update layout & axes
            figure.update_xaxes({'title_text':'Test X'}, row= plot['row'], col= plot['col'])
            figure.update_yaxes({'title_text':'Test Y', 'tickmode': yTickMode, 'tick0': 0, 'dtick': yTickStep, 'tickangle': 0}, row= plot['row'], col= plot['col'])
            figure.update_layout({'barmode': styleMode})

        elif srcPlt[plt_i]['tracetype'] == 'Pie':
            pass

    figure.update_layout(width= srcFig['width'], height= srcFig['height'], title= srcFig['name'], showlegend= True, template= pio.templates['simple_white'])

    #for j in range(1, len(srcPlt) +1):
        #figure.update_layout({'yaxis' + str(j):{'title': 'axis' + str(j)}})


    return figure

# Bar (x, y, barmode{gourp, stack, relative}, opacity, textposition{auto, outside}, bargap, bargroupgap)
# Bar layout ()
#
# Pie (labels, values, hole, pull, )
# Pie layout ()