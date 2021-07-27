import pandas as pd

def plotter (srcFig = dict, srcPlt = list) -> list:
    fig = srcFig['id']
    plt = []
    for i in range(0, len(srcPlt)):
        plt.append(srcPlt[i]['id'])

    return [fig, plt]