import re
import pandas as pd
import plotly.graph_objects as plygo
import plotly.io as pio
from plotly.subplots import make_subplots

def PlotterSelective (srcFig= dict, srcPlt= list):

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
        stdDF = pd.read_csv(srcStd['path'], delimiter= ',', low_memory= False, index_col= 'Index')

        stdDF = stdDF.drop(stdDF.index[stdDF.index.get_loc('EnergyplanModel'):stdDF.index.get_loc('Calc.EconomyAndFuel')], axis=0)
        
        try:
            stdDF = stdDF.astype(float)
        except:
            pass

        stdDF.loc['AnnualAverage':'AnnualMinimum'] /= 1000
        
        # calc plot grid position & assign title
        pltPos = plot['pos']
        pltTitle = str(pltPos) + '_' + srcStd['id'] + ' ' + srcStd['name']
        figTitles.append(pltTitle)

        # getting X series data

        if plot['datatype'] == 'hourly':
            
            # set xStart
            if re.fullmatch(r'\d{1, 4}', plot['xstart']):
                xStart = 'h' + plot['xstart']
            elif re.fullmatch(r'h\d{1, 4}', plot['xstart']):
                xStart = plot['xstart']
            elif re.fullmatch(r'd\d{1, 3}', plot['xstart']):
                xStart = int(plot['xstart'][1:])
                xStart = (xStart * 24) - 24 + 1
                xStart = 'h' + str(xStart)
            elif re.fullmatch(r'w\d{1, 2}', plot['xstart']):
                xStart = int(plot['xstart'][1:])
                xStart = ((xStart -1) * 24 * 7) + 1
                xStart = 'h' + str(xStart)
            else:
                xStart = 'h1'

            # set xEnd
            if re.fullmatch(r'\d{1, 4}', plot['xend']):
                xEnd = 'h' + plot['xend']
            elif re.fullmatch(r'h\d{1, 4}', plot['xend']):
                xEnd = plot['xend']
            elif re.fullmatch(r'd\d{1, 3}', plot['xend']):
                xEnd = int(plot['xend'][1:])
                xEnd = xEnd * 24
                xEnd = 'h' + str(xEnd)
            elif re.fullmatch(r'w\d{1, 2}', plot['xend']):
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

            yTitle = plot['ytitle'] + ' (TWh\Year)'

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
                labelsData = xData = stdDF.loc[xStart:xEnd].index.values.tolist()
                valuesData = stdDF.loc[xStart:xEnd, 'g0-Data1'].tolist()
                templateFormat = '%{label}<br>%{value} (MT)<br>%{percent}'

            elif plot['xdata'] == 'Annual Fuel Consumptions':
                xStart = 'FuelConsumption(Total)'
                xEnd = 'V2GPreLoadHours'
                labelsData = xData = stdDF.loc[xStart:xEnd].index.values.tolist()
                valuesData = stdDF.loc[xStart:xEnd, 'g0-Data1'].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'Share of RES':
                xStart = 'ResShareOfPes'
                xEnd = 'ResShareOfElec.Prod.'
                labelsData = xData = stdDF.loc[xStart:xEnd].index.values.tolist()
                valuesData = stdDF.loc[xStart:xEnd, 'g0-Data1'].tolist()
                templateFormat = '%{label}<br>%{value}'

            elif plot['xdata'] == 'Total Elect. Demand':
                xStart = xEnd = 'Annual'
                labelsData = ['Elect. Demand', 'Elect. Demand Cooling', 'Fixed Exp/Imp', 'Flexible Electr, ', 'HH-HP Elect.', 'HH-EB Elect.']
                valuesData = stdDF.loc['Annual', ['0001_ElectrDemand', '0002_ElecdemCooling', '0003_FixedExp/Imp', '0020_FlexibleElectr', '1802_HH-HPElectr', '1804_HH-EBElectr']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'Total Heat Demand':
                xStart = xEnd = 'Annual'
                labelsData = ['DH Demand', 'HH Demand Heat']
                valuesData = stdDF.loc['Annual', ['0004_DHDemand', '1701_HHDemHeat']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'VRES (Renewable Fuel Balance)':
                xStart = xEnd = 'Annual'
                labelsData = ['Wind Electr', 'Offshore Electr', 'PV Electr', 'River Electr', 'Tidal Electr', 'Wave Electr', 'CSP Electr', 'CSP2 Electr']
                valuesData = stdDF.loc['Annual', ['0101_WindElectr', '0102_OffshoreElectr', '0103_PVElectr', '0105_RiverElectr', '0107_TidalElectr', '0106_WaveElectr', '0104_CSPElectr', '0108_CSP2Electr']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'Electricity Consumption':
                xStart = xEnd = 'Annual'
                labelsData = ['Electr Demand', 'Fixed Exp/Imp', 'Flexible Electr', 'Elec. Dem Cooling', 'H2 Electr', 'V2G Charge', 'HP Electr', 'HH-EB Electr', 'Pump Electr', 'Pump2 Electr', 'Hydro Pump', 'EH3 Heat']
                valuesData = stdDF.loc['Annual', ['0001_ElectrDemand', '0003_FixedExp/Imp', '0020_FlexibleElectr', '0002_ElecdemCooling', '2001_H2Electr', '1302_V2GCharge', '0021_HPElectr', '1804_HH-EBElectr', '0801_PumpElectr', '0802_Pump2Electr', '0202_Hydropump', '0016_EH3Heat']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'Electricity Production':
                xStart = xEnd = 'Annual'
                labelsData = ['Wind Electr', 'Offshore Electr', 'PV Electr', 'River Electr', 'Tidal Electr', 'Wave Electr', 'CSP Electr', 'CSP2 Electr', 'HH-CHP Electr', 'Hydro Electr', 'Nuclear Electr', 'Geother. Electr', 'V2G Discharge', 'CSHP Electr', 'CHP Electr', 'Turbine Electr', 'Turbine2 Electr', 'PP Electr', 'PP2 Electr']
                valuesData = stdDF.loc['Annual', ['0101_WindElectr', '0102_OffshoreElectr', '0103_PVElectr', '0105_RiverElectr', '0107_TidalElectr', '0106_WaveElectr', '0104_CSPElectr', '0108_CSP2Electr', '1801_HH-CHPElectr', '0201_HydroElectr', '0701_NuclearElectr', '0702_GeotherElectr', '1303_V2GDischa', '0022_CSHPElectr', '0023_CHPElectr', '0901_TurbineElectr', '0902_Turbine2Electr', '0601_PPElectr', '0602_PP2Electr']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'Electricity Balance':
                xStart = xEnd = 'Annual'
                labelsData = ['Import Electr', 'CEEP Electr', 'EEEP Electr']
                valuesData = stdDF.loc['Annual', ['0025_ImportElectr', '0027_CEEPElectr', '0028_EEEPElectr']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'District Heat Production':
                xStart = xEnd = 'Annual'
                labelsData = ['CSHP 1 Heat', 'Waste 1 Heat', 'Boiler 1 Heat', 'Solar 1 Heat', 'CSHP 2 Heat', 'Waste 2 Heat', 'Geoth 2 Heat', 'CHP 2 Heat', 'HP 2 Heat', 'Boiler 2 Heat', 'EH 2 Heat', 'ELT 2 Heat', 'Solar 2 Heat', 'CSHP 3 Heat', 'Waste 3 Heat', 'Geoth 3 Heat', 'CHP 3 Heat', 'HP 3 Heat', 'Boiler 3 Heat', 'EH 3 Heat', 'ELT 3 Heat', 'Solar 3 Heat']
                valuesData = stdDF.loc['Annual', ['0401_CSHP1Heat', '0402_Waste1Heat', '0005_Boiler1Heat', '0302_Solar1Heat', '0403_CSHP2Heat', '0404_Waste2Heat', '0501_Geoth2Heat', '0006_CHP2Heat', '0007_HP2Heat', '0008_Boiler2Heat', '0009_EH2Heat', '0010_ELT2Heat', '0304_Solar2Heat', '0405_CSHP3Heat', '0406_Waste3Heat', '0504_Geoth3Heat', '0013_CHP3Heat', '0014_HP3Heat', '0015_Boiler3Heat', '0016_EH3Heat', '0017_ELT3Heat', '0306_Solar3Heat']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'District Heat Gr.1':
                xStart = xEnd = 'Annual'
                labelsData = ['CSHP 1 Heat', 'Waste 1 Heat', 'Boiler 1 Heat', 'Solar 1 Heat']
                valuesData = stdDF.loc['Annual', ['0401_CSHP1Heat', '0402_Waste1Heat', '0005_Boiler1Heat', '0302_Solar1Heat']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'District Heat Gr.2':
                xStart = xEnd = 'Annual'
                labelsData = ['CSHP 2 Heat', 'Waste 2 Heat', 'Geoth 2 Heat', 'CHP 2 Heat', 'HP 2 Heat', 'Boiler 2 Heat', 'EH 2 Heat', 'ELT 2 Heat', 'Solar 2 Heat']
                valuesData = stdDF.loc['Annual', ['0403_CSHP2Heat', '0404_Waste2Heat', '0501_Geoth2Heat', '0006_CHP2Heat', '0007_HP2Heat', '0008_Boiler2Heat', '0009_EH2Heat', '0010_ELT2Heat', '0304_Solar2Heat']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'District Heat Gr.3':
                xStart = xEnd = 'Annual'
                labelsData = ['CSHP 3 Heat', 'Waste 3 Heat', 'Geoth 3 Heat', 'CHP 3 Heat', 'HP 3 Heat', 'Boiler 3 Heat', 'EH 3 Heat', 'ELT 3 Heat', 'Solar 3 Heat']
                valuesData = stdDF.loc['Annual', ['0405_CSHP3Heat', '0406_Waste3Heat', '0504_Geoth3Heat', '0013_CHP3Heat', '0014_HP3Heat', '0015_Boiler3Heat', '0016_EH3Heat', '0017_ELT3Heat', '0306_Solar3Heat']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'] == 'Individual (HH) Heating Production':
                xStart = xEnd = 'Annual'
                labelsData = ['HH-EB Electr', 'HH CHP+HP Heat', 'HH Boil. Heat', 'HH Solar Heat']
                valuesData = stdDF.loc['Annual', ['1804_HH-EBElectr', '1702_HHCHP+HPHeat', '1703_HHBoilHeat', '1704_HHSolarHeat']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'
            
            elif plot['xdata'] == 'Heat Balance':
                xStart = xEnd = 'Annual'
                labelsData = ['HH Balan Heat', 'Boiler1 Heat', 'Balance2 Heat', 'Balance3 Heat']
                valuesData = stdDF.loc['Annual', ['1706_HHBalanHeat', '0005_Boiler1Heat', '0012_Balance2Heat', '0019_Balance3Heat']].tolist()
                templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

            elif plot['xdata'][0:16] == 'Investment Costs':

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

                yTitle = ''

            elif plot['xdata'] == 'Installed Capacities':
                break

            if plot['xdata'] != 'Energy Balance':
                xData = stdDF.loc[xStart:xEnd].index.values.tolist()
            xTitle = ''

        # getting Y series data
        yData = []
        if plot['xdata'][0:16] == 'Investment Costs':
            if plot['xdata'] == 'Investment Costs - Total':
                yData = ['g0-Data1']
                yTitle = plot['xdata'] + ' (M Euro)'

            elif plot['xdata'] == 'Investment Costs - Annual':
                yData = ['g0-Data2']
                yTitle = plot['xdata'] + ' (M Euro)'

            elif plot['xdata'] == 'Investment Costs - O & M':
                yData = ['g0-Data3']
                yTitle = plot['xdata'] + ' (M Euro)'

        elif plot['xdata'] == 'Energy Balance':
            for yData_i, headers in enumerate(list(stdDF.columns.values)):
                if headers[:2] == 'g1':
                    yData.append(headers)
            yData.pop()
            yTitle = plot['xdata']

        elif plot['xdata'] == 'Total Elect. Demand':
            yData = ['0001_ElectrDemand', '0002_ElecdemCooling', '0003_FixedExp/Imp', '0020_FlexibleElectr', '1802_HH-HPElectr', '1804_HH-EBElectr']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'Total Heat Demand':
            yData = ['0004_DHDemand', '1701_HHDemHeat']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'VRES (Renewable Fuel Balance)':
            yData = ['0101_WindElectr', '0102_OffshoreElectr', '0103_PVElectr', '0105_RiverElectr', '0107_TidalElectr', '0106_WaveElectr', '0104_CSPElectr', '0108_CSP2Electr']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'Electricity Consumption':
            yData = ['0001_ElectrDemand', '0003_FixedExp/Imp', '0020_FlexibleElectr', '0002_ElecdemCooling', '2001_H2Electr', '1302_V2GCharge', '0021_HPElectr', '1804_HH-EBElectr', '0801_PumpElectr', '0802_Pump2Electr', '0202_Hydropump', '0016_EH3Heat']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'Electricity Production':
            yData = ['0101_WindElectr', '0102_OffshoreElectr', '0103_PVElectr', '0105_RiverElectr', '0107_TidalElectr', '0106_WaveElectr', '0104_CSPElectr', '0108_CSP2Electr', '1801_HH-CHPElectr', '0201_HydroElectr', '0701_NuclearElectr', '0702_GeotherElectr', '1303_V2GDischa', '0022_CSHPElectr', '0023_CHPElectr', '0901_TurbineElectr', '0902_Turbine2Electr', '0601_PPElectr', '0602_PP2Electr']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'Electricity Balance':
            yData = ['0025_ImportElectr', '0027_CEEPElectr', '0028_EEEPElectr']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'District Heat Production':
            yData = ['0401_CSHP1Heat', '0402_Waste1Heat', '0005_Boiler1Heat', '0302_Solar1Heat', '0403_CSHP2Heat', '0404_Waste2Heat', '0501_Geoth2Heat', '0006_CHP2Heat', '0007_HP2Heat', '0008_Boiler2Heat', '0009_EH2Heat', '0010_ELT2Heat', '0304_Solar2Heat', '0405_CSHP3Heat', '0406_Waste3Heat', '0504_Geoth3Heat', '0013_CHP3Heat', '0014_HP3Heat', '0015_Boiler3Heat', '0016_EH3Heat', '0017_ELT3Heat', '0306_Solar3Heat']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'District Heat Gr.1':
            yData = ['0401_CSHP1Heat', '0402_Waste1Heat', '0005_Boiler1Heat', '0302_Solar1Heat']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'District Heat Gr.2':
            yData = ['0403_CSHP2Heat', '0404_Waste2Heat', '0501_Geoth2Heat', '0006_CHP2Heat', '0007_HP2Heat', '0008_Boiler2Heat', '0009_EH2Heat', '0010_ELT2Heat', '0304_Solar2Heat']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'District Heat Gr.3':
            yData = ['0405_CSHP3Heat', '0406_Waste3Heat', '0504_Geoth3Heat', '0013_CHP3Heat', '0014_HP3Heat', '0015_Boiler3Heat', '0016_EH3Heat', '0017_ELT3Heat', '0306_Solar3Heat']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'Individual (HH) Heating Production':
            yData = ['1804_HH-EBElectr', '1702_HHCHP+HPHeat', '1703_HHBoilHeat', '1704_HHSolarHeat']
            yTitle = plot['xdata'] + ' (TWh/year)'

        elif plot['xdata'] == 'Heat Balance':
            yData = ['1706_HHBalanHeat', '0005_Boiler1Heat', '0012_Balance2Heat', '0019_Balance3Heat']
            yTitle = plot['xdata'] + ' (TWh/year)'

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
                styleMode = str(plot['tracestyle']).replace('Only', '').replace(' ', '').strip().lower()
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
                        #yDataHolder = stdDF.columns.get_loc(yData[i])
                        figure.add_trace(plygo.Bar(
                            x= xData, 
                            y= stdDF.iloc[rangeStart:rangeEnd, stdDF.columns.get_loc(yData[i])].tolist(), 
                            #text= stdDF.loc[xStart:xEnd, yData[i]].astype(int), 
                            textfont_color= '#000000', 
                            textposition= 'inside', 
                            name= srcStd['id'] + ' ' + str(yData[i])[str(yData[i]).find('-')+1:]
                            ), row= plot['row'], col= plot['col'])
                        
                    else:
                        figure.add_trace(plygo.Bar(
                            x= xData, 
                            y= stdDF.loc[xStart:xEnd, yData[i]].tolist(), 
                            text= stdDF.loc[xStart:xEnd, yData[i]].astype(int), 
                            textfont_color= '#000000', 
                            textposition= 'inside', 
                            name= srcStd['id'] + ' ' + str(yData[i])[str(yData[i]).find('_')+1:]
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
                labels= labelsData, 
                values= valuesData, 
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
        figTitlesID[cnt4] = figTitlesID[cnt4][figTitlesID[cnt4].find('_') +1:figTitlesID[cnt4].rfind(', ')]

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

def PlotterCollective (srcFig= dict, srcStd= list, xDataSrc= str, xRange= list, traceStyle= str):

    if xDataSrc == 'Energy Balance (per Index)':

        indexList = ['Coal', 'Oil', 'N.Gas', 'Biomass', 'Renewable']
        #indexList = indexList[indexList.index(xStart):indexList.index(xEnd)+1]

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
            showlegend= srcFig['legend'], 
            template= pio.templates['simple_white'])

        return figure

    elif xDataSrc == 'Installed Capacities (per Index)':

        list1 = ['InputCapPpEl', 'InputCapChp2El', 'InputCapChp3El', 'InputCapPp2El', 'InputNuclearCap', 'InputGeopowerCap', 'InputHydroCap', 'InputRes1Capacity', 'InputRes2Capacity', 'InputRes3Capacity', 'InputRes4Capacity', 'InputRes5Capacity', 'InputRes6Capacity', 'InputRes7Capacity', 'InputCapHp2El', 'InputCapHp3El', 'InputCapElttransEl', 'InputEh2', 'InputEh3', 'InputCapBoiler2Th', 'InputCapBoiler3Th', 'InputCapChp2Thermal', 'InputCapChp3Thermal']

        list2 = ['PP1', 'CHP2', 'CHP3', 'PP2', 'Nuclear', 'Geopower', 'Hydro', 'Res1', 'Res2', 'Res3', 'Res4', 'Res5', 'Res6', 'Res7', 'Heat Pump 2', 'Heat Pump 3', 'Electrolysers', 'Boiler 2', 'Boiler 3 ', 'Boiler 2 Thermal', 'Boiler 3 Thermal', 'CHP2 Thermal', 'CHP3 Thermal']

        #xStartIndex = list2.index(xStart)
        #xEndIndex = list2.index(xEnd)+1

        #xStart = list1[xStartIndex]
        #try:
        #    xEnd = list1[xEndIndex]
        #except:
        #    xEnd = list1[-1]

        #list1 = list1[xStartIndex:xEndIndex]
        #list2 = list2[xStartIndex:xEndIndex]

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
            showlegend= srcFig['legend'], 
            template= pio.templates['simple_white'])

        return figure

    elif xDataSrc == 'Total Elect. Demand':

        SumDF = pd.DataFrame(0, index= ['test'], columns=['0001_ElectrDemand', '0002_ElecdemCooling', '0003_FixedExp/Imp', '0020_FlexibleElectr', '1802_HH-HPElectr', '1804_HH-EBElectr'])

        for study in range(len(srcStd)):

            stdDF = pd.read_csv(srcStd[study]['path'], delimiter=',', low_memory=False, index_col='Index')

            stdValues = stdDF.loc['Annual', ['0001_ElectrDemand', '0002_ElecdemCooling', '0003_FixedExp/Imp', '0020_FlexibleElectr', '1802_HH-HPElectr', '1804_HH-EBElectr']].tolist()

            SumDF.loc[srcStd[study]['name']] = stdValues

        SumDF.drop(['test'], axis= 0, inplace=True)
        print(len(SumDF.index.values.tolist()))
        
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
                #x= SumDF.index[i], 
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
            showlegend= srcFig['legend'], 
            template= pio.templates['simple_white'])

        return figure

    elif xDataSrc == 'Total Heat Demand':

        SumDF = pd.DataFrame(0, index= ['test'], columns=['0004_DHDemand', '1701_HHDemHeat'])

        for study in range(len(srcStd)):

            stdDF = pd.read_csv(srcStd[study]['path'], delimiter=',', low_memory=False, index_col='Index')

            stdValues = stdDF.loc['Annual', ['0004_DHDemand', '1701_HHDemHeat']].tolist()

            SumDF.loc[srcStd[study]['name']] = stdValues

        SumDF.drop(['test'], axis= 0, inplace=True)
        print(len(SumDF.index.values.tolist()))
        
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
                #x= SumDF.index[i], 
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
            showlegend= srcFig['legend'], 
            template= pio.templates['simple_white'])

        return figure
