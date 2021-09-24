import pandas as pd
import plotly.graph_objects as plygo
import plotly.io as pio
from plotly.subplots import make_subplots
from functools import reduce

def EnergyBalance (stdCollection = list):

    BulkDF = pd.DataFrame(0, index=['Coal', 'Oil', 'Biomass', 'Renewable'], columns=['test']
    #columns=['g1-DHP','g1-CHP2','g1-CHP3','g1-Boiler2','g1-Boiler3','g1-PP','g1-Geo/Nu','g1-Hydro','g1-Waste/HTL','g1-CAES/ELT','g1-BioCon','g1-EFuel','g1-VRES','g1-SolarTh','g1-Transp','g1-Househ','g1-Ind/Var'])
    )

    for path in range(len(stdCollection)):
        stdDF = pd.read_csv(stdCollection[path], delimiter=',', low_memory=False, index_col='Index')

        rangeStart = stdDF.index.get_loc('TotalAnnualCosts')
        rangeStart = rangeStart + stdDF.iloc[rangeStart:rangeStart+100].index.get_loc('Coal')
                
        rangeEnd = stdDF.iloc[rangeStart:rangeStart+100].index.get_loc('Renewable')
        rangeEnd = rangeEnd + rangeStart +1

        xData = stdDF.iloc[rangeStart:rangeEnd].index.values.tolist()
        
#        yData = []

#        for yData_i, headers in enumerate(list(stdDF.columns.values)):
#            if headers[:2] == 'g1':
#                yData.append(headers)
#        yData.pop()

        stdDF = stdDF.iloc[rangeStart:rangeEnd]
        stdDF = stdDF.loc[:, 'g1-Total']

        BulkDF.insert(0, 'std' + str(path), stdDF)

#        BulkDF = reduce(lambda x, y: x.add(y, fill_value=0), [BulkDF, stdDF])
    print(stdDF)
    print(BulkDF)

    figure = make_subplots()

    for i in range(len(BulkDF.index.values.tolist())):
        xDataSeries = []
        for num1 in range(len(BulkDF.columns.values.tolist())):
            xDataSeries.append(xData[i])

        figure.add_trace(plygo.Box(
            x= xDataSeries,
            y= BulkDF.iloc[i].tolist(),
            boxpoints= 'all',
            showlegend= True,
            name= xData[i],
            jitter= 0.3
        ))

    figure.update_layout(uniformtext_minsize=18, font_size=18, width= 1366 , height= 768, showlegend= True, template= pio.templates['simple_white'])
    return figure
    

def InstalledCapacities (stdCollection = list):
    pass
