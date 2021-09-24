import pandas as pd
import plotly.graph_objects as plygo
import plotly.io as pio
from plotly.subplots import make_subplots

def EnergyBalance (stdCollection = list):

    BulkDF = pd.DataFrame(0, index=['Coal', 'Oil', 'Biomass', 'Renewable', 'H2Etc.', 'Biofuel', 'Nucl/Ccs'], columns=['test'])

    for path in range(len(stdCollection)):
        stdDF = pd.read_csv(stdCollection[path], delimiter=',', low_memory=False, index_col='Index')

        rangeStart = stdDF.index.get_loc('TotalAnnualCosts')
        rangeStart = rangeStart + stdDF.iloc[rangeStart:rangeStart+100].index.get_loc('Coal')
                
        rangeEnd = stdDF.iloc[rangeStart:rangeStart+100].index.get_loc('Nucl/Ccs')
        rangeEnd = rangeEnd + rangeStart +1

        xData = stdDF.iloc[rangeStart:rangeEnd].index.values.tolist()
        
        stdDF = stdDF.iloc[rangeStart:rangeEnd]
        stdDF = stdDF.loc[:, 'g1-Total']

        BulkDF.insert(0, 'std' + str(path), stdDF)

    BulkDF.drop(['test'], axis= 1, inplace=True)
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
    figure.update_yaxes({'title_text': '(TWh\Year)'})
    figure.update_layout(uniformtext_minsize=18, font_size=18, width= 1366 , height= 768, showlegend= True, template= pio.templates['simple_white'])
    return figure
    

def InstalledCapacities (stdCollection = list):
    pass
