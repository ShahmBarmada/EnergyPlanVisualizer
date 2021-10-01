import re
import pandas as pd
import plotly.graph_objects as plygo
import plotly.io as pio
from plotly.subplots import make_subplots

def PlotterSelective (srcFig = dict, srcPlt = list):

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

            if plot['xdata'][0:16] == 'Investment Costs':

                rangeStart = stdDF.index.get_loc('TotalAnnualCosts')
                rangeStart += 1
                
                rangeEnd = stdDF.iloc[rangeStart:rangeStart+100].index.get_loc('Coal')
                rangeEnd = rangeEnd + rangeStart

                xStart = stdDF.iloc[rangeStart:rangeEnd].index[0]
                xEnd = stdDF.iloc[rangeStart:rangeEnd].index[-1]

                if plot['xdata'] == 'Investment Costs - Total':
                    yData = ['g0-Data1']

                elif plot['xdata'] == 'Investment Costs - Annual':
                    yData = ['g0-Data2']

                elif plot['xdata'] == 'Investment Costs - O & M':
                    yData = ['g0-Data3']

                yTitle = plot['xdata'] + ' (M Euro)'

            elif plot['xdata'] == 'Energy Balance':

                rangeStart = stdDF.index.get_loc('TotalAnnualCosts')
                rangeStart = rangeStart + stdDF.iloc[rangeStart:rangeStart+100].index.get_loc('Coal')
                
                rangeEnd = stdDF.iloc[rangeStart:rangeStart+100].index.get_loc('Renewable')
                rangeEnd = rangeEnd + rangeStart +1

                xData = stdDF.iloc[rangeStart:rangeEnd].index.values.tolist()
                xStart = stdDF.iloc[rangeStart:rangeEnd].index[0]
                xEnd = stdDF.iloc[rangeStart:rangeEnd].index[-1]

            else:

                if plot['xdata'] == 'Power Values - Totals':
                    xStart = xEnd = 'Annual'
                elif plot['xdata'] == 'Power Values - Annual Average':
                    xStart = xEnd = 'AnnualAverage'
                elif plot['xdata'] == 'Power Values - Annual Maximum':
                    xStart = xEnd = 'AnnualMaximum'
                elif plot['xdata'] == 'Power Values - Annual Minimum':
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

                yTitle = plot['ytitle'] + ' (TWh\Year)'

            if plot['xdata'] != 'Energy Balance':
                xData = stdDF.loc[xStart:xEnd].index.values.tolist()
            xTitle = ''

        # getting Y series data
        yData = []
        if plot['xdata'][0:16] == 'Investment Costs':
            pass

        elif plot['xdata'] == 'Energy Balance':
            for yData_i, headers in enumerate(list(stdDF.columns.values)):
                if headers[:2] == 'g1':
                    yData.append(headers)
            yData.pop()

        else:
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
        if plot['tracetype'] == 'Scatter Plot':

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
                    name= srcStd['id'] + ' ' + str(yData[i])[str(yData[i]).find('_'):]
                    ), row= plot['row'], col= plot['col'])

            # update layout & axes
            figure.update_xaxes({'title_text': xTitle, 'tickmode': xTickMode, 'tick0': 0, 'dtick': xTickStep, 'tickangle': -45}, row= plot['row'], col= plot['col'])
            figure.update_yaxes({'title_text': yTitle, 'tickmode': yTickMode, 'tick0': 0, 'dtick': yTickStep, 'tickangle': 0}, row= plot['row'], col= plot['col'])

        elif plot['tracetype'] == 'Bar Chart':

            # set mode & shape
            styleMode = str(plot['tracestyle'])[:-2].replace(' ', '').strip().lower()

            # build plot
            for i in range(len(yData)):

                if plot['datatype'] == 'annual':
                    if plot['xdata'] == 'Energy Balance':
                        yTitle = ''
                        #yDataHolder = stdDF.columns.get_loc(yData[i])
                        figure.add_trace(plygo.Bar(
                            x= xData,
                            y= stdDF.iloc[rangeStart:rangeEnd, stdDF.columns.get_loc(yData[i])].tolist(),
                            #text= stdDF.loc[xStart:xEnd, yData[i]].round(3),
                            textfont_color= '#000000',
                            textposition= 'inside',
                            name= srcStd['id'] + ' ' + str(yData[i])[str(yData[i]).find('-')+1:]
                            ), row= plot['row'], col= plot['col'])
                        
                    else:
                        figure.add_trace(plygo.Bar(
                            x= xData,
                            y= stdDF.loc[xStart:xEnd, yData[i]].tolist(),
                            #text= stdDF.loc[xStart:xEnd, yData[i]].round(3),
                            textfont_color= '#000000',
                            textposition= 'inside',
                            name= srcStd['id'] + ' ' + str(yData[i])[str(yData[i]).find('_'):]
                            ), row= plot['row'], col= plot['col'])

                else:
                    figure.add_trace(plygo.Bar(
                        x= xData,
                        y= stdDF.loc[xStart:xEnd, yData[i]].tolist(),
                        text= stdDF.loc[xStart:xEnd, yData[i]].astype(int),
                        textfont_color= '#000000',
                        textposition= 'inside',
                        name= srcStd['id'] + ' ' + str(yData[i])[str(yData[i]).find('_'):]
                        ), row= plot['row'], col= plot['col'])

            # update layout & axes
            figure.update_xaxes({'title_text': xTitle}, row= plot['row'], col= plot['col'])
            figure.update_yaxes({'title_text': yTitle, 'tickmode': yTickMode, 'tick0': 0, 'dtick': yTickStep, 'tickangle': 0}, row= plot['row'], col= plot['col'])
            figure.update_layout({'barmode': styleMode})

        elif plot['tracetype'] == 'Pie Chart':
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
                hole= holeSize,
                pull= styleMode,
            ))

        elif plot['tracetype'] == 'Box Plot':
            if plot['tracestyle'] == 'Whiskers & Points':
                styleMode = 'all'
            elif plot['tracestyle'] == 'Whiskers':
                styleMode = False
            elif plot['tracestyle'] == 'OutLiers':
                styleMode = 'suspectedoutliers'
            elif plot['tracestyle'] == 'Whiskers & OutLiers':
                styleMode = 'outliers'

            for i in range(len(xData)):
                xDataSeries = []
                for num1 in range(17):
                    xDataSeries.append(xData[i])

                figure.add_trace(plygo.Box(
                    x= xDataSeries,
                    y= stdDF.iloc[rangeStart + i, 3:20].tolist(),
                    boxpoints= styleMode,
                    name= xData[i],
                    jitter= 0.3
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

    figure.update_layout(
        uniformtext_minsize=18,
        font_size= srcFig['font'],
        width= srcFig['width'],
        height= srcFig['height'],
        title= srcFig['name'],
        showlegend= srcFig['legend'],
        template= pio.templates['simple_white'])

    return figure

def PlotterCollective (srcFig = dict, srcStd = list, xDataSrc = str):

    if xDataSrc == 'Energy Balance':
        SumDF = pd.DataFrame(0, index=['Coal', 'Oil', 'N.Gas', 'Biomass', 'Renewable', 'H2Etc.', 'Biofuel', 'Nucl/Ccs'], columns=['test'])

        for study in range(len(srcStd)):
            stdDF = pd.read_csv(srcStd[study]['path'], delimiter=',', low_memory=False, index_col='Index')
    
            rangeStart = stdDF.index.get_loc('TotalAnnualCosts')
            rangeStart = rangeStart + stdDF.iloc[rangeStart:rangeStart+100].index.get_loc('Coal')
                    
            rangeEnd = stdDF.iloc[rangeStart:rangeStart+100].index.get_loc('Nucl/Ccs')
            rangeEnd = rangeEnd + rangeStart +1
    
            xData = stdDF.iloc[rangeStart:rangeEnd].index.values.tolist()
            
            stdDF = stdDF.iloc[rangeStart:rangeEnd]
            stdDF = stdDF.loc[:, 'g1-Total']
    
            SumDF.insert(0, 'std' + str(study), stdDF)

        SumDF.drop(['test'], axis= 1, inplace=True)

        figure = make_subplots()

        for i in range(len(SumDF.index.values.tolist())):
            xDataSeries = []
            for num1 in range(len(SumDF.columns.values.tolist())):
                xDataSeries.append(xData[i])

            figure.add_trace(plygo.Box(
                x= xDataSeries,
                y= SumDF.iloc[i].tolist(),
                boxpoints= 'all',
                name= xData[i],
                jitter= 0.3
            ))
            
        figure.update_yaxes({'title_text': '(TWh\Year)'})
        figure.update_layout(
            uniformtext_minsize=18,
            font_size= srcFig['font'],
            width= srcFig['width'],
            height= srcFig['height'],
            title= srcFig['name'],
            showlegend= srcFig['legend'],
            template= pio.templates['simple_white'])

        return figure

    elif xDataSrc == 'Installed Capacities':
        #SumDF = pd.DataFrame(0, index=['Condensing power plant 1','CHP plants (elect. capacity) gr.2','CHP plants (elect. capacity) gr.3','Condensing power plant 2','Nuclear','Geothermal plants','Dammed hydro','RES1','RES2','RES3','RES4','RES5','RES6','RES7','DH - Heat pump gr.2','DH - Heat pump gr.3','Electrolysers','DH - Electric boiler gr.2','DH - Electric boiler gr.3','DH - Boiler gr.2','DH - Boiler gr.3','DH - CHP (thermal capacity) gr.2','DH - CHP (thermal capacity) gr.3'], columns=['test'])

        SumDF = pd.DataFrame(0, index=['InputCapPpEl','InputCapChp2El','InputCapChp3El','InputCapPp2El','InputNuclearCap','InputGeopowerCap','InputHydroCap','InputRes1Capacity','InputRes2Capacity','InputRes3Capacity','InputRes4Capacity','InputRes5Capacity','InputRes6Capacity','InputRes7Capacity','InputCapHp2El','InputCapHp3El','InputCapElttransEl','InputEh2','InputEh3','InputCapBoiler2Th','InputCapBoiler3Th','InputCapChp2Thermal','InputCapChp3Thermal'], columns=['test'])

        for study in range(len(srcStd)):
            stdDF = pd.read_csv(srcStd[study]['path'], delimiter=',', low_memory=False, index_col='Index')
    
            rangeStart = stdDF.index.get_loc('InputCapPpEl')   
            rangeEnd = stdDF.index.get_loc('InputCapChp3Thermal') +1
    
            xData = stdDF.iloc[rangeStart:rangeEnd].index.values.tolist()
            
            stdDF = stdDF.iloc[rangeStart:rangeEnd]
            stdDF = stdDF.loc[:, 'g0-Data1']
    
            SumDF.insert(0, 'std' + str(study), stdDF)

        SumDF.drop(['test'], axis= 1, inplace=True)

        figure = make_subplots()

        for i in range(len(SumDF.index.values.tolist())):
            xDataSeries = []
            for num1 in range(len(SumDF.columns.values.tolist())):
                xDataSeries.append(xData[i])

            figure.add_trace(plygo.Box(
                x= xDataSeries,
                y= SumDF.iloc[i].tolist(),
                boxpoints= 'all',
                name= xData[i],
                jitter= 0.3
            ))
            
        figure.update_yaxes({'title_text': '(TWh\Year)'})
        figure.update_layout(
            uniformtext_minsize=18,
            font_size= srcFig['font'],
            width= srcFig['width'],
            height= srcFig['height'],
            title= srcFig['name'],
            showlegend= srcFig['legend'],
            template= pio.templates['simple_white'])

        return figure

    elif xDataSrc == 'Total Elect. Demand':
        pass

    elif xDataSrc == 'Total Heat Demand':
        pass
