import re
import pandas as pd
import plotly.graph_objects as plygo
import plotly.io as pio
from plotly.subplots import make_subplots

def plotter (srcFig = dict, srcPlt = list):

    figSize = srcFig['rows'] * srcFig['cols']
    figTitles = []

    for size_i in range(0, figSize):
        figTitles.append('Plot ' + str(size_i))

    figure = make_subplots(rows= srcFig['rows'], cols= srcFig['cols'], horizontal_spacing= 0.1, vertical_spacing= 0.23, subplot_titles= tuple(figTitles))
    figTitles.clear()

    for plt_i in range(len(srcPlt)):
        
        plot = srcPlt[plt_i]

        # get data source
        srcStd = plot['datasrc']
        stdDF = pd.read_csv(srcStd['path'], delimiter=',', low_memory=False, index_col='Index')
        stdDF.loc['AnnualAverage':'AnnualMinimum'] /= 1000

        # calc plot grid position & assign title
        pltPos = plot['row'] * 10 + plot['col'] * 1
        pltTitle = str(pltPos) + '_' + srcStd['id'] + ' ' + srcStd['name']
        figTitles.append(pltTitle)

        # getting X series data

        if plot['datatype'] == 'hourly':
            
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
                xTitle = 'Time Range'
            elif plot['xtype'] == 'data':
                xDataOffset = ''
                xTitle = plot['xtitle'] + ' (MW)'

                for xData_i, headers in enumerate(list(stdDF.columns.values)):

                    if plot['xdata'][:2] == '00':
                        if plot['xdata'] == headers[:4]:
                            xDataOffset = headers
                            xData = stdDF.loc[xStart:xEnd, xDataOffset].tolist()
                            break
                    else:
                        xData = stdDF.loc[xStart:xEnd].index.values.tolist()

            yTitle = plot['ytitle'] + ' (MW)'

        elif plot['datatype'] == 'monthly':

            xStart = plot['xstart']
            xEnd = plot['xend']
            xData = stdDF.loc[xStart:xEnd].index.values.tolist()

            if plot['xtype'] == 'time':
                xTitle = 'Time Range'
            elif plot['xtype'] == 'data':
                xTitle = plot['xtitle'] + ' (MW)'

            yTitle = plot['ytitle'] + ' (MW)'

        elif plot['datatype'] == 'annual':

            if plot['xdata'] == 'Total':
                xStart = xEnd = 'Annual'
            elif plot['xdata'] == 'Average':
                xStart = xEnd = 'AnnualAverage'
            elif plot['xdata'] == 'Maximum':
                xStart = xEnd = 'AnnualMaximum'
            elif plot['xdata'] == 'Minimum':
                xStart = xEnd = 'AnnualMinimum'
            elif plot['xdata'] == 'Annual CO2 Emissions':
                xStart = 'Co2-Emission(Total)'
                xEnd = 'Co2-Emission(Corrected)'
                templateFormat = '%{label}<br>%{value} (MT)<br>%{percent}'

            elif plot['xdata'] == 'Annual Fuel Consumptions':
                xStart = 'FuelConsumption(Total)'
                xEnd = 'V2GPreLoadHours'
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'
                
            elif plot['xdata'] == 'Share of RES':
                xStart = 'ResShareOfPes'
                xEnd = 'ResShareOfElec.Prod.'
                templateFormat = '%{label}<br>%{value}'

            xData = stdDF.loc[xStart:xEnd].index.values.tolist()
            xTitle = ''
            yTitle = plot['ytitle'] + ' (TWh\Year)'

        # getting Y series data
        yData = []
        for yData_i, headers in enumerate(list(stdDF.columns.values)):

            if plot['ydata'][2:4] == '00':
                if plot['ydata'][:2] == headers[:2]:
                    yData.append(headers)
                    next
            elif plot['ydata'] == headers[:4]:
                yData.append(headers)
                break

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


        # drawing the plot
        if plot['tracetype'] == 'Scatter':

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
                    name= srcStd['id'] + ' ' + str(yData[i])[5:]
                    ), row= plot['row'], col= plot['col'])

            # update layout & axes
            figure.update_xaxes({'title_text': xTitle, 'tickmode': xTickMode, 'tick0': 0, 'dtick': xTickStep, 'tickangle': -45}, row= plot['row'], col= plot['col'])
            figure.update_yaxes({'title_text': yTitle, 'tickmode': yTickMode, 'tick0': 0, 'dtick': yTickStep, 'tickangle': 0}, row= plot['row'], col= plot['col'])

        elif plot['tracetype'] == 'Bar':

            # set mode & shape
            styleMode = str(plot['tracestyle'])[:-2].replace(' ', '').strip().lower()

            # build plot
            for i in range(len(yData)):

                if plot['datatype'] == 'annual':
                    figure.add_trace(plygo.Bar(
                        x= xData,
                        y= stdDF.loc[xStart:xEnd, yData[i]].tolist(),
                        text= stdDF.loc[xStart:xEnd, yData[i]].round(3),
                        textfont_color= '#000000',
                        textposition= 'inside',
                        name= srcStd['id'] + ' ' + str(yData[i])[5:]
                        ), row= plot['row'], col= plot['col'])

                else:
                    figure.add_trace(plygo.Bar(
                        x= xData,
                        y= stdDF.loc[xStart:xEnd, yData[i]].tolist(),
                        text= stdDF.loc[xStart:xEnd, yData[i]].astype(int),
                        textfont_color= '#000000',
                        textposition= 'inside',
                        name= srcStd['id'] + ' ' + str(yData[i])[5:]
                        ), row= plot['row'], col= plot['col'])

            # update layout & axes
            figure.update_xaxes({'title_text': xTitle}, row= plot['row'], col= plot['col'])
            figure.update_yaxes({'title_text': yTitle, 'tickmode': yTickMode, 'tick0': 0, 'dtick': yTickStep, 'tickangle': 0}, row= plot['row'], col= plot['col'])
            figure.update_layout({'barmode': styleMode})

        elif plot['tracetype'] == 'Pie':
            if plot['tracestyle'] == 'Domain':
                styleMode = 0
                holeSize = 0.1
                
            else:
                styleMode = 0.05
                holeSize = 0
                
            figure.add_trace(plygo.Pie(
                labels= xData,
                values= stdDF.loc[xStart:xEnd, 'g0-Data1'].tolist(),
                texttemplate= templateFormat,
                showlegend= False,
                hole= holeSize,
                pull= styleMode,
            ))

    figTitles.sort()
    figTitlesID = []
    for cnt1 in range(len(figTitles)):
        figTitlesID.append(figTitles[cnt1][:figTitles[cnt1].find('_') +1])

    figTitlesID = list(dict.fromkeys(figTitlesID))
    figTitles = list(dict.fromkeys(figTitles))
    figTitlesID.sort()

    for cnt2 in range(len(figTitlesID)):
        for cnt3 in range(len(figTitles)):
            if figTitlesID[cnt2][:figTitlesID[cnt2].find('_') +1] == figTitles[cnt3][:figTitles[cnt3].find('_') +1]:
                figTitlesID[cnt2] = figTitlesID[cnt2] + figTitles[cnt3][figTitles[cnt3].find('_') +1:] + ', '

    for cnt4 in range(len(figTitlesID)):
        figTitlesID[cnt4] = figTitlesID[cnt4][figTitlesID[cnt4].find('_') +1:figTitlesID[cnt4].rfind(',')]

    for title_i in range(len(figTitlesID)):
        title = figTitlesID[title_i]
        figure.layout.annotations[title_i].update(text= title)

    figure.update_layout(width= srcFig['width'], height= srcFig['height'], title= srcFig['name'], showlegend= True, template= pio.templates['simple_white'])

    return figure