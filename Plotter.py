import re
import sys
import pandas as pd
import numpy as np
import plotly.graph_objects as plygo
import plotly.io as pio
from plotly.subplots import make_subplots

def PlotterSelective (srcFig= dict, srcPlt= list, visibleLegend= bool, visibleTitle= bool):

    ### loop the plots and return a unique list of positions in grid

    i = 0
    posList = []

    for i in range(len(srcPlt)):

        if srcPlt[i]['pos'] in posList:
            pass
        else:
            posList.append(srcPlt[i]['pos'])

    posList.sort()

    ### group plots into dictionaries by pos and trace type

    i, j = 0, 0
    srcPltGrouped = []
    pltGroupDict = {'pos': '', 'trace': [], 'plts': []}

    for i in range(len(posList)):
        pltGroupDict['pos'] = posList[i]

        for j in range(len(srcPlt)):

            if srcPlt[j]['pos'] == posList[i]:
                pltGroupDict['plts'].append(srcPlt[j])
                
                if srcPlt[j]['tracetype'] in pltGroupDict['trace']:
                    pass

                else:
                    pltGroupDict['trace'].append(srcPlt[j]['tracetype'])
                
        srcPltGrouped.append(pltGroupDict)
        pltGroupDict = {'pos': '', 'trace': [], 'plts': []}

    ### check for pie charts (plotly limitation)

    i = 0

    if len(srcPltGrouped) == 1:
        if len(srcPltGrouped[0]['trace']) > 1 and 'Pie Chart' in srcPltGrouped[0]['trace']:
            print('Error 1: Can\'t plot Pie chart with other chart types in the same plot, Plotly Lib limitation')
            sys.exit()

        elif len(srcPltGrouped[i]['plts']) > 1 and 'Pie Chart' in srcPltGrouped[i]['trace']:
            print('Error 2: Can\'t plot multiple Pie charts in the same plot, Plotly Lib limitation')
            sys.exit()

    else:
        for i in range(len(srcPltGrouped)):
            if 'Pie Chart' in srcPltGrouped[i]['trace']:
                print('Error 3: Can\'t plot multiple Pie charts in the same figure, Plotly Lib limitation')
                sys.exit()

    ### build figure subplots

    figure = make_subplots(rows= srcFig['rows'], cols= srcFig['cols'], horizontal_spacing= 0.1, vertical_spacing= 0.23)


    ### build data frames

    i, j = 0, 0
    sumDF = pd.read_csv(srcPlt[0]['datasrc']['path'], delimiter= ',', low_memory= False, index_col= 'Index')
    sumDF[:] = np.NaN
    sumDF.drop(sumDF.columns[1:], axis= 1, inplace= True)
    sumDF.rename({sumDF.index[0]: 'ID', sumDF.index[1]: 'Pos'}, inplace= True)

    #sumDF = pd.DataFrame(0, index= ['Pos', 'ID'], columns=['initial'])

    for i in range(len(srcPltGrouped)):

        statMean, statMedian, statOnly, stackLines = False, False, False, False

        for j in range(len(srcPltGrouped[i]['plts'])):
            plot = srcPltGrouped[i]['plts'][j]

            ### check and set statistics switches

            if 'Pie Chart' in srcPltGrouped[i]['trace'] or 'Box Plot' in srcPltGrouped[i]['trace']:
                pass
            else:
                statMean = statMean or plot['mean']
                statMedian = statMedian or plot['median']
                statOnly = statOnly or plot['statonly']
                stackLines = stackLines or plot['stack']

            ### get data source

            srcStd = plot['datasrc']
            stdDF = pd.read_csv(srcStd['path'], delimiter= ',', low_memory= False, index_col= 'Index')

            ### drop text values

            stdDF = stdDF.drop(stdDF.index[stdDF.index.get_loc('EnergyplanModel'):stdDF.index.get_loc('Calc.EconomyAndFuel')], axis=0)

            ### cast cells data type

            try:
                stdDF = stdDF.astype(float)
            except:
                pass
            
            ### convert Annual values from TWh -> MWh

            stdDF.loc['AnnualAverage':'AnnualMinimum'] /= 1000

            ### calc X series

            if plot['datatype'] == 'hourly':

                ### set X start

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

                ### set X end

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

                ### Get X Data (by type: time based or data based) and set X axes title

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

                ### Set Y axes title

                yTitle = plot['ytitle'] + ' (MW)'

            elif plot['datatype'] == 'monthly':

                ### set X start and end

                xStart = plot['xstart']
                xEnd = plot['xend']

                ### Get X Data (by type: time based or data based) and set X axes title

                xData = stdDF.loc[xStart:xEnd].index.values.tolist()

                if plot['xtype'] == 'time':
                    xTitle = 'Time Range'
                elif plot['xtype'] == 'data':
                    xTitle = plot['xtitle'] + ' (MW)'

                ### Set Y axes title

                yTitle = plot['ytitle'] + ' (MW)'
            
            ### calc Y series
            
            yData = []

            for yData_i, headers in enumerate(list(stdDF.columns.values)):
                if plot['ydata'][2:4] == '00':
                    if plot['ydata'][:2] == headers[:2]:
                        yData.append(headers)
                        next
                elif plot['ydata'] == headers[:4]:
                    yData.append(headers)
                    break

            ### add index and columns to sumDF

            sumDF = pd.merge(left= sumDF, right= stdDF.loc[xData, yData], how= 'left', left_on= 'Index', right_on= 'Index')

    sumDF.drop(['g0-Data1'], axis= 1, inplace=True)
    sumDF.dropna(axis= 0, how= 'all', inplace= True)

    colsList = sumDF.columns.values.tolist()
    
    i = 0
    for i in range(len(colsList)):
        colsList[i] = colsList[i][5:].replace('_x','').replace('_y','') + str(i)

    sumDF.columns = colsList

    if statMean:
        colMean = sumDF.mean(axis= 1).tolist()
        sumDF.insert(0, 'Mean', colMean)

    if statMedian:
        colMedian = sumDF.median(axis= 1).tolist()
        sumDF.insert(0, 'Median', colMedian)

    if statOnly and ('Mean' in sumDF.columns.values.tolist() or 'Median' in sumDF.columns.values.tolist()):
        #if ('Mean' in sumDF.columns.values.tolist() or 'Median' in sumDF.columns.values.tolist()):
            for col in sumDF:
                if col == 'Median' or col == 'Mean':
                    pass
                else:
                    sumDF.drop([col], axis= 1, inplace= True)
    else:
        print("worked")

    xData = sumDF.index.values.tolist()
    yData = sumDF.columns.values.tolist()

    count = 0

    for count in range(len(yData)):
        figure.add_trace(plygo.Scatter(
            x= xData, 
            y= sumDF.loc[:, yData[count]], 
            connectgaps= False, 
            fill= 'none', 
            mode= 'lines+markers', 
            #line= 'linear', 
            name= yData[count]
            ), row= 1, col= 1)

#        figure.add_trace(plygo.Bar(
#            x= xData, 
#            y= sumDF.loc[:, yData[count]], 
#            #text= yData[count], 
#            textfont_color= '#000000', 
#            textposition= 'inside', 
#            name= yData[count]
#            ), row= 1, col= 1)

    ### update layout & axes
    figure.update_xaxes({'title_text': xTitle, 'tickmode': 'auto', 'tick0': 0, 'tickangle': -45}, row= 1, col= 1)
    figure.update_yaxes({'title_text': yTitle, 'tickmode': 'auto', 'tick0': 0, 'tickangle': 0}, row= 1, col= 1)

            
    figure.update_layout(
        uniformtext_minsize=18, 
        font_size= srcFig['font'], 
        width= srcFig['width'], 
        height= srcFig['height'], 
        title= srcFig['name'], 
        showlegend= visibleLegend, 
        template= pio.templates['simple_white'])

    return figure


def PlotterCollective (srcFig= dict, srcStd= list, xDataSrc= str, xRange= list, traceStyle= str, visibleLegend= bool, visibleTitle= bool):

    if xDataSrc == 'Energy Balance (per Index)':

        indexList = ['Coal', 'Oil', 'N.Gas', 'Biomass', 'Renewable']

        SumDF = pd.DataFrame(0, index= indexList, columns=['test'])

        for study in range(len(srcStd)):
            stdDF = pd.read_csv(srcStd[study]['path'], delimiter=',', low_memory=False, index_col='Index')
    
            rangeStart = stdDF.index.get_loc('TotalAnnualCosts')
            rangeStart = rangeStart + stdDF.iloc[rangeStart:rangeStart+100].index.get_loc(indexList[0])
                    
            rangeEnd = stdDF.iloc[rangeStart:rangeStart+100].index.get_loc(indexList[-1])
            rangeEnd = rangeEnd + rangeStart +1
    
            xData = stdDF.iloc[rangeStart:rangeEnd].index.values.tolist()
            
            stdDF = stdDF.iloc[rangeStart:rangeEnd]
            stdDF = stdDF.loc[:, 'g1-Total']
    
            SumDF.insert(0, 'std' + str(study), stdDF)

        SumDF.drop(['test'], axis= 1, inplace=True)

        xRangeTarget = SumDF.index.values.tolist()
        for j in range(len(xRangeTarget)):
            if xRangeTarget[j] not in xRange:
                SumDF.drop([xRangeTarget[j]], axis= 0, inplace=True)

        figure = make_subplots()

        if traceStyle == 'Whiskers & Points':
            styleMode = 'all'
        elif traceStyle == 'Whiskers':
            styleMode = False
        elif traceStyle == 'OutLiers':
            styleMode = 'suspectedoutliers'
        elif traceStyle == 'Whiskers & OutLiers':
            styleMode = 'outliers'

        for i in range(len(SumDF.index.values.tolist())):
            xDataSeries = []
            for num1 in range(len(SumDF.columns.values.tolist())):
                xDataSeries.append(xData[i])

            figure.add_trace(plygo.Box(
                x= xDataSeries, 
                y= SumDF.iloc[i].tolist(), 
                boxpoints= styleMode, 
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
            showlegend= visibleLegend, 
            template= pio.templates['simple_white'])

        return figure

    elif xDataSrc == 'Installed Capacities (per Index)':

        list1 = ['InputCapPpEl', 'InputCapChp2El', 'InputCapChp3El', 'InputCapPp2El', 'InputNuclearCap', 'InputGeopowerCap', 'InputHydroCap', 'InputRes1Capacity', 'InputRes2Capacity', 'InputRes3Capacity', 'InputRes4Capacity', 'InputRes5Capacity', 'InputRes6Capacity', 'InputRes7Capacity', 'InputCapHp2El', 'InputCapHp3El', 'InputCapElttransEl', 'InputEh2', 'InputEh3', 'InputCapBoiler2Th', 'InputCapBoiler3Th', 'InputCapChp2Thermal', 'InputCapChp3Thermal']

        list2 = ['PP1', 'CHP2', 'CHP3', 'PP2', 'Nuclear', 'Geopower', 'Hydro', 'Res1', 'Res2', 'Res3', 'Res4', 'Res5', 'Res6', 'Res7', 'Heat Pump 2', 'Heat Pump 3', 'Electrolysers', 'Boiler 2', 'Boiler 3 ', 'Boiler 2 Thermal', 'Boiler 3 Thermal', 'CHP2 Thermal', 'CHP3 Thermal']

        SumDF = pd.DataFrame(0, index= list1, columns=['test'])

        for study in range(len(srcStd)):
            stdDF = pd.read_csv(srcStd[study]['path'], delimiter=',', low_memory=False, index_col='Index')

            rangeStart = stdDF.index.get_loc(list1[0])   
            rangeEnd = stdDF.index.get_loc(list1[-1]) +1

            stdDF = stdDF.iloc[rangeStart:rangeEnd]
            stdDF = stdDF.loc[:, 'g0-Data1']
            stdDF = stdDF.astype(float)

            SumDF.insert(0, 'std' + str(study), stdDF)

        SumDF.drop(['test'], axis= 1, inplace=True)

        SumDF.rename(index= dict(zip(list1, list2)), inplace= True)

        xRangeTarget = SumDF.index.values.tolist()
        for j in range(len(xRangeTarget)):
            if xRangeTarget[j] not in xRange:
                SumDF.drop([xRangeTarget[j]], axis= 0, inplace=True)

        SumDF.sort_index(axis=0, inplace=True)

        xData = SumDF.index.values.tolist()

        figure = make_subplots()

        if traceStyle == 'Whiskers & Points':
            styleMode = 'all'
        elif traceStyle == 'Whiskers':
            styleMode = False
        elif traceStyle == 'OutLiers':
            styleMode = 'suspectedoutliers'
        elif traceStyle == 'Whiskers & OutLiers':
            styleMode = 'outliers'

        for i in range(len(SumDF.index.values.tolist())):
            xDataSeries = []
            for num1 in range(len(SumDF.columns.values.tolist())):
                xDataSeries.append(xData[i])

            figure.add_trace(plygo.Box(
                x= xDataSeries, 
                y= SumDF.iloc[i].tolist(), 
                boxpoints= styleMode, 
                name= xData[i], 
                jitter= 0.3
            ))
            
        figure.update_yaxes({'title_text': '(MW)'})
        figure.update_layout(
            uniformtext_minsize=18, 
            font_size= srcFig['font'], 
            width= srcFig['width'], 
            height= srcFig['height'], 
            title= srcFig['name'], 
            showlegend= visibleLegend, 
            template= pio.templates['simple_white'])

        return figure

    elif xDataSrc == 'Total Elect. Demand':

        SumDF = pd.DataFrame(0, index= ['test'], columns=['0001_ElectrDemand', '0002_ElecdemCooling', '0003_FixedExp/Imp', '0020_FlexibleElectr', '1802_HH-HPElectr', '1804_HH-EBElectr'])

        for study in range(len(srcStd)):

            stdDF = pd.read_csv(srcStd[study]['path'], delimiter=',', low_memory=False, index_col='Index')

            stdValues = stdDF.loc['Annual', ['0001_ElectrDemand', '0002_ElecdemCooling', '0003_FixedExp/Imp', '0020_FlexibleElectr', '1802_HH-HPElectr', '1804_HH-EBElectr']].tolist()

            SumDF.loc[srcStd[study]['name']] = stdValues

        SumDF.drop(['test'], axis= 0, inplace=True)
        
        figure = make_subplots()

        if traceStyle == 'Whiskers & Points':
            styleMode = 'all'
        elif traceStyle == 'Whiskers':
            styleMode = False
        elif traceStyle == 'OutLiers':
            styleMode = 'suspectedoutliers'
        elif traceStyle == 'Whiskers & OutLiers':
            styleMode = 'outliers'

        for i in range(len(SumDF.index.values.tolist())):
            figure.add_trace(plygo.Box(
                y= SumDF.iloc[i].tolist(), 
                boxpoints= styleMode, 
                name= SumDF.index[i], 
                jitter= 0.3
            ))
            
        figure.update_yaxes({'title_text': '(TWh\Year)'})
        figure.update_layout(
            uniformtext_minsize=18, 
            font_size= srcFig['font'], 
            width= srcFig['width'], 
            height= srcFig['height'], 
            title= srcFig['name'], 
            showlegend= visibleLegend, 
            template= pio.templates['simple_white'])

        return figure

    elif xDataSrc == 'Total Heat Demand':

        SumDF = pd.DataFrame(0, index= ['test'], columns=['0004_DHDemand', '1701_HHDemHeat'])

        for study in range(len(srcStd)):

            stdDF = pd.read_csv(srcStd[study]['path'], delimiter=',', low_memory=False, index_col='Index')

            stdValues = stdDF.loc['Annual', ['0004_DHDemand', '1701_HHDemHeat']].tolist()

            SumDF.loc[srcStd[study]['name']] = stdValues

        SumDF.drop(['test'], axis= 0, inplace=True)
        
        figure = make_subplots()

        if traceStyle == 'Whiskers & Points':
            styleMode = 'all'
        elif traceStyle == 'Whiskers':
            styleMode = False
        elif traceStyle == 'OutLiers':
            styleMode = 'suspectedoutliers'
        elif traceStyle == 'Whiskers & OutLiers':
            styleMode = 'outliers'

        for i in range(len(SumDF.index.values.tolist())):
            figure.add_trace(plygo.Box(
                y= SumDF.iloc[i].tolist(), 
                boxpoints= styleMode, 
                name= SumDF.index[i], 
                jitter= 0.3
            ))
            
        figure.update_yaxes({'title_text': '(TWh\Year)'})
        figure.update_layout(
            uniformtext_minsize=18, 
            font_size= srcFig['font'], 
            width= srcFig['width'], 
            height= srcFig['height'], 
            title= srcFig['name'], 
            showlegend= visibleLegend, 
            template= pio.templates['simple_white'])

        return figure
