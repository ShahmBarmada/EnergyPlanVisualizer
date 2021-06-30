import tkinter, re, os
import pandas as pd
from tkinter import filedialog

rootWindow = tkinter.Tk()
rootWindow.withdraw()

inputPath = filedialog.askopenfilename()
outputPath = filedialog.askdirectory()

outputPath1 = outputPath + "/Output.txt"
outputPath2 = outputPath + "/Output2.txt"
outputPath3 = outputPath + "/Output3.txt"

exceptionList1 = ['RESULT: Da','ANNUAL CO2','SHARE OF R','ANNUAL FUE','ANNUAL COS']
exceptionList2 = ['EnergyPLAN','RESULT: Da','Technical ','Critical E']
exceptionList3 = ['Coal ','Oil ','N.Gas ','Biomass ','Renewable ','H2 Etc. ','Biofuel ','Nucl/Ccs ','Total ','So2 ','Pm2.5 ','Nox ','Ch4 ','N2O ','Detailed Emi']
headerList = ['Index','g0-Data1','g0-Data2','g0-Data3','g1-DHP','g1-CHP2','g1-CHP3','g1-Boiler2','g1-Boiler3','g1-PP','g1-Geo/Nu','g1-Hydro','g1-Waste/HTL','g1-CAES/ELT','g1-BioCon','g1-EFuel','g1-VRES','g1-SolarTh','g1-Transp','g1-Househ','g1-Ind/Var','g1-Total','g2-ElectrDemand','g2-ElecdemCooling','g2-FixedExp/Imp','g2-DHDemand','g2-WindElectr','g2-OffshoreElectr','g2-PVElectr','g2-CSPElectr','g2-RiverElectr','g2-WaveElectr','g2-TidalElectr','g2-CSP2Electr','g2-CSP2Storage','g2-CSP2loss','g2-HydroElectr','g2-Hydropump','g2-Hydrostorage','g2-HydroWat-Sup','g2-HydroWat-Loss','g2-SolarHeat','g2-CSHP1Heat','g2-Waste1Heat','g2-Boiler1Heat','g2-Solar1Heat','g2-Sol1StrHeat','g2-CSHP2Heat','g2-Waste2Heat','g2-Geoth2Heat','g2-Geoth2Steam','g2-Geoth2Storage','g2-CHP2Heat','g2-HP2Heat','g2-Boiler2Heat','g2-EH2Heat','g2-ELT2Heat','g2-Solar2Heat','g2-Sol2StrHeat','g2-Storage2Heat','g2-Balance2Heat','g2-CSHP3Heat','g2-Waste3Heat','g2-Geoth3Heat','g2-Geoth3Steam','g2-Geoth3Storage','g2-CHP3Heat','g2-HP3Heat','g2-Boiler3Heat','g2-EH3Heat','g2-ELT3Heat','g2-Solar3Heat','g2-Sol3StrHeat','g2-Storage3Heat','g2-Balance3Heat','g2-FlexibleElectr','g2-HPElectr','g2-CSHPElectr','g2-CHPElectr','g2-PPElectr','g2-PP2Electr','g2-NuclearElectr','g2-GeotherElectr','g2-PumpElectr','g2-TurbineElectr','g2-PumpedStorage','g2-Pump2Electr','g2-Turbine2Electr','g2-Pumped2Storage','g2-RockinElectr','g2-RockoutSteam','g2-RockstrStorage','g2-ELT2Electr','g2-ELT2H2ELT2','g2-ELT3Electr','g2-ELT3H2ELT3','g2-V2GDemand','g2-V2GCharge','g2-V2GDischa','g2-V2GStorage','g2-H2Electr','g2-H2Storage','g2-CO2HydroElectr','g2-NH3HydroElectr','g2-CO2Hydroliqfuel','g2-NH3HydroAmmonia','g2-HH-CHPElectr','g2-HH-HPElectr','g2-HH-HP/EBElectr','g2-HH-EBElectr','g2-HH-H2Electr','g2-HH-H2Storage','g2-HH-H2Prices','g2-HHDemHeat','g2-HHCHP+HPHeat','g2-HHBoilHeat','g2-HHSolarHeat','g2-HHStoreHeat','g2-HHBalanHeat','g2-StabilLoadPercent','g2-ImportElectr','g2-ExportElectr','g2-CEEPElectr','g2-EEEPElectr','g2-ExMarketPrices','g2-ExMarketProd','g2-SystemPrices','g2-InMarketPrices','g2-Btl-neckPrices','g2-ImportPayment','g2-ExportPayment','g2-BltneckPayment','g2-AddexpPayment','g2-Boilers','g2-CHP2+3','g2-PPCAES','g2-Indi-vidual','g2-Transp','g2-IndustVarious','g2-DemandSum','g2-Biogas','g2-Syngas','g2-CO2HyGas','g2-SynHyGas','g2-SynFuel','g2-Storage','g2-StorageContent','g2-Sum','g2-ImportGas','g2-ExportGas','g2-FreshWDemand','g2-FreshWStorage','g2-SaltWDemand','g2-BrineProd','g2-BrineStorage','g2-DesalPlElectr','g2-FWPumpElectr','g2-TurbineElectrT','g2-PumpElectrT','g2-CoolGr1Demand','g2-CoolGr2Demand','g2-CoolGr3Demand','g2-Cool-ElDemand','g2-CoolGr1Natural','g2-CoolGr2Natural','g2-CoolGr3Natural','g2-CoolingDHgr1','g2-CoolingDHgr2','g2-CoolingDHgr3','g2-CoolingElectr']
out1 = ''
out2 = ''

opf = open(outputPath1, 'w')

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if line[:10] == 'TOTAL FOR ':
            lineAnnual = i
            next

        elif line[:10] == 'MONTHLY AV':
            lineMonthly = i
            next

        elif line[:10] == 'HOURLY VAL':
            lineHourly = i
            break

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if i < lineAnnual-4:

            if line[:17].isspace():
                next

            elif line[:20].title().find('Warning') != -1:
                line = line.encode('ascii',errors='ignore').decode()
                opf.write(line.replace('\t',' ').replace('WARNING:','\n' + 'Warning').strip() + '\n')
                next

            elif line[:20].title().find('Result') != -1:
                opf.write('InputStudy ' + line[line.rfind('/') + 1 : line.rfind('.txt') + 4].strip().replace('\t',' ') + '\n')
                next

            elif line[:10] in exceptionList1:
                next

            else:
                opf.write(line[:91].replace('\t',' ').strip().title() + '\n')
                next

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if i < lineAnnual-4:

            if line[:95].isspace():
                next

            elif line[:20].title().find('Warning') != -1:
                next

            elif line[:10] in exceptionList2:
                next

            else:
                opf.write(line[91:151].replace('\t',' ').strip().title() + '\n')
                next

opf.close()

opf = open(outputPath2, 'w')

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if i < lineAnnual-4:

            if line[:20].title().find('Warning') != -1:
                next

            elif line[:10] in exceptionList2:
                next
            
            else:
                opf.write(line[151:].replace('\t',' ').strip().title() + '\n')
                next

opf.close()

opf = open(outputPath1, 'a')

with open(outputPath2) as ipf:
    for i, line in enumerate(ipf):

        if line[:10].isspace():
            next

        elif line[:2].replace('\t',' ').strip().isalpha():

            if any((match := x) in line.title() for x in exceptionList3):
                out1 = out1 + (line[:line.find(match)].replace('\t',' ').strip().title() + '   ')
                out2 = out2 + (line[line.find(match):].replace('\t',' ').strip().title() + '\n')

            else:
                out1 = out1 + (line.replace('\t',' ').strip().title() + '   ')

        elif line[:2].replace('\t',' ').strip().isdigit():

            if any((match := x) in line.title() for x in exceptionList3):
                out1 = out1 + (line[:line.find(match)].replace('\t',' ').strip().title() + '\n')
                out2 = out2 + (line[line.find(match):].replace('\t',' ').strip().title() + '\n')

            else:
                out1 = out1 + (line.replace('\t',' ').strip().title() + '\n')

opf.write(out1)
opf.write(out2)

opf.close()

opf = open(outputPath2, 'w')

with open(outputPath1) as ipf:
    for i, line in enumerate(ipf):
        
        if line[:5].strip().isdigit():
            next

        else:
            opf.write(re.sub(r'\s+',r'',re.sub(r'\s+(?=\d|-\d)', r',', re.sub(r'(?!\w)\s(?=\d|-\d)',r'',line))) + '\n')

opf.close()

opf = open(outputPath3, 'w')

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if i > lineAnnual and i <= lineHourly:

            if line.isspace():
                next

            elif i == lineMonthly or i == lineHourly:
                next

            else:
                opf.write(re.sub(r'\s+',r'',re.sub(r'\s+(?=\d|-\d|-\s|Percent)', r',', line)) + '\n')

        elif i > lineHourly:
            opf.write(re.sub(r'\s+(?=\d)', r'h', line[:14]) + ',' + re.sub(r'\s+',r'',line[:14]) + (',' * 21) + re.sub(r'\s+(?=\d|-\d)', r',', line[14:].strip()) + '\n')

opf.close()

opf = open(outputPath1, 'w')

with open(outputPath2) as ipf:
    for i, line in enumerate(ipf):

        if line[:17] == 'DetailedEmissions':
            next

        elif len(re.findall(',',line)) <= 3:
            opf.write(re.sub(r'(?!\w):',r'',line.replace('InputStudy','InputStudy,').replace('planModel','planModel,').replace('RegulationNo.','RegulationNo.,').replace('Percent','').replace('Twh/Year','').replace('Warning',('Warning' + str(i) + ','))))

        elif 18 >= len(re.findall(',',line)) > 3:
            opf.write(line.replace(',', ',,,,', 1))

opf.close()

opf = open(outputPath1, 'a')

with open(outputPath3) as ipf:
    for i, line in enumerate(ipf):
        if line[:1] != 'h':
            opf.write(re.sub(r'(?!\w):',r'',line.replace(',', (',' * 22), 1).replace('Percent','').replace(',-,',',,')))
        else:
            opf.write(line)

opf.close()

dfObj = pd.read_csv(outputPath1, delimiter=',', names=headerList, low_memory=False)
dfObj.to_csv (outputPath + '/Output.csv', index=True)

if os.path.exists(outputPath1):
    os.remove(outputPath1)

if os.path.exists(outputPath2):
    os.remove(outputPath2)

if os.path.exists(outputPath3):
    os.remove(outputPath3)

rootWindow.destroy()
