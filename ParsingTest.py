import pandas, re


inputfile = pandas.read_csv('D:/Projects/EnergyPlanVisualizer/ParserTests/Output1.txt', delimiter=',', header=None, names=range(169), low_memory=False)
inputfile.to_csv ('D:/Projects/EnergyPlanVisualizer/ParserTests/Output1.csv', index=None)

#inputfile = 'D:/Projects/EnergyPlanVisualizer/ParserTests/Output1.txt'
#outputfile = 'D:/Projects/EnergyPlanVisualizer/ParserTests/test.txt'
#
#opf = open (outputfile, 'w')
#with open(inputfile) as ipf:
#    for i, line in enumerate(ipf):
#        opf.write(str(len(re.findall(',',line))) + '\n')
#opf.close()