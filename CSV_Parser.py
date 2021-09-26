import re
import os
import pandas as pd

def csvParser (originalFile: str, inputFile: str, timestamp: str) -> str:
    outputPath = inputFile[:inputFile.rfind('/')]
    outputPath1 = outputPath + "/Output1.txt"
    outputPath2 = outputPath + "/Output2.txt"
    outputPath3 = outputPath + "/Output3.txt"

    exceptionList1 = ['RESULT: Da','ANNUAL CO2','SHARE OF R','ANNUAL FUE','ANNUAL COS']
    exceptionList2 = ['EnergyPLAN','RESULT: Da','Technical ','Critical E']
    exceptionList3 = ['Coal ','Oil ','N.Gas ','Biomass ','Renewable ','H2 Etc. ','Biofuel ','Nucl/Ccs ','Total ','So2 ','Pm2.5 ','Nox ','Ch4 ','N2O ','Detailed Emi']
    headerList = ['Index','g0-Data1','g0-Data2','g0-Data3','g1-DHP','g1-CHP2','g1-CHP3','g1-Boiler2','g1-Boiler3','g1-PP','g1-Geo/Nu','g1-Hydro','g1-Waste/HTL','g1-CAES/ELT','g1-BioCon','g1-EFuel','g1-VRES','g1-SolarTh','g1-Transp','g1-Househ','g1-Ind/Var','g1-Total','0001_ElectrDemand','0002_ElecdemCooling','0003_FixedExp/Imp','0004_DHDemand','0101_WindElectr','0102_OffshoreElectr','0103_PVElectr','0104_CSPElectr','0105_RiverElectr','0106_WaveElectr','0107_TidalElectr','0108_CSP2Electr','0109_CSP2Storage','0110_CSP2loss','0201_HydroElectr','0202_Hydropump','0203_Hydrostorage','0204_HydroWat-Sup','0205_HydroWat-Loss','0301_SolarHeat','0401_CSHP1Heat','0402_Waste1Heat','0005_Boiler1Heat','0302_Solar1Heat','0303_Sol1StrHeat','0403_CSHP2Heat','0404_Waste2Heat','0501_Geoth2Heat','0502_Geoth2Steam','0503_Geoth2Storage','0006_CHP2Heat','0007_HP2Heat','0008_Boiler2Heat','0009_EH2Heat','0010_ELT2Heat','0304_Solar2Heat','0305_Sol2StrHeat','0011_Storage2Heat','0012_Balance2Heat','0405_CSHP3Heat','0406_Waste3Heat','0504_Geoth3Heat','0505_Geoth3Steam','0506_Geoth3Storage','0013_CHP3Heat','0014_HP3Heat','0015_Boiler3Heat','0016_EH3Heat','0017_ELT3Heat','0306_Solar3Heat','0307_Sol3StrHeat','0018_Storage3Heat','0019_Balance3Heat','0020_FlexibleElectr','0021_HPElectr','0022_CSHPElectr','0023_CHPElectr','0601_PPElectr','0602_PP2Electr','0701_NuclearElectr','0702_GeotherElectr','0801_PumpElectr','0901_TurbineElectr','1001_PumpedStorage','0802_Pump2Electr','0902_Turbine2Electr','1002_Pumped2Storage','0903_RockinElectr','0904_RockoutSteam','0905_RockstrStorage','1101_ELT2Electr','1102_ELT2H2ELT2','1201_ELT3Electr','1202_ELT3H2ELT3','1301_V2GDemand','1302_V2GCharge','1303_V2GDischa','1304_V2GStorage','2001_H2Electr','2002_H2Storage','2003_CO2HydroElectr','2004_NH3HydroElectr','2005_CO2Hydroliqfuel','2006_NH3HydroAmmonia','1801_HH-CHPElectr','1802_HH-HPElectr','1803_HH-HP/EBElectr','1804_HH-EBElectr','1901_HH-H2Electr','1902_HH-H2Storage','1903_HH-H2Prices','1701_HHDemHeat','1702_HHCHP+HPHeat','1703_HHBoilHeat','1704_HHSolarHeat','1705_HHStoreHeat','1706_HHBalanHeat','0024_StabilLoadPercent','0025_ImportElectr','0026_ExportElectr','0027_CEEPElectr','0028_EEEPElectr','1401_ExMarketPrices','1402_ExMarketProd','1501_SystemPrices','1502_InMarketPrices','1503_Btl-neckPrices','0029_ImportPayment','1601_ExportPayment','1602_Blt-neckPayment','0030_Add-expPayment','2301_Boilers','2302_CHP2+3','2303_PPCAES','2304_Indi-vidual','2305_Transp','2306_IndustVarious','2307_DemandSum','2308_Biogas','2309_Syngas','2310_CO2HyGas','2311_SynHyGas','2312_SynFuel','2313_Storage','2314_StorageContent','2315_Sum','2316_ImportGas','2317_ExportGas','2201_FreshWDemand','2202_FreshWStorage','2203_SaltWDemand','2204_BrineProd','2205_BrineStorage','2206_DesalPlElectr','2207_FWPumpElectr','2208_TurbineElectr','2209_PumpElectr','2101_CoolGr1Demand','2102_CoolGr2Demand','2103_CoolGr3Demand','2104_Cool-ElDemand','2105_CoolGr1Natural','2106_CoolGr2Natural','2107_CoolGr3Natural','2108_CoolingDHgr1','2109_CoolingDHgr2','2110_CoolingDHgr3','2111_CoolingElectr']
    out1 = ''
    out2 = ''

    opf = open(outputPath1, 'w')

    with open(inputFile) as ipf:
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

    with open(inputFile) as ipf:
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

    with open(inputFile) as ipf:
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

    with open(inputFile) as ipf:
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

            elif line[:1].replace('\t',' ').strip().isalpha():

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

    with open(inputFile) as ipf:
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

    dfObj = pd.read_csv(outputPath1, delimiter=',', names=headerList, low_memory=False, index_col='Index')

    print(dfObj.index.get_loc('Annual'))

    with open(originalFile) as ipf:
        for i, line in enumerate(ipf):
            if line == 'input_cap_pp_el':
                value = ipf.readline(i + 1)


    studyName = dfObj.loc['InputStudy','g0-Data1']
    studyName = studyName[:studyName.rfind('.')]
    studyPath = outputPath + '/' + studyName + '_' + timestamp + '.csv'
    dfObj.to_csv (studyPath, index=True)

    if os.path.exists(outputPath1):
        os.remove(outputPath1)

    if os.path.exists(outputPath2):
        os.remove(outputPath2)

    if os.path.exists(outputPath3):
        os.remove(outputPath3)

    if os.path.exists(inputFile):
        os.remove(inputFile)

    return studyPath