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
    tempDF = pd.read_csv(srcPlt[0]['datasrc']['path'], delimiter= ',', low_memory= False, index_col= 'Index')
    tempDF[:] = np.NaN
    tempDF.insert(0,'temp0',np.NaN)
    tempDF.drop(tempDF.columns[1:], axis= 1, inplace= True)
    tempDF.drop(tempDF.index[tempDF.index.get_loc('EnergyplanModel'):tempDF.index.get_loc('Calc.EconomyAndFuel')], axis=0, inplace= True)
    pltInfoList = ['pltid', 'stdid', 'stdname', 'datatype', 'tracetype', 'tracestyle', 'tracefill', 'xstart', 'xend', 'xtitle', 'ytitle', 'xtick', 'xstep', 'ytick', 'ystep']
    sumDF = pd.DataFrame(0, pltInfoList, ['temp0'])
    sumDF = pd.concat([sumDF,tempDF])

    for i in range(len(srcPltGrouped)):

        sumDF.reset_index(inplace= True)
        sumDF['indNum'] = sumDF.index
        sumDF.set_index('index', inplace= True, drop= True)
        sumDF = sumDF[['indNum']]
        
        statMean, statMedian, statOnly, stackLines = False, False, False, False
        posRow = int(str(srcPltGrouped[i]['pos'])[:1])
        posCol = int(str(srcPltGrouped[i]['pos'])[-1:])

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
                    valuesData = stdDF.loc['Annual', ['0101_WindElectr', '0102_OffshoreElectr', '0103_PVElectr', '0105_RiverElectr', '0107_TidalElectr', '0106_WaveElectr', '0104_CSPElectr',   '0108_CSP2Electr']].tolist()
                    templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

                elif plot['xdata'] == 'Electricity Consumption':
                    xStart = xEnd = 'Annual'
                    labelsData = ['Electr Demand', 'Fixed Exp/Imp', 'Flexible Electr', 'Elec. Dem Cooling', 'H2 Electr', 'V2G Charge', 'HP Electr', 'HH-EB Electr', 'Pump Electr', 'Pump2 Electr',  'Hydro Pump', 'EH3 Heat']
                    valuesData = stdDF.loc['Annual', ['0001_ElectrDemand', '0003_FixedExp/Imp', '0020_FlexibleElectr', '0002_ElecdemCooling', '2001_H2Electr', '1302_V2GCharge', '0021_HPElectr',   '1804_HH-EBElectr', '0801_PumpElectr', '0802_Pump2Electr', '0202_Hydropump', '0016_EH3Heat']].tolist()
                    templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

                elif plot['xdata'] == 'Electricity Production':
                    xStart = xEnd = 'Annual'
                    labelsData = ['Wind Electr', 'Offshore Electr', 'PV Electr', 'River Electr', 'Tidal Electr', 'Wave Electr', 'CSP Electr', 'CSP2 Electr', 'HH-CHP Electr', 'Hydro Electr',   'Nuclear Electr', 'Geother. Electr', 'V2G Discharge', 'CSHP Electr', 'CHP Electr', 'Turbine Electr', 'Turbine2 Electr', 'PP Electr', 'PP2 Electr']
                    valuesData = stdDF.loc['Annual', ['0101_WindElectr', '0102_OffshoreElectr', '0103_PVElectr', '0105_RiverElectr', '0107_TidalElectr', '0106_WaveElectr', '0104_CSPElectr',   '0108_CSP2Electr', '1801_HH-CHPElectr', '0201_HydroElectr', '0701_NuclearElectr', '0702_GeotherElectr', '1303_V2GDischa', '0022_CSHPElectr', '0023_CHPElectr',    '0901_TurbineElectr', '0902_Turbine2Electr', '0601_PPElectr', '0602_PP2Electr']].tolist()
                    templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

                elif plot['xdata'] == 'Electricity Balance':
                    xStart = xEnd = 'Annual'
                    labelsData = ['Import Electr', 'CEEP Electr', 'EEEP Electr']
                    valuesData = stdDF.loc['Annual', ['0025_ImportElectr', '0027_CEEPElectr', '0028_EEEPElectr']].tolist()
                    templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

                elif plot['xdata'] == 'District Heat Production':
                    xStart = xEnd = 'Annual'
                    labelsData = ['CSHP 1 Heat', 'Waste 1 Heat', 'Boiler 1 Heat', 'Solar 1 Heat', 'CSHP 2 Heat', 'Waste 2 Heat', 'Geoth 2 Heat', 'CHP 2 Heat', 'HP 2 Heat', 'Boiler 2 Heat', 'EH 2  Heat', 'ELT 2 Heat', 'Solar 2 Heat', 'CSHP 3 Heat', 'Waste 3 Heat', 'Geoth 3 Heat', 'CHP 3 Heat', 'HP 3 Heat', 'Boiler 3 Heat', 'EH 3 Heat', 'ELT 3 Heat', 'Solar 3 Heat']
                    valuesData = stdDF.loc['Annual', ['0401_CSHP1Heat', '0402_Waste1Heat', '0005_Boiler1Heat', '0302_Solar1Heat', '0403_CSHP2Heat', '0404_Waste2Heat', '0501_Geoth2Heat',   '0006_CHP2Heat', '0007_HP2Heat', '0008_Boiler2Heat', '0009_EH2Heat', '0010_ELT2Heat', '0304_Solar2Heat', '0405_CSHP3Heat', '0406_Waste3Heat', '0504_Geoth3Heat',  '0013_CHP3Heat', '0014_HP3Heat', '0015_Boiler3Heat', '0016_EH3Heat', '0017_ELT3Heat', '0306_Solar3Heat']].tolist()
                    templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

                elif plot['xdata'] == 'District Heat Gr.1':
                    xStart = xEnd = 'Annual'
                    labelsData = ['CSHP 1 Heat', 'Waste 1 Heat', 'Boiler 1 Heat', 'Solar 1 Heat']
                    valuesData = stdDF.loc['Annual', ['0401_CSHP1Heat', '0402_Waste1Heat', '0005_Boiler1Heat', '0302_Solar1Heat']].tolist()
                    templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

                elif plot['xdata'] == 'District Heat Gr.2':
                    xStart = xEnd = 'Annual'
                    labelsData = ['CSHP 2 Heat', 'Waste 2 Heat', 'Geoth 2 Heat', 'CHP 2 Heat', 'HP 2 Heat', 'Boiler 2 Heat', 'EH 2 Heat', 'ELT 2 Heat', 'Solar 2 Heat']
                    valuesData = stdDF.loc['Annual', ['0403_CSHP2Heat', '0404_Waste2Heat', '0501_Geoth2Heat', '0006_CHP2Heat', '0007_HP2Heat', '0008_Boiler2Heat', '0009_EH2Heat',  '0010_ELT2Heat', '0304_Solar2Heat']].tolist()
                    templateFormat = '%{label}<br>%{value} (TWh/year)<br>%{percent}'

                elif plot['xdata'] == 'District Heat Gr.3':
                    xStart = xEnd = 'Annual'
                    labelsData = ['CSHP 3 Heat', 'Waste 3 Heat', 'Geoth 3 Heat', 'CHP 3 Heat', 'HP 3 Heat', 'Boiler 3 Heat', 'EH 3 Heat', 'ELT 3 Heat', 'Solar 3 Heat']
                    valuesData = stdDF.loc['Annual', ['0405_CSHP3Heat', '0406_Waste3Heat', '0504_Geoth3Heat', '0013_CHP3Heat', '0014_HP3Heat', '0015_Boiler3Heat', '0016_EH3Heat',  '0017_ELT3Heat', '0306_Solar3Heat']].tolist()
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

                elif plot['xdata'][:14] == 'Energy Balance':
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

                if plot['xdata'][:14] != 'Energy Balance':
                    xData = stdDF.loc[xStart:xEnd].index.values.tolist()
                xTitle = ''

            ### calc Y series
            
            yData = []

            if plot['xdata'][:14] == 'Energy Balance':
                for yData_i, headers in enumerate(list(stdDF.columns.values)):
                    if headers[:2] == 'g1':
                        yData.append(headers)
                yData.pop()
                yTitle = plot['xdata']

            elif plot['xdata'][0:16] == 'Investment Costs':
                if plot['xdata'] == 'Investment Costs - Total':
                    yData = ['g0-Data1']
                    yTitle = plot['xdata'] + ' (M Euro)'

                elif plot['xdata'] == 'Investment Costs - Annual':
                    yData = ['g0-Data2']
                    yTitle = plot['xdata'] + ' (M Euro)'

                elif plot['xdata'] == 'Investment Costs - O & M':
                    yData = ['g0-Data3']
                    yTitle = plot['xdata'] + ' (M Euro)'

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

            ### add index and columns to sumDF
            pltDF = pd.DataFrame(0, pltInfoList, ['test'])

            stdDF = pd.concat([pltDF,stdDF.loc[xData, yData]])

            stdDF.loc['pltid',:] = plot['id']
            stdDF.loc['stdid',:] = plot['datasrc']['id']
            stdDF.loc['stdname',:] = plot['datasrc']['name']
            stdDF.loc['datatype',:] = plot['datatype']
            stdDF.loc['tracetype',:] = plot['tracetype']
            stdDF.loc['tracestyle',:] = plot['tracestyle']
            stdDF.loc['tracefill',:] = plot['tracefill']
            stdDF.loc['xstart',:] = plot['xstart']
            stdDF.loc['xend',:] = plot['xend']
            stdDF.loc['xtitle',:] = plot['xtitle']
            stdDF.loc['ytitle',:] = plot['ytitle']
            stdDF.loc['xtick',:] = plot['xtick']
            stdDF.loc['xstep',:] = plot['xstep']
            stdDF.loc['ytick',:] = plot['ytick']
            stdDF.loc['ystep',:] = plot['ystep']

            stdDF.drop(['test'], axis= 1, inplace=True)

            for col in stdDF.columns.values.tolist():
                colName = stdDF[col].name
                colName = colName[colName.find('_') +1:]
                colName = stdDF[col].loc['stdname'] + ': ' + colName + str(j)
                stdDF.rename(columns= {stdDF[col].name: colName}, inplace= True)

            sumDF = sumDF.join(stdDF)

        sumDF['index'] = sumDF.index
        sumDF.set_index('indNum', inplace= True, drop= True)
        sumDF.sort_index(axis= 0, ascending= True, inplace= True)
        sumDF.set_index('index', inplace= True, drop= True)
        sumDF.dropna(axis= 0, how= 'all', inplace= True)

        if statMean:
            colMean = sumDF.iloc[16:].mean(axis= 1).tolist()
            tmpList = [0] * 16
            tmpList.extend(colMean)
            colMean = tmpList
            sumDF.insert(0, 'Mean', colMean)
            sumDF['Mean'].iloc[:15] = sumDF.iloc[:15, -1]

        if statMedian:
            colMedian = sumDF.iloc[16:].median(axis= 1).tolist()
            tmpList = [0] * 16
            tmpList.extend(colMedian)
            colMedian = tmpList
            sumDF.insert(0, 'Median', colMedian)
            sumDF['Median'].iloc[:15] = sumDF.iloc[:15, -1]

        if statOnly and ('Mean' in sumDF.columns.values.tolist() or 'Median' in sumDF.columns.values.tolist()):
            for col in sumDF:
                if col == 'Median' or col == 'Mean':
                    pass
                else:
                    sumDF.drop([col], axis= 1, inplace= True)
        
        indexLoc = sumDF.index.get_loc('ystep') +1

        if srcPltGrouped[i]['trace'][0] == 'Scatter Plot':
            for col in sumDF.columns.values.tolist():

                if sumDF[col].loc['tracefill']:
                    styleFill = 'tonexty'
                else:
                    styleFill = 'none'

                if sumDF[col].loc['tracestyle'] == 'Smooth Linear':
                    styleMode = 'lines'
                    styleLine = {'shape': 'spline'}
                else:
                    styleMode = str(sumDF[col].loc['tracestyle']).replace('Only', '').replace(' ', '').strip().lower()
                    styleLine = {'shape': 'linear'}

                figure.add_trace(plygo.Scatter(
                    x= sumDF[col].iloc[indexLoc:].index.tolist(),
                    y= sumDF[col].iloc[indexLoc:].values.tolist(),
                    connectgaps= False, 
                    fill= styleFill, 
                    mode= styleMode, 
                    line= styleLine, 
                    name= col[:-1]
                    ), row= posRow, col= posCol)

        #elif sumDF[col].loc['tracetype'] == 'Bar Chart':
        if srcPltGrouped[i]['trace'][0] == 'Bar Chart':
            for col in sumDF.columns.values.tolist():

                figure.add_trace(plygo.Bar(
                    x= sumDF[col].iloc[indexLoc:].index.tolist(),
                    y= sumDF[col].iloc[indexLoc:].values.tolist(),
                    text= sumDF[col].iloc[indexLoc:].values.tolist(), 
                    texttemplate= '%{y:,.2d}',
                    textfont_color= '#000000', 
                    textposition= 'inside',
                    name= col[:-1]
                    ), row= posRow, col= posCol)

            figure.update_layout({'barmode': str(sumDF[col].loc['tracestyle'])[:-2].replace(' ', '').strip().lower()})

        #elif sumDF[col].loc['tracetype'] == 'Pie Chart':
        if srcPltGrouped[i]['trace'][0] == 'Pie Chart':
            for col in sumDF.columns.values.tolist():

                if sumDF[col].loc['tracestyle'] == 'Domain':
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

        #elif sumDF[col].loc['tracetype'] == 'Box Plot':
        if srcPltGrouped[i]['trace'][0] == 'Box Plot':
            print(sumDF)
            break
            for col in sumDF.columns.values.tolist():

                figure.add_trace(plygo.Box(
                    x= '',
                    y= '',
                    boxpoints= '',
                    names= '',
                    jitter= 0.3
                ))

        ### update layout & axes
        figure.update_xaxes({'title_text': xTitle, 'tickmode': sumDF.loc['xtick'].values.tolist()[0], 'tick0': 0, 'dtick': sumDF.loc['xstep'].values.tolist()[0], 'tickangle': -45}, row= posRow, col= posCol)
        figure.update_yaxes({'title_text': yTitle, 'tickmode': sumDF.loc['ytick'].values.tolist()[0], 'tick0': 0, 'dtick': sumDF.loc['ystep'].values.tolist()[0], 'tickangle': 0}, row= posRow, col= posCol)
            
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
            stdDF = stdDF.loc[:, 'g1_Total']
    
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
